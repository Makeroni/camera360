 Camera 360
=================================================

This project allows to control a rotatory platform and a camera to take fotos around an object.

The user interface is written in Python. 
It takes the user inputs as the name of the project or the number of pictures to take from each object.
It communicates with arduino in order to start rotating the platform.
When the platform has rotated, arduino communicates with Python.
Then python calls to gphoto program who will take a picture of the object.
The program will continue until it takes the desired number of pictures


Installation
----------------------
Install Python
Install Arduino IDE
Compile gphoto

Windows version can be downloaded here
http://code.google.com/p/scan-manager/downloads/detail?name=gphoto-2.4.14-win32-build2.zip&can=2&q=

 "You'll need to install a special driver for each USB camera you want to use with it (and remove the driver if you want to use it with other software). Download the latest binary version of libusb-win32 from here http://sourceforge.net/projects/libusb-win32/, unzip it somewhere, and run ./bin/inf-wizard.exe, select your camera and when you're finished click the "Install" button. You can roll back the drivers for you camera if you no longer want to use it with gphoto2 by using the Device Manager on Windows (see Control Panel -> System)."


Use
----------------------

Connect the camera via USB
Connect Arduino and load the scketch (it will start listening the serial port)
Run the pyhon program and follow the comand line instructions
Enjoy!



Contribute
----------------------

TODO


Any problems?
-------------
Feel free to [write an issue](https://github.com/Makeroni/camera360/issues) if you have any questions or problems.


Copyright and license
---------------------

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later version.
