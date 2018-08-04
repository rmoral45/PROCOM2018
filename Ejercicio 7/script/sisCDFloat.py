import numpy as np
import matplotlib.pyplot as plt
from tool.DSPtools import *

ROLL_OFF = 0.5
UPSAMPLE = 4
SENT_LENGHT = 512
N_BAUD = 6
BAUD_RATE = 1.0/100000000
OVERSAMPLE = 4


def simfloat(symbols):

	#genero senial aleatoria
#	parte_re = np.random.randint(0,2,SENT_LENGHT)*2-1
#	parte_im = np.random.randint(0,2,SENT_LENGHT)*2-1
	parte_re = symbols
	parte_im = symbols

	tx_convol = 0.0

	#UPSampling 
	tx_re = np.zeros(UPSAMPLE*SENT_LENGHT)
#	parte_im_up = np.zeros(UPSAMPLE*SENT_LENGHT)

#	index = range(0,SENT_LENGHT*UPSAMPLE,UPSAMPLE)	#generacion de vector de indices desde 0 a 1024 con un paso de 4
	
#	parte_re_up[index] = parte_re 					#en el vector de 0, inserto 1 o -1 cada index veces
#	parte_im_up[index] = parte_im

	#filtro tx/rx
	(rcosx, rcosy) = rcosine(ROLL_OFF, BAUD_RATE, OVERSAMPLE, N_BAUD, True)
	#rta en frecuencia de filtro tx/rx
#	H,A,F = resp_freq(rcosy, 1./BAUD_RATE, SENT_LENGHT)
	#plot de la rta en frec. filtro tx/rx
#	plt.figure(1)
#	plt.title('Filtro tx/rx')
#	plt.plot(rcosx,rcosy)
#	plt.show()
#	plt.figure(2)
#	plt.title('Rta en Frecuencia filtro tx/rx')
#	plt.grid()
#	plt.semilogx(F, 10*np.log(H))
#	plt.show()


	#enviar senial
#	tx_parte_re = np.convolve(rcosy, parte_re_up, 'same')

	#convolucion
	for ctr in range(0, len(rcosy)):
		tx_convol += rcosy[ctr] * parte_re_up[ctr] 

#	tx_parte_im = np.convolve(rcosy, parte_im_up, 'same')
	#plot de bits transmitidos
#	plt.figure(3)
#	plt.grid()
#	plt.title('tx_parte_re')
#	plt.plot(tx_parte_re)
#	plt.show()

	#plot diagrama de ojo de filtro tx
#	eyediagram(tx_parte_re, 4,2,UPSAMPLE)


	#recibir senial
#	rx_parte_re = np.convolve(rcosy, tx_parte_re,'same')
#	rx_parte_im = np.convolve(rcosy, tx_parte_im,'same')
	#plot de bits recibidos
#	plt.figure(5)
#	plt.grid()
#	plt.title('senal recibida')
#	plt.plot(rx_parte_re)
#	plt.show()


	#plot diagrama de ojo de filtro tx
#	eyediagram(rx_parte_re, 4, 2, UPSAMPLE)

	#DOWNSampling
#	rx_re_down = rx_parte_re[index]					#Elimino los ceros de la senial recibida, sabiendo que hay informacion cada index veces
#	rx_im_down = rx_parte_im[index]

	#deteccion por umbral, si es menor a 0, recibi un -1 si no un 1
#	decided_re = (rx_re_down>=0)*2-1
#	decided_im = (rx_im_down>=0)*2-1

	#calculo de BER
#	re_diff = (decided_re - parte_re)/2				
#	im_diff = (decided_im - parte_im)/2
	
	#Ploteo de constelacion
#	plt.figure(6)
#	plt.title('Constelacion')
#	plt.stem(decided_re,decided_im)
#	plt.show()

#	BER = sum(re_diff) + sum(im_diff)
#	print 'BER' , BER

#if __name__ == '__main__':
#    main()
