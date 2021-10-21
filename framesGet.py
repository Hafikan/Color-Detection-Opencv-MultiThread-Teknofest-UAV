"""
    Hafıkan Yeşilyurt / 2021-2022 Cevheri Teknofest UAV
    MultiThreading kullanarak kamera verisini farklı bir threade atama

"""


import cv2
import threading as thr
import os


class GetFrames:
    def __init__(self,source=0,width=640,height=480):
        self.source = source

        self.width, self.height = width, height

        self.is_stop = False

        if type(self.source) == str:
            if os.path.isfile(self.source) == False:
                print("Dosya Yolu Bulunamadı!")

                self.is_stop= True

            else:
                self.capture = cv2.VideoCapture(self.source)


        else:
            self.capture = cv2.VideoCapture(self.source)

            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,self.width)

            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,self.height)

        self.success,self.frame = self.capture.read()

    def start(self):
        thr.Thread(target=self.get,args=(),name="Get Frames").start()
        return self
    
    def get(self):
        while True:
            self.success,self.frame = self.capture.read()

            if type(self.source) == str:
                self.frame =  cv2.resize(self.frame,(self.width,self.height))

            if self.is_stop == True:
                self.capture.release()
                break


    def stop(self):
        self.is_stop = True




