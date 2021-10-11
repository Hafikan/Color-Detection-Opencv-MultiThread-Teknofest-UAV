import cv2 
import threading as thr

class BlurFrames:
    def __init__(self,frame = None):
        self.frame = frame

        self.is_stop= False 
        
        if self.frame is None:
            self.is_stop = True




    def start(self):
        thr.Thread(target=self.blur,args=(),name="Blur").start()
        return self
    def blur(self):

        while self.is_stop !=True:
            self.blur = cv2.bilateralFilter(self.frame,9,75,75)

            if cv2.waitKey(27)&0xFF == ord("q"):
                self.is_stop=True

    def stop(self):
        self.is_stop = True
        
