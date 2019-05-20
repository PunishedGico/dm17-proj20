import cv2
import numpy as np
from detector import Detector
from metrics import Metrics

import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

#Class that handles video loading, selecting frames,
#and saving them as separate images in disk
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
        #self.metadata.append((60000, 200000, "msec"))
        pass

    #Add metadata
    def add_metadata(self):
        pass

    #Loads the video and stores the video info
    def load_video(self, filename=None, video=None, vidname="video"):
        #Determine if video needs to be loaded or is passed
        if filename is not None:
            self.vidcap = cv2.VideoCapture(filename)
            #Isolate filename from path and extension (COMPLETE junk, redo)
            filename = filename.split(".")[0]
            self.vidname = filename.split("/")[2]
        else:
            self.vidcap = video
            self.vidname = vidname

        #Store info about the video
        if self.vidcap.isOpened():
            self.vidinfo = {
                "width" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "fps" : int(self.vidcap.get(cv2.CAP_PROP_FPS)),
                "totalframes" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)),
                "length" : int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) #Calculate length of the video in milliseconds
                           / int(self.vidcap.get(cv2.CAP_PROP_FPS)) * 1000
            }
            self.metadata.append((0, self.vidinfo["totalframes"], "f"))
            #self.metadata.append((4000, 5000, "f"))
            return True
        return False

    #Picks frames from the video at given intervals
    def pick_frames(self, interval, infer=None):
        metric = Metrics()
        #First loop through the number of sections specified in the metadata
        for section in range(len(self.metadata)):
            #Convert msec to frames if necessary
            if self.metadata[section][2] == "msec":
                startframe = int(self.metadata[section][0] * self.vidinfo["fps"] / 1000)
                endframe = int(self.metadata[section][1] * self.vidinfo["fps"] / 1000)
            else:
                startframe = self.metadata[section][0]
                endframe = self.metadata[section][1]

            infer.setup_session(self.vidinfo)
            #Then loop through each section with a step value of the interval given
            for i in range(startframe, endframe, interval):
                self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = self.vidcap.read()

                output_dict = infer.new_run(frame)
                print("Saving frame: " + str(i))
                #print(output_dict)
                
                detections = {}
                total_d = 0
                #Temporary? metric code
                for idx, detection in enumerate(output_dict["detection_scores"]):
                    if detection > 0.5:
                        total_d += 1
                        det_class = output_dict["detection_classes"][idx]
                        det_name = infer.category_index.get(det_class)["name"]
                        if det_name not in detections:
                            detections[det_name] = 1
                        else:
                            detections[det_name] += 1
                
                metric.add_detection(i, detections)

                self.save_data(output_dict, self.vidname + "-frame-" + str(i) + ".npy", total_d)

                self.save_frame(frame, self.vidname + "-frame-" + str(i) + "." + self.imex)
        
        infer.close_session()
        print("Final:")
        print(metric.frames)
        metric.add_visualisation(self.dir + self.vidname + "-frame-", interval, self.vidinfo, infer.category_index)
        
    #Saves a single frame to disk
    def save_frame(self, frame, filename):
        cv2.imwrite(self.dir + filename, frame)

    def save_data(self, dic, filename, total_d):
        m = dic.pop("detection_masks")
        eh = m[0:total_d]
        dic["detection_masks"] = eh
        np.save(self.dir + filename, dic)

#Test
d = Detector()
d.load_graph(d.graph_name)
d.load_labels(d.label_name)

x = Framepicker()
x.load_metadata()
if x.load_video("Test data/Relevance test/relevant.mp4"):
    x.pick_frames(1920, d)

"""
#Big test

d = Detector()
d.load_graph(d.graph_name)
d.load_labels(d.label_name)

x = Framepicker()
x.load_metadata()
if x.load_video("Test data/Relevance test/maybe_relevant.mp4"):
    x.pick_frames(24, d)

d = Detector()
d.load_graph(d.graph_name)
d.load_labels(d.label_name)

x = Framepicker()
x.load_metadata()
print("minor_relevance.mp4:")
if x.load_video("Test data/Relevance test/minor_relevance.mp4"):
    x.pick_frames(24, d)

d = Detector()
d.load_graph(d.graph_name)
d.load_labels(d.label_name)

x = Framepicker()
x.load_metadata()
print("minor_relevance_2.mp4:")
if x.load_video("Test data/Relevance test/minor_relevance_2.mp4"):
    x.pick_frames(24, d)

d = Detector()
d.load_graph(d.graph_name)
d.load_labels(d.label_name)

x = Framepicker()
x.load_metadata()
print("not_relevant.mp4:")
if x.load_video("Test data/Relevance test/not_relevant.mp4"):
    x.pick_frames(24, d)

d = Detector()
d.load_graph(d.graph_name)
d.load_labels(d.label_name)

x = Framepicker()
x.load_metadata()
print("relevant.mp4:")
if x.load_video("Test data/Relevance test/relevant.mp4"):
    x.pick_frames(24, d)
"""
