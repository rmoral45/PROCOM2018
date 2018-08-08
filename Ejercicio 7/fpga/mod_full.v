`timescale 1ns/100ps

module tb_full(
                rst,
                CLK100MHZ,
                i_sw,
                o_led
                );
   
input       [3:0]       i_sw; 
input                   rst;
input                   CLK100MHZ;
output      [3:0]       o_led;
  
    
    wire    [11:0]      tx_out;
    wire                bit_gen;
    wire                o_valid;
    wire                detection;
    wire                tx_enable;
    wire                rx_enable;
    wire     [1:0]      phase;
    wire                berled;
    wire                txled;
    wire                rxled;
    wire                rstled;
    

assign tx_enable = i_sw[0];
assign rx_enable = i_sw[1];
assign phase = i_sw[3:2];
assign o_led[0] = i_sw[0];
assign o_led[1] = i_sw[1];
assign o_led[2] = i_sw[2];
assign o_led[3] = berled;


    
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
         .i_phase(phase),
         .o_led(berled)
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