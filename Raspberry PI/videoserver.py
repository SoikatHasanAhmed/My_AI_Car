#!/usr/bin/python
import socket
import cv2
import pickle

TCP_IP = ''
TCP_PORT = 5001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
capture.set(cv2.CAP_PROP_FPS, 30)

while True:
	s.listen(True)
	conn, addr = s.accept()
	
	ret, frame = capture.read()
	encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
	result, imgencode = cv2.imencode('.jpg', frame, encode_param)
	AAdata = pickle.dumps(imgencode)
	conn.send(str(len(AAdata)).zfill(16).encode())
	conn.send(AAdata)
	conn.close();

s.close()



