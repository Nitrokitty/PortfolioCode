module vmem8192x24 (
	input clka,
	input clkb,
	input web, //write enable
	input [12:0] addra, //address to get data from
	input [12:0] addrb, //address to write data to
	input [23:0] datab, //data to write
	output reg [23:0] dataa //data retrieved
	);
	
reg [23:0] mem[8191:0];

always @(posedge clka) begin
	dataa <= mem[addra];
end

always @(posedge clkb) 
	if (web)
		mem[addrb] <= datab;
endmodule
