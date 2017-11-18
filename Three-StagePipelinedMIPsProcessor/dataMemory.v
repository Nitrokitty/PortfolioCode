module dataMemory(input [15:0] addr, //rt (desitnation)
input [31:0] dataIn, //word from rt
input we, clk, 
output reg [31:0] dataOut,
output reg [12:0] vga_addr,
output reg [23:0] vga_data,
output reg vga_we
); //memdata_wb. data to send to the register file to write

	reg [31:0] regfile [400:0];

	initial begin
		$readmemb("./sincos.txt", regfile, 0, 400); 
	end
	
	always @(posedge clk) begin
		if(we) begin
			if((addr >= 16'hC000) && (addr <= 16'hF000)) begin
				vga_we <= 1;
				vga_addr <= addr - 16'hC000;
				vga_data <= dataIn[23:0];
			end
			else begin
				vga_we <= 0;
				regfile[addr[9:0]] <= dataIn; 
			end
			$display("Writing to Data Mem: ");
			$display("\taddr: %d", addr);
			$display("\tdataOut: %d", dataIn);
		end
		else vga_we <= 0;
	end //end always

	always@(*) begin
		dataOut = regfile[addr[9:0]];
		$display("Reading from Data Mem");
		$display("\tdataOut: %d", dataOut);
	end
endmodule 