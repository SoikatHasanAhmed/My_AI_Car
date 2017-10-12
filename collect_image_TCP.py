#!/usr/bin/python
import socket
import cv2
import pickle

TCP_IP = '192.168.0.3'
TCP_PORT = 5001

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def getIMG():
	sock = socket.socket()
	sock.connect((TCP_IP, TCP_PORT))


	stringData = sock.recv(16)
	length = stringData.decode()
	stringData = recvall(sock, int(length))
	sock.close()
	data = pickle.loads(stringData)
	return data


def showIMG(data):
        decimg = cv2.imdecode(data, 1)
        return decimg
