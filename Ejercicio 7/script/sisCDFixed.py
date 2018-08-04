import numpy as np
import matplotlib.pyplot as plt
from tool.DSPtools import *
from tool._fixedInt import  *
from pdb import set_trace as bp

########################################--DEFINE--######################################

ROLL_OFF = 0.5
UPSAMPLE = 4
SENT_LENGHT = 512
ITER = 10
N_BAUD = 6
BAUD_RATE = 1.0/100000000
NBI_TX = 12																						#Numero digitos enteros fp para tx
NBF_TX = 10																						#Numero digitos fraccionarios fp para tx
NBI_RX = 15																						#Numero digitos enteros fp para rx
NBF_RX = 13																						#Numero digitos fraccionarios fp para rx
phase = 3																						#Fase, varia de 0 a 3, para probar valores en el calculo de BER
i_sw0 = 1
i_sw1 = 1

########################################--MAIN--########################################
def main():

	yn=0.0
	start = 0x1AA
	bit_gen = start
	state = start
	delay = 0
	ber = 0.1

	#Filtro tx/rx en punto flotante
	(rcosx_ft , rcosy_ft) = rcosine(ROLL_OFF, BAUD_RATE, UPSAMPLE, N_BAUD, True)

	#Filtro tx/rx en punto fijo
	rcosx_fp_tx = arrayFixedInt(NBI_TX, NBF_TX, rcosx_ft)
	rcosy_fp_tx = arrayFixedInt(NBI_TX, NBF_TX, rcosy_ft)									#Vector de coeficientes del filtro tx

	rcosx_fp_rx = arrayFixedInt(NBI_RX, NBF_RX, rcosx_ft)
	rcosy_fp_rx = arrayFixedInt(NBI_RX, NBF_RX, rcosy_ft)									#Vector de coeficientes del filtro rx


	#Inicializacion de vectores de senial y transmision en  0
	signal = np.zeros(UPSAMPLE*N_BAUD)
	tx_plot = np.zeros(SENT_LENGHT*UPSAMPLE)
	rx_plot = np.zeros(SENT_LENGHT*UPSAMPLE)
	rx_ds = np.zeros(UPSAMPLE)																
	decided_vector = np.zeros(SENT_LENGHT)													#Vector de simbolos decididos en p.fijo (salida de slicer)
	decided_vector_ft = np.zeros(SENT_LENGHT)												#Vector de simbolos decididos en flotante (salida de slicer)
	sent_vector = np.zeros(SENT_LENGHT)


	#Inicializacion variables float
	signal_ft = np.zeros(UPSAMPLE*N_BAUD)
	tx_ft = np.zeros(SENT_LENGHT*UPSAMPLE)
	rx_ft = np.zeros(SENT_LENGHT*UPSAMPLE)


	#Conversion a fp
	signaltx_fp = arrayFixedInt(NBI_TX, NBF_TX, signal)										#Memoria del filtro transmisor fixed
	signalrx_fp = arrayFixedInt(NBI_RX, NBF_RX, signal)										#Memoria del filtro receptor fixed
	signaltx_ft = np.zeros(25)																#Memoria del filtro transmisor float
	signalrx_ft = np.zeros(25)																#Memoria del filtro receptor float
	tx_plot = arrayFixedInt(NBI_TX, NBF_TX, tx_plot)										#Vector donde se almacena el resultado de la convolucion en la tx en punto fijo
	rx_plot = arrayFixedInt(NBI_RX, NBF_RX, rx_plot)										#Vector donde se almacena el resultado de la convolucion en la rx en punto fijo
	rx_ds_fp = arrayFixedInt(NBI_RX, NBF_RX, rx_ds)											#Vector donde almaceno 4 recepciones punto fijo
	rx_ds_ft = rx_ds 																		#Vector donde almaceno 4 recepciones flotante
	tx_plot_ft = np.zeros(SENT_LENGHT*UPSAMPLE)												#Vector donde se almacena el resultado de la convolucion en la tx en flotante
	rx_plot_ft = np.zeros(SENT_LENGHT*UPSAMPLE)												#Vector donde se almacena el resultado de la convolucion en la rx en flotante	


	for clock in range(0, SENT_LENGHT*UPSAMPLE):

		if ((clock % 4) == 0 and i_sw0):													#Cada 4 ciclos de clock, genero un nuevo simbolo con el PRSB9
			bit_gen = (state^(state>>4)) & 1
			state = ((state>>1) | (bit_gen<< (9-1)))
			if bit_gen == 0: 
				symbol = 1.0
			else :
				symbol = -1.0


			sent_vector[clock/4] = symbol
			symbol_fp = DeFixedInt(NBI_TX,NBF_TX)													
			symbol_fp.value = symbol
			signaltx_fp[0] = symbol_fp														#Agrego el simbolo generado a la memoria del filtro tx en p.fijo
			signaltx_ft[0] = symbol 														#Agrego el simbolo generado a la memoria del filtro tx en flotante


	#######################TRANSMISION#########################
		if i_sw0:
			tx_fp = convolucion_tx(rcosy_fp_tx, signaltx_fp)  								#Convolucion para transmision en p.fijo
			tx_plot[clock] = tx_fp

			tx_ft = sum(rcosy_ft * signaltx_ft)												#Convolucion para transmision en flotante
			tx_plot_ft[clock] = tx_ft 								

			signaltx_fp = usample(signaltx_fp)												#Funcion encargada de realizar el upsampling en p.fijo
			signaltx_ft = usampleft(signaltx_ft)											#Funcion encargada de realizar el upsampling en flotante

    #######################RECEPCION###########################

		if i_sw1:		
			signalrx_fp = np.roll(signalrx_fp, 1)											#Convolucion para recepcion en p.fijo
			signalrx_fp[0] = tx_fp
			rx_fp = convolucion_rx(rcosy_fp_rx, signalrx_fp)									
			rx_plot[clock] = rx_fp 															

			signalrx_ft = np.roll(signalrx_ft, 1)											#Convolucion para recepcion en flotante
			signalrx_ft[0] = tx_ft
			rx_ft = sum(rcosy_ft * signalrx_ft)
			rx_plot_ft[clock] = rx_ft
			
    		#Vector para almacenar 4 recepciones y variar la fase para el BER
			rx_ds_fp[clock%4] = rx_fp
			rx_plot[clock] = rx_fp

			rx_ds_ft[clock%4] = rx_ft
			rx_plot_ft[clock] = rx_ft

    		#Downsample para p.fijo y flotante
			if (clock % 4) == 0:
				#p.fijo
				decided_symbol = slicer(rx_ds_fp, phase)
				decided_vector[clock/4] = decided_symbol

				#flotante
				decided_symbol_ft = slicerft(rx_ds_ft, phase)
				decided_vector_ft[clock/4] = decided_symbol_ft
	
    #######################CALCULO BER#########################
	ber = sum(np.abs(sent_vector - decided_vector))/2
	delay = 0
	while(ber >20.0):
		delay +=1
		decided_vector = np.roll(decided_vector, -1)
		ber = sum((sent_vector[0:(SENT_LENGHT-delay)] != decided_vector[0:(SENT_LENGHT-delay)])*1)
		print ber	


	#######################CALCULO SNR#########################

	#para TX
	txplotinft = fp_to_float(tx_plot)
	diff1 = txplotinft - tx_plot_ft
	snr_tx = 10*np.log10(sum(txplotinft**2)/sum(diff1**2))

	#para RX
	rxplotinft = fp_to_float(rx_plot)
	diff2 = rxplotinft - rx_plot_ft
	snr_rx = 10*np.log10(sum(rxplotinft**2)/sum(diff2**2))

	print 'snr(TX,RX)=({tx} ; {rx})[dB]'.format(tx=snr_tx, rx=snr_rx) 

	bp()

    #######################--PLOTEO--##########################
