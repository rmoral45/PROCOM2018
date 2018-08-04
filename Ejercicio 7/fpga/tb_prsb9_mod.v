// TB

`timescale 1ns/100ps

module tb_prsb9_mod();

   
   reg                 enable;
   wire                 bit_out;
   reg                  ck_rst   ;
   reg                  CLK100MHZ;


   initial begin
  
      CLK100MHZ    = 1'b0  ;
      ck_rst       = 1'b0  ;
      enable   = 1'b1  ;
      #10 ck_rst  = 1'b1  ;
      #1000000 $finish;
   end

   always #1 CLK100MHZ = ~CLK100MHZ;

   prbs9_mod
     #(
       )
   prbs9_re
     (
      .bit_out (bit_out),
      .rst    (ck_rst)   ,
      .clk (CLK100MHZ),
      .enable (enable)
      );

endmodule // 


