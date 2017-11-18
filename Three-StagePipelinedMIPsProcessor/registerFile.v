module regfile32x32( input [4:0] readaddr1, readaddr2, writeaddr, 
							input clk, we, input [31:0] writedata, input [12:0] reg30_in,
							output reg [31:0] readdata1, readdata2, reg30_out);
	

	reg [31:0] regfile [31:0];
	initial begin
		regfile[0] = 32'b0;		
		regfile[21] = 32'hc000;
	end

	//writing
	always @(posedge clk) begin
		//writing
		if(we && writedata !== 1'dx && writedata !== 1'dz) begin
			if(writeaddr !== 5'h1E && writeaddr !== 5'b0) regfile[writeaddr] <= writedata; 
			else if(writeaddr == 5'h1E ) begin
				reg30_out  <= writedata;
			end
			$display("Writing to Register: ");
			$display("\twriteaddr: %d", writeaddr);
			$display("\twritedata: %d", writedata);
		end //end if	
	end //end always
	always @(negedge clk) begin
		
	end
	always@(*) begin
		readdata1 = regfile[readaddr1];
		readdata2 = regfile[readaddr2];
		$display("Reading from Register: ");
		if(readaddr1 == 5'h1E ) readdata1 = {19'b0, reg30_in};
		if(readaddr2 == 5'h1E ) readdata2 = {19'b0, reg30_in};
		$display("\treadaddr1: %d", readaddr1);
		$display("\treadaddr2: %d", readaddr2);
		$display("\treaddata1: %d", readdata1);
		$display("\treaddata2: %d", readdata2);
	end
endmodule 