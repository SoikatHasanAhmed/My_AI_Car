#!/usr/bin/python

import cv2
import numpy as np
import pygame
import os
from collect_image_TCP import getIMG,showIMG





def collect_image():
    # gamepad value init
    pygame.display.init()
    pygame.joystick.init()
    pygame.joystick.Joystick(0).init()

    saved_frame = 0
    total_frame = 0

    output = [0, 0, 0]
    file_name = 'training_data.npy'

    if os.path.isfile(file_name):
        print('File exists, loading previous data!')
        training_data = list(np.load(file_name))
    else:
        print('File does not exist, starting fresh!')
        training_data = []


    print('Start collecting images...')
    e1 = cv2.getTickCount()
    frame = 1
    while True:

        image = showIMG(getIMG())
        cv2.imshow("steam",image)
        if cv2.waitKey(25) & 0XFF == ord('q'):
            cv2.destroyAllWindows()
            break
        image = cv2.resize(image, (160, 120))
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        frame += 1
        total_frame += 1

        #gamepad values

        pygame.event.pump()
        BX = int((pygame.joystick.Joystick(0).get_axis(3) * 100) + 200)
        AY = int((pygame.joystick.Joystick(0).get_axis(1) * 100) + 200)

        exit = int(pygame.joystick.Joystick(0).get_button(3))
        # complex orders
        if exit ==0:
            if AY < 160 and BX > 240:
                print("Forward Right")
                output = [0,0,1]
                training_data.append([image, output])
                saved_frame += 1


            elif AY < 160 and BX < 160 :
                print("Forward Left")
                output = [1, 0, 0]
                training_data.append([image, output])
                saved_frame += 1


            elif AY > 240  and BX > 240:
                print("Reverse Right")


            elif AY > 240  and BX < 160 :
                print("Reverse Left")


            # simple orders
            elif  AY < 160:
                print("Forward")
                output = [0, 1, 0]
                training_data.append([image, output])
                saved_frame += 1



            elif AY > 240 :
                print("Reverse")
            elif BX > 240:
                print("Right")
            elif BX < 160:
                print("Left")

        elif exit == 1:
            print('exit')
            print(len(training_data))
            np.save(file_name, training_data)
            break


    e2 = cv2.getTickCount()
            # calculate streaming duration
    time0 = (e2 - e1) / cv2.getTickFrequency()
    print('Streaming duration:', time0)
    print('Total frame:', total_frame)
    print('Saved frame:', saved_frame)
    print('Dropped frame', total_frame - saved_frame)




if __name__ == '__main__':
    collect_image()