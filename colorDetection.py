import imutils
from framesGet import GetFrames
from framesShow import FrameShow
from framesBlur import BlurFrames
import cv2 
import numpy as np 
import time
import threading

def ColorDetection(source = 0,lower = (46,204,118),upper = (180,255,255),width=640,height=480):
    stream = GetFrames(source=source,width=width,height=height).start()
    show = FrameShow(frame=stream.frame,frameName="Frame-1").start()
    blur= BlurFrames(frame=stream.frame).start()


    lower  = np.array([lower])
    upper = np.array([upper])

    kernel = np.ones([3,3])


    red = (0,0,255)
    black = (0,0,0)
    white = (255,255,255)

    prev_time = 0

    logo = cv2.imread(".logo.png")
    logo = imutils.resize(logo,width=125)



    while True:


        if stream.is_stop or show.is_stop or  blur.is_stop :
            stream.stop()
            show.stop()
            blur.stop()
            break 

        
        
        frame = stream.frame 
        frame = cv2.flip(frame,1)
        blur.frame  = frame
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,lower,upper)
        open_ = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
        erode = cv2.erode(open_,kernel)
        dilate = cv2.dilate(erode,kernel)
        contours, hier = cv2.findContours(dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        c  = max(contours,key= lambda x: cv2.contourArea(x),default=0)


        try:
            if len(c) >= 150:
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int32(box)

                m = cv2.moments(c)
                cX = int(m["m10"]/m["m00"])
                cY = int(m["m01"]/m["m00"])

                cv2.circle(frame,(cX,cY),3,red,2)
                cv2.drawContours(frame,[box],0,red,2)

                frame_h,frame_w =  frame.shape[:2]
                cv2.circle(frame,(int(frame_w/2),int(frame_h/2)),4,black,2)


                x_dist = cX - frame_w/2
                y_dist = frame_h/2 - cY 
            

                cv2.putText(frame,"Distance: "+str(x_dist) + " " + str(y_dist),(25,25),cv2.QT_FONT_NORMAL,0.8,black,1)

                cv2.line(frame,(cX,cY),(int(frame_w/2),int(frame_h/2)),white,2)

                



        except:
            cv2.putText(frame,"Cisim Araniyor...",(25,25),cv2.QT_FONT_NORMAL,0.5,red,1)

        show.frame = frame


        n_time = time.time()

        try:
            fps = 1/(n_time-prev_time)
            prev_time = n_time
        except ZeroDivisionError:
            fps = stream.capture.get(cv2.CAP_PROP_FPS)

        cv2.putText(frame,"FPS: "+str(int(fps)),(25,65),cv2.QT_FONT_NORMAL,0.5,black,1)

        h,w,c = frame.shape

        frame[0:125,640-125:640,:] = logo

        threads = threading.active_count()
        cv2.putText(frame,"Calisan is parcacigi: "+str(threads),(25,95),cv2.QT_FONT_NORMAL,0.5,black,1 )

        

    cv2.destroyAllWindows()
ColorDetection(0)

    
