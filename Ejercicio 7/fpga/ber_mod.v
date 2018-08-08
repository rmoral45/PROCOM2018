`define PRBS_LEN 10

module ber_mod(
                 i_enable,
                 clk,
                 rst,
                 i_valid,
                 i_bit_gen,
                 i_detection,
                 i_phase,
                 o_led
                 );//falta agregar puerto de salida para encender led
      
   localparam PRBS_LEN = `PRBS_LEN;
   localparam MAX_DELAY = `PRBS_LEN + 1; // sumo 1 para incluir un delay de 511
   localparam COUNT_LEN = $clog2(`PRBS_LEN);//bits que necesita el contador

   // Ports

   input i_enable;
   input clk;
   input rst;
   input i_valid; // esto se puede hacer con un modulo externo que envie la senal de valid o un contador interno al modulo
   input i_bit_gen; //entrada que viene del prbs
   input i_detection; //entrada que viene del rx
   input [1:0] i_phase;
   output      o_led;
   

   // Vars
   
   wire                         reset ;
   wire                         reset_condition;
   wire                         ber0;
   reg  [1:0]                   phase_value;//registro el valor de phase para detectar cambios
   reg                          enable_value;//registro el valor de enable para detectar encendido
   reg  [PRBS_LEN -1 :  0]      buffer; //buffer para almacenar la secuencia de bits recibida(i_bit_gen)
   reg  [COUNT_LEN -1 : 0]      system_delay;//incrementa cada 511 bits recibidos
   reg  [COUNT_LEN -1 : 0]      min_delay; //para almacenar el delay en el que hay menor ber
   reg  [COUNT_LEN -1 : 0]      ber_counter;
   reg  [COUNT_LEN -1 : 0]      min_ber;
   reg  [COUNT_LEN -1 : 0]      counter;//para contar cuantos bits llegaron,va de 0 a 511 siempre
   reg                          adapt_flag;

   assign reset     =  ~rst;
   assign reset_condition = ( ( (enable_value==1'b0) & (i_enable==1'b1) ) | (phase_value ^ i_phase) ) ;
   assign ber0 = (min_ber == 0) ? 1'b1 : 1'b0; 
   
   
   always@(posedge clk or posedge reset) begin
      
      if(reset || reset_condition) begin
         
        phase_value <= i_phase;
        enable_value <= i_enable;
        buffer <= {PRBS_LEN{1'b0}};//ESTO SOLO SE INICIALIZA EN EL RESET !!!!!!
        system_delay <= {COUNT_LEN{1'b0}};
        min_delay <= {COUNT_LEN{1'b0}};
        min_ber <= {COUNT_LEN{1'b1}};
        ber_counter <= {COUNT_LEN{1'b0}};
        adapt_flag <= 1'b1;   
        counter <= {COUNT_LEN{1'b0}};      
         
      end
      //fase de adaptacion, para contar errores deberia estar la flag,el rx habilitado y valid en 1 segun yo  
      else if (enable_value && i_valid && adapt_flag) begin
            phase_value <= phase_value;
            buffer <= {buffer[PRBS_LEN - 2 : 0],i_bit_gen};//left shift
            counter <= counter + 1'b1;
            if( system_delay == MAX_DELAY) begin//termino fase de adaptacion(511*511 pasadas), == (MAX_DELAY - 1)????
                                                //va a andar para el caso que system_delay deba ser 511?? -> revisar
                //revisar que registros setear aca !!!!!!!!!!
                adapt_flag <= 1'b0;
                ber_counter <= {COUNT_LEN{1'b0}};
                
            end
            
            else if (counter == PRBS_LEN) begin //veo si es ber p este delay es menor que para el delay anterior(c/511)
                
                if(ber_counter < min_ber)begin
                    
                    min_ber <= ber_counter;
                    min_delay <= system_delay;
                    
                end
                else begin
                    
                    min_ber <=min_ber;
                    min_delay <= min_delay;
                    
                end
                //reseteo los contadores
                ber_counter <= {COUNT_LEN{1'b0}};
                counter <= {COUNT_LEN{1'b0}}; 
                system_delay <= system_delay + 1;
                adapt_flag <= adapt_flag; // ES NECESARIO ????? 8====3
                
            end
            
            else begin //cuento errores
              // buffer <= {buffer[PRBS_LEN - 2 : 0],i_bit_gen};//left shift
               //counter <= counter + 1;
                 if( buffer[system_delay] ^ i_detection)//si el detectado y enviado son distintos
                     ber_counter <= ber_counter + 1;
                 else
                     ber_counter <= ber_counter;    
                    
            end
         
      end
      else begin //no estoy en fase de adaptacion,no modifico nada
         
         ber_counter <= ber_counter;
         system_delay <= system_delay;
         adapt_flag <= adapt_flag;
         buffer <= buffer;
         system_delay <= system_delay;
         min_delay <= min_delay;
         ber_counter <= ber_counter;
         adapt_flag <= adapt_flag;   
         counter <= counter;
         phase_value <= phase_value;
         
       end  
      
   end



endmodule //