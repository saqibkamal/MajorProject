import time
import sys
import RPi.GPIO as GPIO
import requests
import cv2
import numpy as np
import base64
import os
camera_url="http://192.168.43.110:8080/shot.jpg"
server_url="http://192.168.43.185:233"

GPIO_TRIGGER = 16
GPIO_ECHO    = 18
Forward1     = 36
Backward1    = 35
Forward2     = 38
Backward2    = 37

def setup_motors():
    GPIO.setup(Forward1, GPIO.OUT)
    GPIO.setup(Backward1, GPIO.OUT)
    GPIO.setup(Forward2, GPIO.OUT)
    GPIO.setup(Backward2, GPIO.OUT)

def setup_sensors():
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
    GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    setup_motors()
    setup_sensors()

def get_distance():
    GPIO.output(GPIO_TRIGGER, False)
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    

    while GPIO.input(GPIO_ECHO)==0:
      start = time.time()

    while GPIO.input(GPIO_ECHO)==1:
      stop = time.time()

    # Calculate pulse length
    elapsed = stop-start

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distancet = elapsed * 34300

    # That was the distance there and back so halve the value
    distance = distancet / 2

    print(distance)

    return distance

def forward():
    GPIO.output(Forward1, GPIO.HIGH)
    GPIO.output(Forward2, GPIO.HIGH)
    print("Moving Forward")

    
def right(x):
    GPIO.output(Forward1, GPIO.HIGH)
    print("Moving Right")
    time.sleep(x)
    GPIO.output(Forward1, GPIO.LOW)
    
def left(x):
    GPIO.output(Forward2, GPIO.HIGH)
    print("Moving Left")
    time.sleep(x)
    GPIO.output(Forward2, GPIO.LOW)

def stop():
    print("Stopping")
    GPIO.output(Forward1, GPIO.LOW)
    GPIO.output(Forward2, GPIO.LOW)

def get_filename():
    return str(time.strftime("%Y%m%d-%H%M%S"))+".png"

def capture_image():
    print("capture_image ")
    img=requests.get(camera_url)
    img_arr=np.array(bytearray(img.content),dtype=np.uint8)
    imgg= cv2.imdecode(img_arr,-1)
    
    image_name = get_filename()
    cv2.imwrite(image_name,imgg)

    return image_name

def send_image(mimage,limage,rimage):
    
    print("Sending Image")
    
    with open(mimage,"rb") as a:
        main_jpg_as_text=base64.b64encode(a.read())

    with open(limage,"rb") as a:
        left_jpg_as_text=base64.b64encode(a.read())

    with open(mimage,"rb") as a:
        right_jpg_as_text=base64.b64encode(a.read())
    
    image_josn = {"main_image": main_jpg_as_text,"left_image":left_jpg_as_text,"right_image":right_jpg_as_text}

    response = requests.post("{}/predict".format(server_url), json = image_josn)

    #print(response.json())
    print("Image sent Successfully")
   
    return response.json()

try:
    setup()
    forward()
    forward()
    while(1):
        dis = get_distance()

        if(dis<30):
            startee = time.clock()
            stop()

            #send_image()
            main_image = capture_image()

            #time.sleep(5)
            left(0.5)
            left_image = capture_image()
            left_dis = get_distance()
            time.sleep(3)

            right(1)
            right_image = capture_image()
            right_dis = get_distance()
            #time.sleep(3)

            send_image(main_image,left_image,right_image)

            if(right_dis>left_dis):
                left(1)

            print("Time taken for one garbage is ",time.clock()-startee)
            os.remove(main_image)
            os.remove(left_image)
            os.remove(right_image)
            
            forward()
            forward()
except KeyboardInterrupt:
    print("YES")
    GPIO.cleanup()
            





















