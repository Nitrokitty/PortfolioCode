module controlUnit( 
	input [4:0] shamt, 
	input [5:0] function_code, 
	input [5:0] op_code, 
	input alu_lo, alu_zero,
	output reg stall_EX, 
	output reg [1:0] pcsrc_EX, 
	output reg [3:0] alu_op, 
	output reg [4:0] alu_shamt, //shamt_EX
	output reg enhilo,  //will be true for mult/mult instructions
	output reg [2:0]rdrt, //for I type will b 1
	output reg memwrite_EX, //for lw/sw 
	output reg [3:0] regsel, 
	output reg regwrite
	);

	always @(*) begin
		if(op_code == 6'b0) begin //R Type		
			$display("(R) Func Code: %b", function_code);
			memwrite_EX = 1'b0;
			if(function_code == 6'b001000) begin //JR //jump to register
				$display("\tJR");
				alu_op = 4'bX;//noop
				alu_shamt = 5'bX;		
				enhilo = 1'b0;
				regsel = 2'bX;
				pcsrc_EX = 2'b11; //set register
				stall_EX = 1'b1;
				regwrite = 1'b0;
				rdrt = 1'b0;
			end
			else begin
				stall_EX = 1'b0;
				rdrt = 1'b0;
				pcsrc_EX = 2'b0;
				if((function_code ==6'b100000) | (function_code == 6'b100001)) begin //add, addu
					$display("\tADD");
					alu_op = 4'b0100;
					enhilo = 1'b0;
					regsel = 2'b00;
					regwrite = 1'b1;
					alu_shamt = 5'bX;	
				end 
				else if((function_code == 6'b100010) | (function_code == 6'b100011)) begin //sub, subu
					$display("\tSUB");
					alu_op = 4'b0101;
					alu_shamt = 5'bX;
					enhilo = 1'b0;
					regsel = 2'b00;
					regwrite = 1'b1;
				end 
				else if( function_code == 6'b100100) begin //and
					$display("\tAND");
					alu_op = 4'b00_00;
					alu_shamt = 5'bX;
					enhilo = 1'b0;
					regsel = 2'b00;
					regwrite = 1'b1;
				end
				else if( function_code == 6'b100101) begin //or
					$display("\tOR");
					alu_op = 4'b00_01;
					alu_shamt = 5'bX;
					enhilo = 1'b0;
					regsel = 2'b00;
					regwrite = 1'b1;	
				end
				else if( function_code == 6'b100111) begin //nor
					$display("\tNOR");
					alu_op = 4'b00_10;
					alu_shamt = 5'bX;
					enhilo = 1'b0;
					regsel = 2'b00;
					regwrite = 1'b1;	
				end
				else if( function_code == 6'b100110) begin //xor
					$display("\tXOR");
					alu_op = 4'b00_11;
					alu_shamt = 5'bX;
					enhilo = 1'b0;
					regsel = 2'b00;
					regwrite = 1'b1;	
				end
				else if( function_code == 6'b101010) begin //slt
					$display("\tSLT");
					alu_op = 4'b11_00;
					alu_shamt = 5'bX;
					enhilo = 1'b0;
					regsel = 2'b00;
					regwrite = 1'b1;		
				end
				else if( function_code == 6'b101011) begin //sltu. in the wiki it says it should be 101010
					$display("\tSULT");
					alu_op = 4'b11_11;
					alu_shamt = 5'bX;
					enhilo = 1'b0;
					regsel = 2'b00;
					regwrite = 1'b1;
				end
				else if(function_code == 6'b000000) begin
					regsel = 2'b00;
					enhilo = 1'b0;
					if(shamt == 5'bX | shamt == 5'b0) begin
						$display("\tNOOP");
						alu_op = 4'bX;
						alu_shamt = 5'bX;	
						regwrite = 1'b0;
					end
					else begin
						$display("\tSLL");
						alu_op = 4'b10_00;
						alu_shamt = shamt;
						regwrite = 1'b1;
					end
				end			
				else if( function_code == 6'b000010) begin //srl
					$display("\tSRL");
					alu_op = 4'b10_01;
					alu_shamt = shamt;
					enhilo = 1'b0;
					regsel = 2'b00;
					regwrite = 1'b1;
				end
				else if( function_code == 6'b000011) begin //sra
					$display("\tSRA");
					alu_op = 4'b10_11;
					alu_shamt = shamt;
					enhilo = 1'b0;
					regsel = 2'b00;
					regwrite = 1'b1;
				end		
				else if(function_code == 6'b011000) begin //mult (not multu)
					$display("\tMULT");
					alu_op = 4'b0110;
					alu_shamt = 5'bX;
					enhilo = 1'b1;
					regsel = 2'b00;
					regwrite = 1'b0;
				end
				else if(function_code == 6'b011001) begin //multu
					$display("\tMULTU");
					alu_op = 4'b01_11;
					alu_shamt = 5'bX;
					enhilo = 1'b1;
					regsel = 2'b00;
					regwrite = 1'b0;
				end
				else if(function_code == 6'b010000) begin //mfhi
					$display("\tMFHI");
					alu_op = 4'bX;
					alu_shamt = 5'bX;
					enhilo = 1'b0;
					regsel = 2'b01;
					regwrite = 1'b1;
				end
				else if(function_code == 6'b010010) begin //mflo
					$display("\tMFLO");
					alu_op = 4'bX;
					alu_shamt = 5'bX;
					enhilo = 1'b0;
					regsel = 2'b10;
					regwrite = 1'b1;
				end
				else begin
					$display("UNKNOWN R-Type OPCODE");
					alu_op = 4'bX;
					alu_shamt = 5'bX;
					enhilo = 1'bX;
					regsel = 2'bX;
					regwrite = 1'bX;
				end
			end
		end //End R type
		//New Stuff
		else begin
			enhilo = 1'b0;
			$display("(I) OP Code: %b", op_code);
			if((op_code == 6'b001000) | (op_code == 6'b001001)) begin //addi & addiU; is sign extended
				$display("\tADDI or ADDIU");
				memwrite_EX = 1'b0;
				//copy of add
				alu_op = 4'b1000;
				alu_shamt = 5'bX;	
				stall_EX = 1'b0;	
				pcsrc_EX = 2'b0;
				rdrt = 1'b1;
				regwrite = 1'b1;
				regsel = 2'b00;
			end
			else if(op_code == 6'b001100) begin //andi; zero extended
				$display("\tANDI");
				memwrite_EX = 1'b0;
				//copy of and
				alu_op = 4'b1100;
				alu_shamt = 5'bX;	
				pcsrc_EX = 2'b0;	
				stall_EX = 1'b0;
				rdrt = 1'b1;
				regwrite = 1'b1;
				regsel = 2'b00;
			end
			else if(op_code == 6'b001101) begin //ORI; zero extended
				$display("\tORI");
				memwrite_EX = 1'b0;
				//copy of or
				alu_op = 4'b1101;
				alu_shamt = 5'bX;
				pcsrc_EX = 2'b0;
				stall_EX = 1'b0;
				rdrt = 1'b1;
				regwrite = 1'b1;
				regsel = 2'b00;
			end
			else if(op_code == 6'b001110) begin //XORI; zero extended
				$display("\tXORI");
				memwrite_EX = 1'b0;
				//copy of xor
				alu_op = 4'b1110;
				alu_shamt = 5'bX;	
				pcsrc_EX = 2'b0;
				stall_EX = 1'b0;
				rdrt = 1'b1;
				regwrite = 1'b1;
				regsel = 2'b00;
			end
			else if(op_code == 6'b001010) begin //SLTI; sign extended
				$display("\tSLTI");
				memwrite_EX = 1'b0;
				//copy of slt
				alu_op = 4'b1010;
				alu_shamt = 5'bX;	
				pcsrc_EX = 2'b0;
				stall_EX = 1'b0;
				rdrt = 1'b1;
				regwrite = 1'b1;
				regsel = 2'b00;
			end
			else if(op_code == 6'b100011) begin //LW
				$display("\tLW");
				memwrite_EX =1'b0;
				regsel = 2'b11;
				//copy of and
				alu_op = 4'b0001;
				alu_shamt = 5'bX;
				pcsrc_EX = 2'b0;
				stall_EX = 1'b0;
				rdrt = 1'b1;
				regwrite = 1'b1;
			end
			else if(op_code == 6'b101011) begin //SW
				$display("\tSW");
				regsel = 2'b00;
				memwrite_EX = 1'b1;
				//copy of and
				alu_op = 4'b1011;
				alu_shamt = 5'bX;	
				pcsrc_EX = 2'b0;
				stall_EX = 1'b0;
				rdrt = 1'b1;
				regwrite = 1'b0;
			end
			else if(op_code == 6'b001111) begin //LUI; like sll but shamt is 16
				$display("\tLUI");
				memwrite_EX = 1'b0;
				//copy of sll
				alu_op = 4'b1111;
				alu_shamt = 5'd16; //shamt is 16		
				pcsrc_EX = 2'b0;
				stall_EX = 1'b0;
				rdrt = 1'b1;
				regwrite = 1'b1;
				regsel = 2'b00;
			end
			else if(op_code == 6'b000100) begin //BEQ
				$display("\tBEQ");
				rdrt = 2'b0;	
				alu_op = 4'b0011; //XOR OPERATION; a == b the zero == 1
				alu_shamt = 5'bX;		
				enhilo = 1'b0;
				memwrite_EX = 1'b0;
				regsel = 2'bX;			
				regwrite = 1'b0;
				if(alu_zero) begin
					$display("\t\tare equal");
					pcsrc_EX = 2'b01; //take branch
					stall_EX = 1'b1; //stall
				end
				else begin
					$display("\t\tare not equal");
					pcsrc_EX = 2'b0;
					stall_EX = 1'b0;
				end		
			end
			else if(op_code == 6'b000101) begin //BNE
				$display("\tBNE");
				//copy of sll
				alu_op = 4'b1110; //XOR OPERATION; a != b then zero == 0
				memwrite_EX = 1'b0;
				alu_shamt = 5'bX;		
				enhilo = 1'b0;
				regsel = 2'bX;		
				rdrt = 1'b1;	
				regwrite = 1'b0;	
				if(~alu_zero) begin
					$display("\t\tare not equal");
					pcsrc_EX = 2'b01; //take branch
					stall_EX = 1'b1; //stall
				end
				else begin
					$display("\t\tare equal");
					pcsrc_EX = 2'b0;
					stall_EX = 1'b0;
				end
			end
			else if(op_code == 6'b000001) begin //BGEZ
				$display("\tBGEZ");
				//copy of sll
				memwrite_EX = 1'b0;
				alu_op = 4'b1001;//slt; if a < b, lo == 0
				alu_shamt = 5'bX;		
				enhilo = 1'b0;
				regsel = 2'bX;
				rdrt = 1'b1;
				regwrite = 1'b0;
				if(alu_lo) begin
					$display("\t\tis greater than or equal to zero");
					pcsrc_EX = 2'b01;
					stall_EX = 1'b1;
				end
				else begin
					$display("\t\tis not greater than or equal to zero");
					pcsrc_EX = 2'b00;
					stall_EX = 1'b0;
				end
			end
			else if(op_code == 6'b000010) begin //J
				$display("\tJ");
				memwrite_EX = 1'b0;
				alu_op = 4'bX;//noop
				alu_shamt = 5'bX;		
				enhilo = 1'b0;
				regsel = 2'bX;
				rdrt = 1'b0;
				pcsrc_EX = 2'b10; //jump
				stall_EX = 1'b1;
				regwrite = 1'b0;
			end
			else if(op_code == 6'b000011) begin //JAL; save pc in to reg 31 then jump; so regsel extends here
				$display("\tJAL");
				memwrite_EX = 1'b0;
				alu_op = 4'bX;//noop
				alu_shamt = 5'bX;		
				enhilo = 1'b0;
				regsel = 3'b100; // 4 -> regdata = pc
				pcsrc_EX = 2'b10; //jump
				stall_EX = 1'b1;
				regwrite = 1'b1;
				rdrt = 2'b11; // 3 -> rdrt = 31
			end
			else begin
				$display("\tUNKOWN ITYPE OPCODE");
				memwrite_EX = 1'b0;
				//copy of add
				alu_op = 4'bx;
				alu_shamt = 5'bX;	
				stall_EX = 1'bX;	
				pcsrc_EX = 2'bX;
				rdrt = 1'bX;
				regwrite = 1'bX;
				regsel = 2'bX;
			end
		end //I Types
		$display("\tpcsrc_EX: %d", pcsrc_EX);
		$display("\talu_lo: %d", alu_lo);
		$display("\talu_zero: %d", alu_zero);
		$display("\tstall_EX: %d", stall_EX);
	end
endmodule

			