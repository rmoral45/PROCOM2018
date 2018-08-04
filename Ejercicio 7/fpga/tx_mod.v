`define NBIT 8
`define FBIT 7
`define USAMPLE 4
`define LENGTH 24

module tx_mod(
                 enable,
                 clk,
                 rst,
                 symbol,
                 conv_out         
                 ); 

localparam OUT_FBITS = `FBIT;
localparam OUT_BITS = `NBIT;
localparam OUT_IBITS = OUT_BITS-OUT_FBITS;
localparam USAMPLE = `USAMPLE;
localparam LENGTH =  `LENGTH;
//localparam FULL_BITS = NBIT + $clog2(LENGTH/USAMPLE);
localparam FULL_BITS = 32;
localparam FULL_FBITS = 32;
localparam FULL_IBITS = FULL_BITS - FULL_FBITS;
localparam PHASE_BITS = $clog2(USAMPLE);
localparam SAT_BITS = FULL_IBITS - OUT_IBITS;


    

       

input enable;
input clk;
input rst;
input symbol;
output reg signed  [FULL_BITS - 1:0] conv_out;

wire reset;
reg signed [FULL_BITS -1 : 0]             coeff [LENGTH-1:0];
reg [LENGTH/USAMPLE - 1 : 0]        memory;
reg  signed [FULL_BITS - 1 : 0]     conv_full;  
reg [PHASE_BITS -1: 0]              phase;
reg                                 enable_flag;
reg [7:0]contador_neg;
reg [7:0]contador_pos;
integer i,j;

assign reset = ~rst;

always @ (posedge clk or posedge reset) begin
    if(reset) begin
        memory <= {LENGTH{1'b0}};
        phase <= {PHASE_BITS{1'b0}};
        enable_flag <=1'b0;
        contador_neg <= 0;
        contador_pos <= 0;
        for(i=0; i<LENGTH; i=i+1)
            coeff[i] <= i;
    end
    else if (enable_flag == 0 && enable == 1)begin
        phase<=2'b00;
        enable_flag<= enable;
        memory <= memory;
        contador_pos <= 0;
        contador_neg <= 0;

    end
    else begin
       phase<= (phase+1'b1);
       enable_flag <= enable;
       if(enable_flag && phase == USAMPLE-1)begin
            phase <= 2'b00;
            memory <={memory[LENGTH/USAMPLE-2:0],symbol};
       end
       
    end
    
end
always @ (*)begin
    //convolucin
    conv_full = {FULL_BITS{1'b0}};
    conv_out = {FULL_BITS{1'b0}};
    contador_neg = {8{1'b0}};
    contador_pos = {8{1'b0}};
    if(enable)begin
        for(j=0; j<(LENGTH/USAMPLE); j=j+1) begin
            
                if(memory[j] == 1'b1) begin
                    conv_full = conv_full - coeff[(j*USAMPLE) + phase];
                end
                else begin
                    conv_full = conv_full + coeff[(j*USAMPLE) + phase];
               end
        end
    end
    //conv_out = conv_full;
end

always @ (*) begin
    if(conv_full[FULL_BITS - 1])begin
        if(conv_full[FULL_BITS -1 :(FULL_BITS -1 -SAT_BITS)] ^ {SAT_BITS{1'b1}})begin
            //no saturo
            conv_out = conv_full[FULL_FBITS + OUT_IBITS - 1: FULL_FBITS-OUT_FBITS ];
        end
        else begin
        //saturacion para negativos
            conv_out = {1'b1,{OUT_BITS - 1{1'b0}}};
        end  
    end
    else begin
        if(conv_full[FULL_BITS -1 :(FULL_BITS -1 -SAT_BITS)] ^ {SAT_BITS{1'b0}})begin
            conv_out = conv_full[FULL_FBITS + OUT_IBITS - 1: FULL_FBITS-OUT_FBITS ];
        end
        else begin
            //saturo para positivos, osea todo en 1
            conv_out = {1'b0,{OUT_BITS - 1{1'b1}}};
        end
    end
end

                 
endmodule