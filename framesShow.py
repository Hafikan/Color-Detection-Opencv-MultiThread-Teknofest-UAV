import cv2 
import threading as thr 

class FrameShow:
    def __init__(self,frame=None,frameName="Frame"):
        self.frame = frame

        self.frameName = str(frameName)
        self.is_stop = False


        if self.frame is None:
            self.is_stop = True

    def start(self):
        thr.Thread(target=self.show,args=(),name="Show").start()
        return self

    def show(self):
        while self.is_stop !=True:
            cv2.imshow(self.frameName,self.frame)

            if cv2.waitKey(27) & 0xFF == ord("q"):
                self.is_stop=True


    def stop(self):
        self.is_stop=True