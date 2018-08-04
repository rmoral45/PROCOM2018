`define seed 0xAA1

module prbs9_mod(
                 enable,
                 clk,
                 rst,
                 bit_out
                 );
      
   localparam SEED = 9'h`seed         ;

   // Ports
   output bit_out;

   input enable;
   input clk;
   input rst;
   

   // Vars
   
   wire bit_gen  ;
   reg [8 : 0] state  ;
   wire reset ;

   assign reset     =  ~rst;
   assign bit_out = state[0];
   
   always@(posedge clk or posedge reset) begin
      if(reset) begin
         state<= SEED;
      end
      else if(enable) begin
        state<={state[7:0],(state[8]^state[4])};
      end
      else 
        state<=state;
       
   end



endmodule //
