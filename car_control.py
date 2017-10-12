import pygame
import socket


SERVER_ADDRESS = '192.168.0.4'
SERVER_PORT = 22222

ay ="100"
bx = "100"

pygame.display.init()
pygame.joystick.init()
pygame.joystick.Joystick(0).init()


# Create the socket
c = socket.socket()

# Connect to the server. A port for the client is automatically allocated
# and bound by the operating system
c.connect((SERVER_ADDRESS, SERVER_PORT))


# Prints the values for axis0
while True:
        pygame.event.pump()

        bx = str(int((pygame.joystick.Joystick(0).get_axis(3)*100)+200))
        ay = str(int((pygame.joystick.Joystick(0).get_axis(1)*100)+200))
        data = ay + bx
        # Convert string to bytes. (No-op for python2)
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