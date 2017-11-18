module my_video_test (input CLOCK_50,
				   output [9:0] VGA_R,
				   output [9:0] VGA_G,
				   output [9:0] VGA_B,
				   output VGA_SYNC,
				   output VGA_BLANK,
				   output VGA_CLK,
				   output VGA_HS,
				   output VGA_VS,
					output [6:0] HEX0,
				   output [6:0] HEX1,
				   output [6:0] HEX2,
				   output [6:0] HEX3,
				   output [6:0] HEX4,
				   output [6:0] HEX5,
				   output [6:0] HEX6,
				   output [6:0] HEX7,
				 	input [3:0] KEY,
					output reg [17:0] LEDR
					);
				   
reg [5:0] row, old_row;
reg [6:0] col, old_col;
wire [23:0] data;
reg [25:0] clk_div;
wire [3:0] not_keys;
wire [31:0] output_data;
wire [12:0] vga_addr;
wire [5:0] write_row;
wire [6:0] write_col;
wire vga_we;

initial begin
  LEDR <= 0;
  clk_div <= 0;
end

always @(posedge clk_div[22]) LEDR <= LEDR + 18'b1;
assign not_keys = ~KEY;
//assign data = (col > 7'd30) && (col < 7'd40) && (row > 6'd30) && (row < 6'd40) ? 24'hff00 : 24'd0;
//assign data = output_data[0] > 0 ? 24'hff00 : 24'd0;
//assign write_col = output_data[7:1];
//assign write_row = output_data[13:8];

execWrite EW( .clk(CLOCK_50), .rst(1'b0), .output_data(output_data), .vga_we(vga_we), .vga_addr(vga_addr), .vga_data(data), .keys(not_keys));

display_if mydisplay (
	 .clk(CLOCK_50),
	 .rst(1'b0),
	 .mem_waddr(vga_addr),
	 .mem_wdata(data),
	 .mem_web(vga_we),
	 .VGA_R(VGA_R),
	 .VGA_G(VGA_G),
	 .VGA_B(VGA_B),
	 .VGA_SYNC(VGA_SYNC),
	 .VGA_BLANK(VGA_BLANK),
	 .VGA_CLK(VGA_CLK),
	 .VGA_HS(VGA_HS),
	 .VGA_VS(VGA_VS)
	 );
	 
display hex0_display (4'b0,HEX0);
display hex1_display (4'b0,HEX1);
display hex2_display (4'b0,HEX2);
display hex3_display (4'b0,HEX3);
display hex4_display (4'b0,HEX4);
display hex5_display (4'b0,HEX5);
display hex6_display (4'b0,HEX6);
display hex7_display (not_keys, HEX7);

always @(posedge CLOCK_50) begin
	if (col==7'd79) begin
		if (row==6'd59) row <= 6'd0; else row <= row + 6'd1;
		col <= 7'd0;
	end else col <= col + 7'd1;
	if(vga_we) begin
		$display("writing to vga: ");
		$display("addr: %d", vga_addr);
		$display("data: %d", data);
	end

end

endmodule
