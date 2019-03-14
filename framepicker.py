import cv2
from detector import Detector

#Class that handles video loading, selecting frames,
# and saving them as separate images in disk
class Framepicker:
    def __init__(self):
        self.vidcap = None
        self.dir = "output/" #Output folder, needs to make sure it exists
        self.vidname = ""
        self.imex = "jpg" #Extension of the images being saved
        self.vidinfo = {} #Dictionary containing data about the video
        self.metadata = [] #List of tuples marking sections to work on

    #Dummy function for loading metadata
    def load_metadata(self):
        self.metadata.append((38000, 87000, "msec"))

    #Loads the video and stores the video info
    def load_video(self, filename=None, video=None, vidname="video"):
        #Determine if video needs to be loaded or is passed
        if filename is not None:
            self.vidcap = cv2.VideoCapture(filename)
            #Isolate filename from path and extension (junk, redo)
            filename = filename.split(".")[0]
            self.vidname = filename.split("/")[1]
        else:
            self.vidcap = video
            self.vidname = vidname

        if self.vidcap.isOpened():
            self.vidinfo = {
                "width" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "fps" : int(self.vidcap.get(cv2.CAP_PROP_FPS)),
                "totalframes" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)),
                "length" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) #Calculate length of the video in milliseconds
                           / int(self.vidcap.get(cv2.CAP_PROP_FPS)) * 1000
            }
            return True
        return False

    #Picks frames from the video at given intervals
    def pick_frames(self, interval, infer=None):
        #First loop through the number of sections specified in the metadata
        for section in range(len(self.metadata)):
            #Convert msec to frames if necessary
            if self.metadata[section][2] == "msec":
                startframe = int(self.metadata[section][0] * self.vidinfo["fps"] / 1000)
                endframe = int(self.metadata[section][1] * self.vidinfo["fps"] / 1000)
            else:
                startframe = self.metadata[section][0]
                endframe = self.metadata[section][1]

            #Then loop through each section with a step value of the interval given
            for i in range(startframe, endframe, interval):
                self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = self.vidcap.read()

                if infer.run_inference(frame):
                    print("Saving frame: " + str(i))
                    self.save_frame(frame, self.vidname + "-frame-" + str(i) + "." + self.imex)

    # ???
    def analyse_frame(self, frame):
        return True

    #Saves a single frame to disk
    def save_frame(self, frame, filename):
        cv2.imwrite(self.dir + filename, frame)

#Test

d = Detector()
d.load_graph(d.graph_name)
d.load_labels(d.label_name)

x = Framepicker()
x.load_metadata()
if x.load_video("Test data/621982f28ad947308051d07c3e4d0df4.mp4"):
    x.pick_frames(60, d)
