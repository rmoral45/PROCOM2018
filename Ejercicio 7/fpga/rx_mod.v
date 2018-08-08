`timescale 1ns / 1ps

`define INPUT_BITS 12
`define COEF_BITS 8
`define COEF_FBITS 0
`define LENGTH 24


module rx_mod(
                i_enable,
                i_tx,
                i_phase,
                o_detection,
                rst,
                clk
              );


localparam COEFF = {8'h0, 8'hfe, 8'hff, 8'h0, 8'h2, 8'h0, 8'hfb, 8'hf5,
                    8'hf9, 8'ha, 8'h25, 8'h3e, 8'h48, 8'h3e, 8'h25, 8'ha, 
                    8'hf9, 8'hf5,8'hfb, 8'h0, 8'h2, 8'h0, 8'hff, 8'hfe};


localparam INPUT_BITS = `INPUT_BITS; 
localparam COEF_BITS = `COEF_BITS;
localparam COEF_FBITS = `COEF_FBITS;
localparam LENGTH = `LENGTH ;
localparam FULL_BITS = COEF_BITS * INPUT_BITS + $clog2(LENGTH);

integer i;

input                          i_enable;
input signed [INPUT_BITS -1:0] i_tx;
input [1:0]                    i_phase;
input                          rst;
input                          clk;

output                         o_detection;


reg        [1:0]                phase_counter;
reg signed [FULL_BITS -1 : 0 ]  memory [LENGTH-1:0];
reg signed [COEF_BITS - 1 : 0 ] coeff [LENGTH -1 : 0];
wire                            reset;
reg                             out_bit;

assign reset = ~rst;
assign o_detection = out_bit;

always @ (posedge clk or posedge reset)begin
    if(reset) begin
        phase_counter <= 2'b0;
        out_bit <= 1'b0;
        for( i=0; i<LENGTH ; i=i+1)begin
            memory[i] <= {FULL_BITS{1'b0}};
            coeff[i] <= COEFF[(LENGTH -1) - i]; 
        end    
    end
    else if (i_enable)begin
        phase_counter <= phase_counter + 1;
        memory[0] = i_tx * coeff[0];
        for(i=1; i < LENGTH ; i = i+1)
            memory[i] = (memory[i-1] + coeff[i] * i_tx);
        if(phase_counter == i_phase)begin
            out_bit <= memory[LENGTH-1][FULL_BITS -1];            
        end         
    end
    else begin
        phase_counter <= i_phase;
        out_bit <= out_bit;
        for(i=0 ; i<LENGTH ; i=i+1)
            memory[i] <= memory[i];
    end
end


endmodule