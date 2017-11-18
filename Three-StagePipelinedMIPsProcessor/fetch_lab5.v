module fetch( input clk, rst, stall_EX, input [9:0] branch_addr_EX, jtype_addr_EX, reg_addr_EX,
input [1:0] pc_src_EX, output reg [31:0] instruction_EX, output reg [9:0] pc_FETCH);
							
	reg [31:0] mem [2000:0];
	reg [9:0] pc;
	initial begin
		//$readmemh("./display_test.txt", mem, 0, 1023); 
		//$readmemh("./test_please_ugh.txt", mem, 0, 2000); 
		$readmemh("./one_more_time_2.txt", mem, 0, 2000); 
		//$readmemh("./no_delay.txt", mem, 0, 2000); 
		//$readmemh("./testing.txt", mem, 0, 2000);
		//$readmemh("./test_please_ugh.txt", mem, 0, 1023); 
		pc <= 0;
	end

	always@(posedge clk, posedge rst) begin
		$display("**********************\nPC: %d", pc);
		if(rst) begin
			instruction_EX <= 32'b0;
			pc <= 0;
			$display("rest");
		end
		else begin
			if( (pc_src_EX == 2'b11)) begin
				pc <= reg_addr_EX;
				$display("set new register");	
				instruction_EX <= 32'b0;
			end
			else if(pc_src_EX == 2'b1) begin
				pc <= branch_addr_EX;
				$display("branch");
				instruction_EX <= 32'b0;
			end
			else if(pc_src_EX == 2'b10) begin
				pc <= jtype_addr_EX;
				$display("jump");
				instruction_EX <= 32'b0;
			end
			else begin
				instruction_EX <= mem[pc];
				pc <= pc +10'b1;
				$display("increment PC");
			end
		end
		pc_FETCH <= pc;	
		//if(stall_EX) instruction_EX = 31'b0;
		//else begin		
		$display("Insruction: %x", instruction_EX);
		$display("next PC: %d", pc);
		$display("pc_src_EX: %b", pc_src_EX);
		//pc = pc +10'b1;
	end
endmodule 