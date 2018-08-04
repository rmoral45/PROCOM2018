import numpy as np
import matplotlib.pyplot as plt
from tool.DSPtools import *
from tool._fixedInt import  *
from pdb import set_trace as bp

ROLL_OFF = 0.5
UPSAMPLE = 4
SENT_LENGHT = 256
N_BAUD = 6
BAUD_RATE = 1.0/100000000
SIM_ITER =1024
def main():
	#var para PBSR9
	start = 0x1AA
	bit_gen = start
	state = start
	n=0
	#tx=DeFixedInt(9,7)
	#tx.value = 0.0
	#var sim
	(rcos_x_float , rcos_y_float) = rcosine(ROLL_OFF, BAUD_RATE, UPSAMPLE, N_BAUD, True)
	rcos_y = arrayFixedInt(9, 12, rcos_y_float)
	#genero vector de prueba
	sig_re = np.zeros(24)
	sig = arrayFixedInt(9, 12, sig_re)
	ceros = np.zeros(SIM_ITER)
	tx_vect = arrayFixedInt(9, 12,ceros)
	for clock in range(0,SIM_ITER):

	#asignaciones p prox ciclo de clock(cada 1 ciclo de clock)

	#PRBS9 (una iteracion cada 4 ciclos de clock)
		if (clock % 4) == 0:
			bit_gen = (state^(state>>4)) & 1
			state = ((state>>1) | (bit_gen<< (9-1)))
			if bit_gen ==0 :
				symbol = 1.0
			else :
				symbol = -1.0
			#agrego el simbolo generado y los ceros		
			fv=DeFixedInt(9,12)
			fv.value=symbol
			sig[0]=fv
			
			'''
			for i in range(1,UPSAMPLE):
				fv.value = 0.0
				sig[i]=fv
			'''	
	#FIR Tx(cada 1 ciclo de clock)
		
		for c in range(0,len(rcos_y_float)-1):
			if c ==  0:
				tx=rcos_y[c] * sig[c]
			else:	
				tx += rcos_y[c] * sig[c]
		tx_vect[clock]=tx	
		
		
	#right shift
		for i in reversed(range(1,len(rcos_y)-1)):
			sig[i] = sig[i-1]
		fv=DeFixedInt(9,12)	
		fv.value = 0.0
		sig[0]=fv
	
	print_fixed_to_float(tx_vect)				

def print_fixed_to_float(vect):
	aux = []
	for i in range(0,len(vect)):
		aux.append(vect[i].fValue)
	plt.figure(1)
	plt.grid()
	plt.title('senal enviada')
	plt.plot(aux)
	plt.show()
	return	

if __name__ == '__main__':
		main()	
