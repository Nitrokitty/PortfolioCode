module execWrite( input clk, rst, input [3:0] keys, output [31:0] output_data, output [12:0] vga_addr, output [23:0] vga_data, output vga_we);

	//Registers
	reg [31:0] hi_WB, lo_WB, r_WB, readdata2_WB, memData_WB;
	reg [3:0] regsel_WB;
	reg [4:0] regdest_WB;
	reg regwrite_WB, memwrite_WB, pc_FETCH_WB;
	reg [9:0] branch_addr_EX;
	//Wires
	wire enhilo_EX, regwrite_EX, zero_EX, memwrite_EX;	
	wire [2:0] rdrt;
	wire [31:0] readdata1_EX, readdata2_EX, instruction_EX, hi_EX,lo_EX, memData_EX, regdata_WB;
	wire [3:0] alu_op_EX; 
	wire [4:0] shamt_EX; 
	wire [9:0] PC_EX;
	wire [3:0] regsel_EX;
	reg [10:0] data_mem_read_addr;
	wire stall_FETCH;
	wire [1:0] pc_src_EX;
	
	controlUnit controller(.function_code(instruction_EX[5:0]), .op_code(instruction_EX[31:26]), .shamt(instruction_EX[10:6]),
	.alu_op(alu_op_EX), .alu_shamt(shamt_EX), .regwrite(regwrite_EX), .regsel(regsel_EX), .stall_EX(stall_FETCH),
	.enhilo(enhilo_EX), .pcsrc_EX(pc_src_EX),	.memwrite_EX(memwrite_EX), .rdrt(rdrt), .alu_lo(lo_EX[0]), .alu_zero(zero_EX));
	
	regfile32x32 regis( .clk(clk), .writedata(regdata_WB), .we(regwrite_WB), .readaddr1(instruction_EX[25:21]), .readaddr2(instruction_EX[20:16]),
	.writeaddr(regdest_WB), .reg30_in({9'b0, keys}), .readdata1(readdata1_EX), .readdata2(readdata2_EX), .reg30_out(output_data));
	
	alu myalu(.a(readdata1_EX), .b(readdata2_EX), .op(alu_op_EX), .i_type(rdrt[0]), .shamt(shamt_EX), .hi(hi_EX), .lo(lo_EX), .zero(zero_EX), .immediate(instruction_EX[15:0]));
	
	fetch myfetch(.clk(clk), .rst(rst), .branch_addr_EX(PC_EX + instruction_EX[9:0]), .jtype_addr_EX(instruction_EX[9:0]), .pc_src_EX(pc_src_EX),
	.stall_EX(stall_FETCH), .reg_addr_EX(readdata1_EX[9:0]), .instruction_EX(instruction_EX), .pc_FETCH(PC_EX));
	
	dataMemory datMem(.addr(lo_EX[15:0]), .clk(clk), .dataIn(readdata2_EX), .we(memwrite_EX), .dataOut(memData_EX), .vga_addr(vga_addr), .vga_we(vga_we), .vga_data(vga_data));
	
	always @(posedge clk) begin
		$display("EXECUTIVE WRITE: ");
		regdest_WB <= (rdrt == 2'b01) ? instruction_EX[20:16]: ((rdrt == 2'b0) ? instruction_EX[15:11] : 5'b11111); //if rdrt = 1,then I type and then the destination register is rt
		regsel_WB <= regsel_EX;
		regwrite_WB <= regwrite_EX;
		r_WB <= lo_EX;
		//for mult hi/lo
		if(enhilo_EX)begin
			hi_WB <= hi_EX;
			lo_WB <= lo_EX;
		end
		branch_addr_EX <= PC_EX + instruction_EX[9:0];
		memData_WB <= memData_EX;
		$display("\treaddata1_EX :%h", readdata1_EX);
		$display("\treaddata2_EX :%h", readdata2_EX);
		$display("\timmediate: %h", instruction_EX[15:0]);
		$display("\tmemwrite_EX :%b", memwrite_EX);
		$display("\tregdest_WB :%x", regdest_WB);
		$display("\tregdata_WB: %x", regdata_WB);
		$display("\tregsel_WB: %x", regsel_WB);
		$display("\tregwrite_WB: %x", regwrite_WB);
		$display("\tr_WB: %x", r_WB);
		$display("\trdrt: %d", rdrt);
		$display("hi_WB: %x", hi_EX);
		$display("lo_WB: %x", lo_EX);
		end
		
		
//		if(regsel_WB == 2'b1) assign regdata_WB = hi_WB;
//		else if(regsel_WB == 2'b10) assign regdata_WB = lo_WB;
//		else if(regsel_WB ==	2'b11) assign regdata_WB = memData_WB; //from dataMemory
//		else assign regdata_WB = r_WB;
		always@(*) begin

		end
		assign regdata_WB = (regsel_WB == 3'b0) ? r_WB:((regsel_WB == 3'b1) ? hi_WB : ((regsel_WB ==3'b10) ? lo_WB : ((regsel_WB ==3'b11) ? memData_WB : branch_addr_EX))); 
		
		
		//		always @(*) begin
//			case(regsel_WB)
//				3'b00 : regdata_WB = r_WB;
//				3'b01 : regdata_WB = hi_WB;
//				3'b10 : regdata_WB = lo_WB;
//				3'b11 : regdata_WB = memData_WB;
//				3'b100 : regdata_WB = branch_addr_EX;
//			endcase
//		end
		//assign regdata_WB = (regsel_WB == 3'b0) ? r_WB:((regsel_WB == 3'b1) ? hi_WB : ((regsel_WB ==3'b10) ? lo_WB : ((regsel_WB ==3'b11) ? memData_WB : pc_src_EX))); 
		//if the Hi/LO write regsel != 0
		//if it is one, write high. if it is 2, write low

endmodule
	
	