import cv2
import socket
from alexnet_model import alexnet
from collect_image_TCP import getIMG,showIMG


WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 10
MODEL_NAME = 'MY_AI_CAR.model'
t_time = 0.09
model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)


#server to send car command
SERVER_ADDRESS = '192.168.0.4'
SERVER_PORT = 22222
ay ="100"
bx = "100"
c = socket.socket()

# Connect to the server. A port for the client is automatically allocated
# and bound by the operating system
c.connect((SERVER_ADDRESS, SERVER_PORT))


while True :

    image = showIMG(getIMG())
    image = cv2.resize(image, (160, 120))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    prediction = model.predict([image.reshape(WIDTH, HEIGHT , 1)])[0]
    print(prediction)

    turn_thresh =.36000000

    if  prediction[0] > turn_thresh and prediction[2] < turn_thresh:
        AY = '150'
        BX ='150'
        print('turn left')
    elif  prediction[0]< turn_thresh and prediction[2] > turn_thresh:
        BX='250'
        AY = '150'
        print('turn right')
    else:
        BX = '200'
        AY = '150'
        print('F')

    data = AY+BX
    print('send data  ' + data)
    data = data.encode()
    # Send data to server
    c.send(data)

    # Receive response from server
    data = c.recv(2048)
    if not data:
        print("Server abended. Exiting")
        break
    print(data)

c.close()