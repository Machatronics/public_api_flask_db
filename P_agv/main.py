import RPi.GPIO as GPIO
import time
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import serial
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",help = "path to the video file")
ap.add_argument("-a","--min-area",type = int, default=500,help="minimum")
args = vars(ap.parse_args())

if args.get("video",None) is None:
    vs = VideoStream(src=0).start()
    time.sleep(2.0)

else:
    vs = cv2.VideoCapture(args["video"])

firstFrame = None

while True:
    try:

        frame = vs.read()
        frame = frame if args.get("video",None) is None else frame[1]
        text = "Unoccupied"

        if frame is None:
            break

        frame = imutils.resize)frame,width=500)
        gray = cv2.cvtColor(frame,cv2.COLOR.BGR2GRAY)
        gray = cv2.GaussianBlur(gray,(21,21),0)

        if firstFrame is None:
            firstFrame = gray
            continue
        frameDelta = cv2.absdiff(firstFrame,gray)
        thresh = cv2.threshold(frameDelta,25,255,cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh,None,iterations = 2)
        cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in ctns:

            if cv2.contourArea(c) < args["min_area"]:
                continue

                (x,y,w,h) = cv2.boundingRect(c)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                text = "Occupied"

            cv2.putText(frame,"Room Status: {}".format(text),(10,20))
            cv2.FONT_HERSHEY_SIMPLEX,0.5 (0,0,255),2)

            cv2.putText(frame,datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")),
            (10,frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX,0.35,(0,0,255),1)

            cv2.imshow("Security Feed", frame)
            cv2.imshow("Thresh",thresh)
            cv2.imshow("Frame Delta",frameDelta)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
            GPIO.setmode(GPIO.BOARD)
            PIN_TRIGGER = 7
            PIN_ECHO = 11
            PIN_TRIGGER2 = 15
            PIN_ECHO2 = 13

            GPIO.setup(PIN_TRIGGER,GPIO.OUT)
            GPIO.setup(PIN_ECHO,GPIO.IN)
            GPIO.setup(PIN_TRIGGER2,GPIO.OUT)
            GPIO.setup(PIN_ECHO2,GPIO.IN)

            time.sleep(0.2)

            GPIO.output(PIN_TRIGGER,GPIO.HIGH)
            GPIO.output(PIN_TRIGGER2,GPIO.HIGH)

            while (GPIO.input(PIN_ECHO) == 0) & (GPIO.input(PIN_ECHO2) == 0) :
                pulse_start_time = time.time()
                pulse_start_time2 = time.time()

            while (GPIO.input(PIN_ECHO) == 1) & (GPIO.input(PIN_ECHO) == 1) :
                pulse_end_time = time.time()
                pulse_end_time2 = time.time()

            pulse_duration = pulse_end_time - pulse_start_time
            pulse_duration2 = pulse_end_time2 - pulse_start_time2

            distance = round(pulse_duration * 17150,2)
            distance2 = round(pulse_duration2 * 17150,2)

            if(distance > distance2):
                Distance = distance2
            if(distance <= distance2):
                Distance = distance

            print("Distance:", Distance,"cm")
            check = 1
            if(text == "Occupied" and Distance < 15):
                check = 2
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(32,GPIO.OUT)
                GPIO.output(32,1)

                print("Object!")
                ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
                ser.flush()
                ser.write(b'Q')
                text == "a"

                while True:
                    ser.write(b'8')
                    time.sleep(0.1)
                    ser.write(b'B')
                    time.sleep(1)
                    ser.write(b'L')
                    time.sleep(0.5)
                    ser.write(b'F')
                    time.sleep(1)
                    ser.write(b'R')
                    time.sleep(0.5)
                    ser.write(b'S')
                    time.sleep(0.5)
                    GPIO.setmode(GPIO.BOARD)

                    PIN_TRIGGER = 7
                    PIN_ECHO = 11
                    PIN_TRIGGER2 = 15
                    PIN_ECHO2 = 13

                    GPIO.setup(PIN_TRIGGER,GPIO.OUT)
                    GPIO.setup(PIN_ECHO,GPIO.IN)
                    GPIO.setup(PIN_TRIGGER2,GPIO.OUT)
                    GPIO.setup(PIN_ECHO2,GPIO.IN)

                    time.sleep(0.2)

                    print("Calculating distance")

                    GPIO.output(PIN_TRIGGER,GPIO.HIGH)
                    GPIO.output(PIN_TRIGGER2,GPIO.HIGH)

                    time.sleep(0.00001)

                    GPIO.output(PIN_TRIGGER,GPIO.LOW)
                    GPIO.output(PIN_TRIGGER2,GPIO.HIGH)

                    time.sleep(0.00001)

                    GPIO.output(PIN_TRIGGER,GPIO.LOW)
                    GPIO.output(PIN_TRIGGER2,GPIO.LOW)

                    while(GPIO.input(PIN_ECHO) == 0) & (GPIO.input(PIN_ECHO2) == 0):
                        pulse_start_time = time.time()
                        pulse_start_time2 = time.time()

                    while (GPIO.input(PIN_ECHO) == 1) & (GPIO.input(PIN_ECHO) ==1) :
                        pulse_end_time = time.time()
                        pulse_start_time2 = time.time()

                    pulse_duration = pulse_end_time - pulse_start_time
                    pulse_duration2 = pulse_end_time2 - pulse_start_time2

                    distance = round(pulse_duration * 17150,2)
                    distance = round(pulse_duration2 * 17150,2)

                    if(distance > distance2):
                        Distance = distance2

                    if(distance <= distance2):
                        Distance = distance
                    print("Distance:",Distance,"cm")

                    if(Distance < 15):
                        ser.write(b'8')
                        time.sleep(0.1)
                        ser.write(b'B')
                        time.sleep(1)
                        ser.write(b'L')
                        time.sleep(0.5)
                        ser.write(b'F')
                        time.sleep(1)
                        ser.write(b'R')
                        time.sleep(0.5)
                        ser.write(b'S')
                        time.sleep(1)
                    else:
                        text =="a"
                        ser.write(b'C')

                        GPIO.output(32,0)
                        break
    finally:
        GPIO.cleanup()