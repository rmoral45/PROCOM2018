import time
import serial

ser=serial.serial_for_url('loop://', timeout=1)
ser.isOpen()
ser.timeout=5
ser.flushInput()
ser.flushOutput()
print(ser.timeout)
comandos_validos =[]
comandos_validos.append("0R")
comandos_validos.append("1R")
comandos_validos.append("2R")
comandos_validos.append("3R")
comandos_validos.append("0G")
comandos_validos.append("1G")
comandos_validos.append("2G")
comandos_validos.append("3G")
comandos_validos.append("0B")
comandos_validos.append("1B")
comandos_validos.append("2B")
comandos_validos.append("3B")
comandos_validos.append("exit")


while True :
    print 'Ingrese un comando, indicando numero de LED (0-3) y color (R-G-B) \n'
    frame = []
    data_size = 0
    input = raw_input("ToSend: ")
    if input == 'exit':
        ser.close()
        print 'Comunicacion finalizada por el usuario.'
        exit()
    elif input in comandos_validos:
        #-----------envio--------------------------------
        #bits fijos de trama
        frame.append(0xA0)
        #Siempre enviaremos y recibiremos tramas cortas.
        frame[0] |= 0x10
        #Indicamos el tamanio de la trama
        data_size =( len(input) & 0x0F)
        frame[0] |= data_size
        #agrego L.HIGH y L.LOW
        frame.append(0x00)
        frame.append(0x00)
        #El device nos va a indicar el numero de led para prender, o el numero de switch que leo. 
        if(input[0] == '0'):
            frame.append(0x00)
        elif(input[0] == '1'):
            framen.append(0x01)
        elif(input[0] == '2'):
            frame.append(0x02)
        else
            frame.append(0x03)
        #agrego los datos. En data, almacenamos la letra indicada para el usuario, la cual indica el color a prender
        if(input[1] == 'R'):
            data = 0x0A
        elif(input[1] == 'G'):
            data = 0x0B
        elif(input[1] == 'B'):
            data = 0x0C         
        frame.append(data)
        #agrego fin de trama    
        frame.append(0x40)
        frame[-1] |= (frame[0] & 0x1F )
        #Escribo el puerto para transmision
        for f in frame:
            ser.write(chr(f))
 
                    
    #-----------------recepcion-------------------------
        #leo los primeros 4 bytes(cabecera)
        header = ser.read(4) 
        header = map(ord,header)
        print "cabecera",header
        data_size = (header[0] & 0x0F)
        #leo datos
        recv = ser.read(data_size)
        if len(recv) != data_size:
            print "se recibieron menos datos"
        frame_end = ord(ser.read(1))
        if (frame_end & 0x1F) != (header[0] & 0x1F):
            print 'Error de recepcion \n'
        if recv == 'calculadora' :
            print "ejecuto calculadora"
            calc()
        elif recv == 'graficar':
            print "ejecuto graficar"   

    else:
        print 'Comando invalido, intente nuevamente \n'