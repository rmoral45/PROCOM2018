// TB


`timescale 1ns/100ps

module tb_tx_mod();

   
   reg                 enable;
   wire    [10:0]      tx_out;
  
   reg                 ck_rst   ;
   reg                 CLK100MHZ;
   wire                bit_out;

   initial begin
  
      CLK100MHZ    = 1'b0  ;
      ck_rst       = 1'b1  ;
      enable   = 1'b0  ;
      #10 ck_rst  = 1'b0  ;
      #10 ck_rst  = 1'b1  ;
      #20 enable = 1'b1;
      #1000000 $finish;
   end

   always #1 CLK100MHZ = ~CLK100MHZ;
   

   prbs9_mod
     #(
       )
   prbs9_re
     (
      .bit_out (bit_out),
      .rst    (ck_rst),
      .clk (CLK100MHZ),
      .enable (enable)
      );

   tx_mod
     #(
       )
   tx_re
     (
      .conv_out (tx_out),
      .rst    (ck_rst)   ,
      .clk (CLK100MHZ),
      .enable (enable),
      .symbol (bit_out)
      );

endmodule // 

