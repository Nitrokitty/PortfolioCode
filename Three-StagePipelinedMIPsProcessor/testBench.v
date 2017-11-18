module testBench();
	//inputs
	reg clk_tb, rst_tb;
	reg [3:0] stall, pc_src;
	reg [11:0] branch_addr, jtype_addr, reg_addr;
	//outputs
	wire [31:0] instruction;
	wire [9:0] pc_FETCH;
	reg [31:0] vectornum;
	reg [31:0] instruction_EX;
	reg [39:0] testvectors [19:0];
	wire [31:0] output_final;
	wire [24:0] data;
	wire [31:0] output_data;
	wire [12:0] vga_addr;
	wire vga_we;
	
	/*fetch goFetch( .clk(clk_tb), .rst(rst_tb), .stall_EX(stall[0:0]), .branch_addr_EX({instruction[9:0]+pc_FETCH}), 
	.jtype_addr_EX(instruction[9:0]), .reg_addr_EX(10'd1), .pc_src_EX(pc_src[1:0]), 
	.instruction_EX(instruction), .pc_FETCH(pc_FETCH[9:0]));*/
	
	//initalizing file and rest
	initial begin 
		//$readmemh("$HOME/Documents/CSCE-611/Project3/inputs.txt", testvectors); //input file
		//vectornum = 0;
		rst_tb = 1; #4; rst_tb=0; 
	end
	
	//initializing clock
	always begin 
		clk_tb=0; #5; clk_tb=1; #5; 
	end 

	execWrite EW( .clk(clk_tb), .rst(rst_tb), .keys(4'd4), .output_data(output_data), .vga_we(vga_we), .vga_addr(vga_addr), .vga_data(data));


always @(posedge clk_tb) begin
	if(vga_we) begin
		$display("writing to vga: ");
		$display("addr: %d", vga_addr);
		$display("data: %d", data);
	end
end
endmodule
