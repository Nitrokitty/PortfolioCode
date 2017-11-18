
module alu (input [31:0] a,b,
			input[3:0] op,
			input i_type,
			input [4:0] shamt,
			input [15:0] immediate,
			output reg [31:0] hi,lo,
			output reg zero
			);

wire [31:0] zero_extension = {16'b0, {immediate}};
wire [31:0] sign_extension = {{16{immediate[15]}}, {$signed(immediate[15:0])}};
wire [32:0] diff = {1'b0,a}+{1'b0,~b+32'b1};
wire [32:0] diff_i = {1'b0,a}+{1'b0,~sign_extension+32'b1};


always @(*) begin

	//intermediate
	if(i_type) begin
		casez(op)
			4'b1000: lo = $signed(a) + $signed(sign_extension); //add
			4'b0001: lo = a + immediate; //LW
			4'b1011: lo = a + immediate; //SW
			4'b1100: lo = a & zero_extension; // and zero extended
			4'b1101: lo = a | zero_extension; // or zero extended 
			4'b1110: lo = a ^ zero_extension; // xor zero extended
			4'b1010:
				if (~diff_i[32]) lo = 32'b1; // sltu: not sure abourt this one
				else lo = 32'b0;	
			4'b1111: lo = immediate << shamt; // lui
			4'b1001: lo = ($signed(a) >= 0);
			default begin
				$display("Unknown I-Type OpCode: %b", op);
				hi = 32'bX;
				lo = 32'bX;
			end
		endcase
	end
	else	begin
		casez (op)
			// arithmetic operations
			4'b0100: lo = a+b; // add
			4'b0101: lo = $signed(a)-$signed(b); // sub
			
			// mult signed
			4'b0110: {hi,lo} = $signed(a)*$signed(b);
			
			// mult unsigned
			4'b0111: {hi,lo} = a*b;

			// shifter operations
			4'b1000: lo = b << shamt; // sll
			4'b1001: lo = b >> shamt; // srl
			4'b101?: lo = $signed(b) >>> shamt; //sra
			
			// comparison operations
			4'b1100: 
			if ($signed(a) < $signed(b)) lo = 32'b1;
         else lo = 32'b0;
			4'b11??:
			if (~diff[32]) lo = 32'b1; // sltu
			else lo = 32'b0;
							
			// logical operations
			4'b0000: lo = a & b; // and
			4'b0001: lo = a | b; // or
			4'b0010: lo = ~(a | b); // nor
			4'b0011: lo = a ^ b; // xor
			default begin
				$display("Unknown R-Type OpCode: %b", op);
				hi = 32'bX;
				lo = 32'bX;
			end
		endcase
	end

	zero = lo==32'b0 ? 1'b1 : 1'b0;
	$display("ALU: ");
	$display("\ta: %x", a);
	$display("\tb: %x", b);
	$display("\timmediate: %x", immediate);
	$display("\tlo: %x", lo);
	$display("\ti_type: %b", i_type);
	$display("\tzero: %b", zero);
	$display("******");
	
end // always

endmodule