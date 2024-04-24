##################################################################################################
# Pi Camera Code
##################################################################################################

import cv2
from picamera2 import Picamera2
import numpy as np
from pyzbar.pyzbar import decode

piCam = Picamera2()
piCam.preview_configuration.main.size=(640, 360)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.align()
piCam.start()

while True:
    frame=piCam.capture_array()

    for barcode in decode(frame):
        print(barcode.data)
        mydata = barcode.data.decode('utf-8')
        print(mydata)
        points = np.array([barcode.polygon], np.int32)
        points = points.reshape((-1,1,2))
        cv2.polylines(frame, [points], True, (255, 0, 255), 5)
        
        points2 = barcode.rect
        # show text on the image
        cv2.putText(frame, mydata, (points2[0], points2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255))
                    
    cv2.imshow("piCam", frame)
    if cv2.waitKey(1)==ord('q'):
        break

cv2.destroyAllWindows()


####################################################################################################
# End Pi Camera
######################################################################################################


#####################################################################################################
# RFID Scanning Code
#####################################################################################################


import RPi.GPIO as GPIO
import socket
import time
from mfrc522 import SimpleMFRC522

# Set up the socket for communication (replace 'your_laptop_ip' and 'your_port' with actual values)

host, port = '192.168.1.188', 8000 #Wongani's laptop

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(s)
s.connect((host, port))

reader = SimpleMFRC522()

try:
	while True:
		print('place card on reader')
		id, text = reader.read()
		print('ID: ', id)
		print('Text: ', text)
		data = f"{id}"
		s.sendall(data.encode('utf-8'))
		time.sleep(2)
except KeyboardInterrupt:
	print("Exiting...")
finally:
	GPIO.cleanup()
	s.close()

