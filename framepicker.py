import cv2
import numpy as np

#Class that handles loading video, selecting frames,
# and saving them as separate images in disk
class Framepicker:
    def __init__(self):
        self.vidcap = None
        self.imex = "jpg" #Extension of the images being saved
        self.vidinfo = {} #Dictionary containing data about the video
        self.metadata = [] #List of tuples marking sections to work on

    #Destructor, probably useless and wrong?
    def __del__(self):
        self.vidcap.release()

    #Dummy function for loading metadata
    def loadmetadata(self):
        for i in range(1):
            self.metadata.append((500, 1000))
            self.metadata.append((1500, 2000))

    #Loads the video and stores the video info
    def loadvideo(self, filename):
        self.vidcap = cv2.VideoCapture(filename)

        if self.vidcap.isOpened():
            self.vidinfo = {
                "width" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "fps" : int(self.vidcap.get(cv2.CAP_PROP_FPS)),
                "totalframes" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)),
                "length" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) #Calculate length of the video in seconds
                           / int(self.vidcap.get(cv2.CAP_PROP_FPS))
            }
            return True

        return False

    #Picks frames from the video at given intervals
    def pickframes(self, interval):
        #First loop through the number of sections specified in the metadata
        for section in range(len(self.metadata)):
            #Then loop through each section with a step value of the interval given
            for i in range(self.metadata[section][0], self.metadata[section][1], interval):
                self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = self.vidcap.read()

                if self.analyseframe(frame):
                    print("Saving frame: " + str(i))
                    self.saveframe(frame, "test" + str(i) + "." + self.imex)

    #Dummy function for analysing a frame and determining if it's worth saving
    def analyseframe(self, frame):
        return True

    #Saves a single frame to disk
    def saveframe(self, frame, filename):
        cv2.imwrite(filename, frame)

x = Framepicker()
x.loadmetadata()
if x.loadvideo("Wildlife.wmv"):
    x.pickframes(200)
