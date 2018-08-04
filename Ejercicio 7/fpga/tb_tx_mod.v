// TB


`timescale 1ns/100ps

module tb_tx_mod();

   
   reg                 enable;
   wire    [10:0]      tx_out;
  
   reg                 ck_rst   ;
   reg                 CLK100MHZ;
   wire                bit_out;


   //localparam COEF = {8'd0,8'd1,8'd2,8'd3,8'd4,8'd5,8'd6,8'd7,8'd8,8'd9,8'd10,8'd11,
   //                    8'd12,8'd13,8'd14,8'd15,8'd16,8'd17,8'd18,8'd19,8'd20,8'd21,8'd22,8'd23};

   initial begin
  
      CLK100MHZ    = 1'b0  ;
      ck_rst       = 1'b0  ;
      enable   = 1'b0  ;
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

