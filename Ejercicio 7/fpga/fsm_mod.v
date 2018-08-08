`define CLOCK_COUNT 3 // REVISAR SI DA BIEN

module fsm_mod(
                clk,
                rst,
                o_valid
               );
               
               
localparam COUNT = `CLOCK_COUNT;
localparam COUNT_BITS = $clog2(COUNT);

input                       clk;
input                       rst;

output  reg                 o_valid;

wire                        reset;
reg  [COUNT_BITS - 1 : 0]   counter;          

assign reset = ~rst;



always @ (posedge clk or posedge reset) begin
    if(reset)begin
        counter<={COUNT_BITS{1'b0}};
        o_valid <= 1'b0;
    end
    
    else begin
        if(counter == COUNT)begin
            counter <= {COUNT_BITS{1'b0}};
            o_valid <= 1'b1;
        end
        else begin
            o_valid <= 1'b0;
            counter <= (counter + 1'b1);
        end   
         
    end
end
               
endmodule              