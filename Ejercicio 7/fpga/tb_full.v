`timescale 1ns/100ps

module tb_full();
    
    wire    [11:0]      tx_out;
    wire                bit_gen;
    wire                o_valid;
    wire                detection;
    reg                 tx_enable;
    reg                 rx_enable;
    reg                 rst;
    reg                 CLK100MHZ;
    reg     [1:0]       phase;
    
    initial begin
        CLK100MHZ    = 1'b0  ;
        rst       = 1'b1  ;
        tx_enable   = 1'b0  ; //RX ENABLE!!!!!!!!!!!!!!!!!1
        rx_enable = 1'b0;
        phase = 2'b10;
        #10 rst  = 1'b0  ; //se resetea con reset por bajo,checkear
        #3 rst = 1'b1;
        #20 tx_enable = 1'b1;
        #20 rx_enable = 1'b1;
       
        
        #1000000 $finish;
    end
    
    
    always #1 CLK100MHZ = ~CLK100MHZ;
    
    prbs9_mod
    #(
      )
    prbs9_re
            (
             .bit_out(bit_gen),
             .rst(rst),
             .clk(CLK100MHZ),
             .i_valid(o_valid),
             .enable(tx_enable)
            );
   
   tx_mod
    #(
      )
    
   tx_re
        (
         .enable(tx_enable),
         .rst(rst),
         .clk(CLK100MHZ),
         .symbol(bit_gen),
         .conv_out(tx_out)
        );     
        
   rx_mod
    #(
      )     
    rx_re
        (
         .i_enable(rx_enable),        
         .i_tx(tx_out),
         .i_phase(phase),
         .o_detection(detection),
         .rst(rst),
         .clk(CLK100MHZ)
        );
   ber_mod
    #(
      )
   ber_re
        (
         .i_enable(rx_enable),
         .clk(CLK100MHZ),
         .rst(rst),
         .i_valid(o_valid),
         .i_bit_gen(bit_gen),
         .i_detection(detection),
         .i_phase(phase)
        );
   fsm_mod
    #(
      )
   fsm
     (
      .clk(CLK100MHZ),
      .rst(rst),
      .o_valid(o_valid)
     );                       
endmodule             