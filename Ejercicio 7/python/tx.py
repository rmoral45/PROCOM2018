#IMPORTS
import numpy as np
import matplotlib.pyplot as plt
from tool.DSPtools import *
from tool._fixedInt import  *
from pdb import set_trace as bp
from commpy.filters import rrcosfilter

#DEFINES
ROLL_OFF = 0.5
UPSAMPLE = 4
SENT_LENGHT = 256
N_BAUD = 6
BAUD_RATE = 1./1000000
SIM_ITER =2222
TOTAL_WIDTH_TX = 9
FRAC_WIDTH_TX = 2
INT_WIDTH_TX = TOTAL_WIDTH_TX - FRAC_WIDTH_TX
TOTAL_WIDTH_RX = 15
FRAC_WIDTH_RX = 13
INT_WIDTH_RX = TOTAL_WIDTH_RX - FRAC_WIDTH_RX
PHASE = 3
SEED = 0x1AA
def main():

	#VARIABLES
	clock = 0
	enable=1
	reset = 0
	#var prsb9
	prbs9_port_bit_out = 0
	state_current =SEED 
	state_next = SEED
	#var tx
	tx_phase_current = 0
	tx_phase_next = 0
	tx_port_out = DeFixedInt(TOTAL_WIDTH_TX,FRAC_WIDTH_TX)
	tx_enable_flag_next = 0
	tx_enable_flag_current = 0
	conv_full = DeFixedInt(TOTAL_WIDTH_TX,FRAC_WIDTH_TX)

	# filtro tx
	#(rcos_floatx, rcos_floaty) = rcosine(ROLL_OFF, BAUD_RATE, UPSAMPLE, N_BAUD, True)
	rcos_floaty = np.arange(0.0,24.0,1.0)
	rcos = arrayFixedInt(TOTAL_WIDTH_TX, FRAC_WIDTH_TX, rcos_floaty)

	rcos_t = np.transpose(rcos)

	filter_taps = len(rcos)
	tx_memory_current = np.zeros(N_BAUD)
	tx_memory_next = np.zeros(N_BAUD)
	#vectores para almacenar resultados
	prbs9_vect = []
	tx_vect = []
	tx_sim = []

	#filtro rx
	rx_input = 0
	rx_port_out = 0
	rx_memory_current = np.zeros( filter_taps-1 )
	rx_memory_next = np.zeros( filter_taps-1 )	
	rx_vect = []
	rx_enable = 0
	rx_enable_flag_next = 0

	for clock in range (0,SIM_ITER):

		
	#PRSB9
		if (clock % UPSAMPLE) == 0:
			bp()
			if(reset):
				state_next = SEED
			elif (enable):
				prbs9_port_bit_out = (state_current>>8) & 1  #bit generado(wire que vale el bit [0] del shift reg state)
				bit_gen = (state_current ^(state_current>>4)) & 1 #xor
				prbs9_vect.append(prbs9_port_bit_out)
				state_next = ( (state_current >>1 ) | (bit_gen<<8)) # shift + xor en bit [0]
			else:
				state_next = state_current

			

		#TX @always(posedge CLK)
		if (reset):
			tx_memory_next = np.zeros(N_BAUD)
			tx_phase_next = 0
			tx_enable_flag_next = 0	
			#asignar coeff con un for?

		elif(tx_enable_flag_current == 0) and (enable == 1):
			tx_phase_next = 0
			tx_enable_flag_next = enable
			tx_memory_next = tx_memory_current
		else:
			tx_phase_next = tx_phase_current + 1
			tx_enable_flag_next = tx_enable_flag_current
			if tx_enable_flag_current	and (tx_phase_current == UPSAMPLE - 1):
				tx_phase_next = 0
				tx_memory_next = np.roll(tx_memory_current, 1)
				tx_memory_next[0] = prbs9_port_bit_out #asigno la salida del modulo prbs9
				
		#Convolucion p/ transmision @always *
		if tx_enable_flag_current :
			conv_full = conv_tx(rcos, tx_memory_current,tx_phase_current,UPSAMPLE)
		
	
			#CUIDADO
			tx_port_out = conv_full	
			rx_input = tx_port_out

			tx_vect.append(conv_full.fValue)	
			



		#RX @always(posedge CLK)
	

		if(reset):
			rx_memory_next = np.zeros(filter_taps-1)
			rx_phase_next = 0
			rx_enable = 1

		elif(rx_enable):
			rx_memory_next = rx_memory_current
			(mem, rx_port_out) = conv_rx(rcos_t, rx_memory_current, rx_input)
			rx_memory_next = np.copy(mem)
			rx_vect.append(rx_port_out.fValue)


		#BER




		#ACTUALIZACION REGISTROS
		#prbs9 reg
		state_current = np.copy(state_next)
		
		#tx reg
		tx_port_out = conv_full
		tx_phase_current = tx_phase_next
		tx_memory_current = np.copy(tx_memory_next)
		tx_enable_flag_current = tx_enable_flag_next
		
		#rx reg
		rx_memory_current = np.copy(rx_memory_next)


	bp()	
	plt.figure(1)
	plt.grid()
	plt.title('TX')
	plt.stem(tx_vect)
	plt.show()


#PLOTS


def print_fixed(vect,titulo):
	aux = []
	for i in range(0,len(vect)):
		aux.append(vect[i].fValue)
	plt.figure(1)
	plt.grid()
	plt.title(titulo)
	plt.plot(aux)
	plt.show()
	return
def fix_to_float(vect):
	fvect = np.zeros(len(vect))
	for i in range(0,len(vect)-1):
		fvect[i]=vect[i].fValue
	return fvect
def conv_tx(filtro,signal,phase,upsample):
	conv_full = DeFixedInt(TOTAL_WIDTH_TX,FRAC_WIDTH_TX)
	conv_full.value = 0.0
	f = DeFixedInt(11,2)
	conv_full.value = 0.0
	for i in range(0 , len(signal) ):
		
		if(signal[i] == 0.0):
			conv_full = conv_full + filtro[i*upsample + phase]
		else :
			conv_full = conv_full - filtro[i*upsample + phase]			
	f.value = conv_full.fValue
	return f
def conv_rx(filtro,signal,sample):
	mem = np.copy(signal)
	mem[0] = (sample * filtro[len(signal)])
	for i in range (1,len(signal)):
		mem[i] = ( sample * filtro[len(signal)-i] ) + signal[i-1]

	out = mem[len(signal)-1] + ( filtro[len(signal)] * sample )	
	
	return (mem,out)		
if __name__ == '__main__':
		main()	