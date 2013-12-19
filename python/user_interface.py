import serial
#import time
import os
#from subprocess import call

arduino_port = input("Puerto Arduino [COM5]?: ")
if arduino_port == "":
    arduino_port = "COM5"

ser = serial.Serial(arduino_port, 9600)
#Arduino resets when you open the serial communication~, wait 2 seconds
#time.sleep(2)

nombre_proyecto = input("Nombre del proyecto?: ")

num_fotos = int(input("Numero de fotos por vuelta?: "))
x = 0
#initialize camera
#call(['D:\estudio\electronica\camara_CSIC\gphoto\win32\gphoto2.bat'])

while x < num_fotos:
    #Say Arduino to rotate_on
    comando = "rotate_on " + str(round(200/num_fotos))
    ser.write(comando.encode('utf-8'))
    #Wait until arduino writes rotate_off
    arduino_msg = ser.readline()
    if arduino_msg == "rotate_off\r\n".encode('utf-8'):
        os.chdir('D:\estudio\electronica\camara_CSIC\gphoto\win32')
        #os.startfile("gphoto2_capture.bat")
        #call(['D:\estudio\electronica\camara_CSIC\gphoto\win32\gphoto2_capture.bat'])
        #os.system("gphoto2_capture.bat")
        #os.system("gphoto2.bat")
        os.putenv("CAMLIBS", "camlibs")
        os.putenv("IOLIBS", "iolibs")
        os.system('gphoto2.exe --capture-image-and-download --filename \"../../fotos/' +nombre_proyecto +'/foto_' +str(x).zfill(2) +'.jpg\" ')
        print("echo rotate_off")
        x = x + 1
#Close serial connection
ser.close()

print("GAME OVER")


