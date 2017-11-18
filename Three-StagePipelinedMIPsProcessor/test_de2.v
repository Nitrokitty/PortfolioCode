module test_de2 (input CLOCK_50,
					  input [3:0] KEY,
					  output reg [17:0] LEDR,
					  output [6:0] HEX0,
					  output [6:0] HEX1,
					  output [6:0] HEX2,
					  output [6:0] HEX3,
					  output [6:0] HEX4,
					  output [6:0] HEX5,
					  output [6:0] HEX6,
					  output [6:0] HEX7,
					  input [17:0] SW
					  );
					  
reg [25:0] clk_div;
wire [31:0] output_data;

//regfile32x32( input [4:0] readaddr1, readaddr2, writeaddr, 
//							input clk, we, input [31:0] writedata, reg30_in,
//							output reg [31:0] readdata1, readdata2, reg30_out);

execWrite EW( .clk(CLOCK_50), .rst(~KEY[0]), .SW(SW), .output_data(output_data));

initial begin
  LEDR <= 0;
  clk_div <= 0;
end

always @(posedge clk_div[22]) LEDR <= LEDR + 18'b1;
always @(posedge CLOCK_50) clk_div <= clk_div+26'b1;


							  
endmodule
