import serial
import os, datetime
import glob
import sys
import time
from subprocess import PIPE, Popen
import _winreg as winreg
import itertools

# Print logo
print ""
print ""
print "              ::    ::                                          :::"
print "              @@@  ;@@   @@@  ,@@  @@'@@@@@ @@@@@   @@@ @@@  @@ @@@"
print "              @@@  @@@  @@@@  .@@  @@ @@@@@ @@+@@@ @@ @@@@@: @@ @@@"
print "              @@@@:@@@  @@@@@ .@@ @@  @@.   @@` @@ @@ @@@@@@ @@ @@#"
print "              @#@@@#@@  @,@@@ .@@#@.  @@+@: @@`+@@ @@:@#@@@@@@@ @@#"
print "              @#@@@.@@ +@ ,@@ .@@@@@  @@:@  @@@@@`  @@@ @@`@@@@ @@#"
print "              @# @,.@@ @@@@@@@.@@ @@+ @@`   @@`+@@@     @@ '@@@ @@#"
print "              @# # ,@@ @@  @@@.@@ @@@ @@@@@`@@` +@@@@@@+@@  @@@ @@#"
print "              @@   ,@@ @@  @@@.@@  @@;@@@@@ @@.   @@@@@#@@   @@ @@@"
print ""
print "                               Camera 360 v1.0                     "
print ""
print ""

# Select serial port
port = ""
path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
try:
  key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
except WindowsError:
  raise IterationError

for i in itertools.count():
  try:
    val = winreg.EnumValue(key, i)
    port = str(val[1])
  except EnvironmentError:
    break
if port == "":
  raw_input(">> No serial ports found")
  exit()
print ">> Using " + port + " for Arduino communication"

# Open serial port
try:
  ser = serial.Serial(port, 9600)
except Exception, e:
  raw_input(">> Error opening serial port")
  exit()

# Request capture description
desc = raw_input(">> Project description: ")
	
# Request number of photos
photos = 0
while not photos > 0:
  input = raw_input(">> Number of images: ")
  if input.isdigit():
    photos = int(input)

# Create folder
now = datetime.datetime.now()
dir = os.path.join(os.getcwd(), now.strftime('%Y-%m-%d_%H-%M-%S'))
os.makedirs(dir)
print ">> Working folder: " + os.path.basename(dir)

# Export gphoto2 paths
os.putenv("CAMLIBS", "C:\\gphoto\\camlibs")
os.putenv("IOLIBS", "C:\\gphoto\\iolibs")

# Run gphoto2 in shell mode
proc = Popen(['C:\\gphoto\\gphoto2.exe', '--shell'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
sys.stdout.write("\r>> Starting gphoto2")
sys.stdout.flush()

# Write info.txt
f = open(os.path.join(dir, "info.txt"), 'w')
f.write('Description: '+desc+'\nImages: '+str(photos)+'\nDate: '+now.strftime('%Y/%m/%d %H:%M:%S')+'\n')
f.close()

# Enable motor driver
msg = ""
cmd = "RQen"
while msg != "RQen_srv\r\n".encode('utf-8'):
  ser.write(cmd.encode('utf-8'))
  msg = ser.readline()
msg = ""
while msg != "GRen\r\n".encode('utf-8'):
  msg = ser.readline()

for i in range(photos):
  # Capture photo and wait until finished
  sys.stdout.write("\r>>                              ")
  sys.stdout.write("\r>> Capturing image %d " %(i+1))
  sys.stdout.flush()
  print>> proc.stdin, "capture-image-and-download"
  while True:
    sys.stdout.write(".")
    sys.stdout.flush()
    line = proc.stdout.readline()
    if line.startswith("New file"):
      time.sleep(2)
      break
  # Rename file
  pic1 = max(glob.iglob('*'), key=os.path.getctime)
  pic2 = '%03d.jpg'%(i+1,)
  os.rename(pic1, os.path.join(dir, pic2))
  # Rotate motor
  msg = ""
  while msg != "RQstp_srv\r\n".encode('utf-8'):
    cmd = "RQstp" + str(round(200/photos))
    ser.write(cmd.encode('utf-8'))
    msg = ser.readline()
  msg = ""
  while msg != "GRstp\r\n".encode('utf-8'):
    msg = ser.readline()
  
# Disable motor driver
msg = ""
cmd = "RQdis"
while msg != "RQdis_srv\r\n".encode('utf-8'):
  ser.write(cmd.encode('utf-8'))
  msg = ser.readline()
msg = ""
while msg != "GRdis\r\n".encode('utf-8'):
  msg = ser.readline()

# Close serial port
ser.close()

sys.stdout.write("\r>>                              ")
sys.stdout.write("\r>> Capture finished\n")
sys.stdout.write("\r>> ")
sys.stdout.flush()
raw_input("")

