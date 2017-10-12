
import RPi.GPIO as GPIO # always needed with RPi.GPIO
import time
import socket
import cv2
import numpy



SERVER_ADDRESS = ''
SERVER_PORT = 22222


# Create the socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_ADDRESS, SERVER_PORT))
s.listen(5)


print("Listening on address %s. Kill server with Ctrl-C" %
      str((SERVER_ADDRESS, SERVER_PORT)))

# Now we have a listening endpoint from which we can accept incoming
# connections. This loop will accept one connection at a time, then service
# that connection until the client disconnects. Lather, rinse, repeat.
while True:
    
    
    c, addr = s.accept()
    print("\nConnection received from %s" % str(addr))
    
    FM_A = 26
    FM_B = 19
    BM_A = 13
    BM_B = 5
    F_PWM_PIN = 20
    B_PWM_PIN = 16
    



    #GPIO SETUP
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(FM_B, GPIO.OUT)
    GPIO.setup(FM_A, GPIO.OUT)
    GPIO.setup(F_PWM_PIN, GPIO.OUT)
    GPIO.setup(BM_A, GPIO.OUT)
    GPIO.setup(BM_B, GPIO.OUT)
    GPIO.setup(B_PWM_PIN, GPIO.OUT)

    F_PWM = GPIO.PWM(F_PWM_PIN, 1000)
    B_PWM = GPIO.PWM(B_PWM_PIN, 1000)
    GPIO.output(B_PWM_PIN,GPIO.LOW)
    GPIO.output(F_PWM_PIN,GPIO.LOW)
     

    F_PWM.start(80)  
    B_PWM.start(60)
 
   # B_PWM.ChangeDutyCycle(30)  

    while True:
        
        B_PWM.ChangeDutyCycle(60) 
       
        data = c.recv(2048)
        if not data:
            print("End of file from client. Resetting")
            break

        # Decode the received bytes into a unicode string using the default
        # codec. (This isn't strictly necessary for python2, but, since we will
        # be encoding the data again before sending, it works fine there too.)
        data = str(data.decode())
        

        print("Received '%s' from client" % data)
        AY = int(data[0:3])
        BX = int(data[3:])
        
        
        if AY < 160:
                GPIO.output(BM_A,GPIO.HIGH)
                GPIO.output(BM_B,GPIO.LOW)
                
                print("FRONT")
        elif AY > 240:
                
                GPIO.output(BM_A,GPIO.LOW)
                GPIO.output(BM_B,GPIO.HIGH)
                print("BACK")
                
        else:
                GPIO.output(BM_A,GPIO.LOW)
                GPIO.output(BM_B,GPIO.LOW)
                print("NO F/B")

        if BX < 160:
                GPIO.output(FM_A,GPIO.HIGH)
                GPIO.output(FM_B,GPIO.LOW)
                B_PWM.ChangeDutyCycle(60) 
                print("L")
        elif BX > 240:
                
                GPIO.output(FM_A,GPIO.LOW)
                GPIO.output(FM_B,GPIO.HIGH)
                B_PWM.ChangeDutyCycle(60) 
                print("R")
        else :
                GPIO.output(FM_A,GPIO.LOW)
                GPIO.output(FM_B,GPIO.LOW)
                print("NO L/R")



        

        # See above
        data ="200"
        data = data.encode()

        # Send the modified data back to the client.
        
        c.send(data)
        
    F_PWM.stop()            # stop the PWM output
    B_PWM.stop()     
    c.close()
          # stop the PWM output
    GPIO.cleanup()
    
 
 
 