#	print_fixed_to_float(tx_plot, "senal enviada en P.Fijo",1)								#Ploteo de la senial a transmitir en p.fijo
#	print_fixed_to_float(rx_plot, "senal recibida en P.Fijo",2)								#Ploteo de la senial recibida en p.fijo
#	print_float(tx_plot_ft, "senal enviada en Flotante",3)									#Ploteo de la senial enviada en flotante
#	print_float(rx_plot_ft, "senal recibida en Flotante",4)									#Ploteo de la senial recibida en flotante

	float_tx_plot = fp_to_float(tx_plot)
	float_rx_plot = fp_to_float(rx_plot)

	eyediagram(float_tx_plot, 4, 2, BAUD_RATE)
	eyediagram(float_rx_plot, 4, 2, BAUD_RATE)
	eyediagram(tx_plot_ft, 4, 2, BAUD_RATE)
	eyediagram(rx_plot_ft, 4, 2, BAUD_RATE)
	plt.show()

########################################--TX-CONVOLVE--###################################
def fp_to_float(vect):
	aux = np.zeros(SENT_LENGHT*UPSAMPLE)
	for ctr in range(0, len(vect)-1):
		aux[ctr] = vect[ctr].fValue

	return aux
########################################--TX-CONVOLVE-P.Fijo-#############################
def convolucion_tx(vect1, vect2):
	yn = DeFixedInt(NBI_TX, NBF_TX) 
	yn.value = 0.0
	for ctr in range(0, len(vect2)-1):
		if(vect2[ctr].fValue != 0.0):
			if(vect2[ctr].fValue == 1):
				yn.value = (yn+vect1[ctr]).fValue
			else:
				yn.value = (yn-vect1[ctr]).fValue 
	return yn
########################################--UPSAMPLING-P.Fijo-##############################
def usample(vect):
	cero = DeFixedInt(NBI_TX, NBF_TX)
	cero.value = 0.0
	vect = np.roll(vect, 1)	
	vect[0] = cero
	return vect
########################################--UPSAMPLING-Flotante-############################
def usampleft(vect):
	vect = np.roll(vect, 1)	
	vect[0] = 0.0
	return vect
########################################--RX-CONVOLVE-P.Fijo-#############################
def convolucion_rx(vect1, vect2):
	yn = DeFixedInt(NBI_RX, NBF_RX) 
	yn.value = 0.0

	for ctr in range(0, len(vect2)-1):
		yn.value = (yn + vect1[ctr]*vect2[ctr]).fValue
	return yn
########################################--SLICER-P.Fijo-##################################
def slicer(vect, phase):
	if(vect[phase].fValue >= 0.0):
		return 1.0
	else:
		return -1.0
########################################--SLICER-Flotante-################################
def slicerft(vect, phase):
	if(vect[phase] >= 0.0):
		return 1.0
	else:
		return -1.0
########################################--PLOTEO-P.Fijo-##################################
def print_fixed_to_float(vect, title, N):
	aux = []
	for i in range(0,len(vect)-1):
		aux.append(vect[i].fValue)
	plt.figure(N)
	plt.grid()
	plt.title(title)
	plt.plot(aux)
	return

########################################--PLOTEO-Flotante-#################################
def print_float(vect, title, N):
	plt.figure(N)
	plt.grid()
	plt.title(title)
	plt.plot(vect)
	return

if __name__ == '__main__':
	   main()