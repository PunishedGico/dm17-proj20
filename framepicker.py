import cv2
import numpy as np

class Framepicker:
    def __init__(self):
        self.vidcap = None
        self.imex = "jpg"
        self.vidinfo = {}
        self.metadata = []

    def __del__(self):
        self.vidcap.release()

    def loadmetadata(self):
        for i in range(1):
            self.metadata.append((500, 1000))
            self.metadata.append((1500, 2000))

    def loadvideo(self, filename):
        self.vidcap = cv2.VideoCapture(filename)

        if self.vidcap.isOpened():
            self.vidinfo = {
                "width" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "fps" : int(self.vidcap.get(cv2.CAP_PROP_FPS)),
                "totalframes" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)),
                "length" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
                           / int(self.vidcap.get(cv2.CAP_PROP_FPS))
            }
            return True

        return False

    def pickframes(self, interval):
        for section in range(len(self.metadata)):
            for i in range(self.metadata[section][0], self.metadata[section][1], interval):
                self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = self.vidcap.read()

                if self.analyseframe(frame):
                    print("Saving frame: " + str(i))
                    self.saveframe(frame, "test" + str(i) + "." + self.imex)

    def analyseframe(self, frame):
        return True

    def saveframe(self, frame, filename):
        cv2.imwrite(filename, frame)

x = Framepicker()
x.loadmetadata()
if x.loadvideo("test.mp4"):
    x.pickframes(200)
