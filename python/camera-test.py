import os, datetime
import glob
import sys
import time
from subprocess import PIPE, Popen

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

# Export gphoto2 paths
os.putenv("CAMLIBS", "C:\\gphoto\\camlibs")
os.putenv("IOLIBS", "C:\\gphoto\\iolibs")

# Run gphoto2 in shell mode
proc = Popen(['C:\\gphoto\\gphoto2.exe', '--shell'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
sys.stdout.write("\r>> Starting gphoto2")
sys.stdout.flush()

while 1:
  # Capture photo and wait until finished
  sys.stdout.write("\r>>                              ")
  sys.stdout.write("\r>> Capturing image ")
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
  pic2 = "camera-test.jpg"
  if os.path.exists(pic2):
    os.remove(pic2)
  os.rename(pic1, pic2)
  # Run windows viewer
  #os.system('%SystemRoot%\\System32\\rundll32.exe "%ProgramFiles%\\Windows Photo Viewer\\PhotoViewer.dll", ImageView_Fullscreen '+os.path.join(os.getcwd(), pic2))
  os.system('%SystemRoot%\\System32\\rundll32.exe C:\\WINDOWS\\System32\\shimgvw.dll,ImageView_Fullscreen '+os.path.join(os.getcwd(), pic2))
