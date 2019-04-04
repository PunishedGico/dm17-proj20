import cv2
import numpy as np

#Class containing data and functionality related to detection metrics
class Metrics:
    def __init__(self):
        self.frames = [{}]
        self.frames.clear()
        self.total_frames = 0
        self.total_detections = 0
        self.frames_with_detections = 0

    def add_detection(self, frame_num, det_classes):
        t = {"frame_num": frame_num}
        z = {**t, **det_classes}
        self.frames.append(z)

    def visualise(self, interval):
        img = np.zeros((40, 6648, 3), np.uint8)
        cv2.rectangle(img, (0,0), (6648,40), (0,0,0,128), -1)

        for frame in self.frames:
            for key, value in frame.items():
                if "Bollard" in frame and frame["Bollard"] > 0:
                    cv2.rectangle(img, (frame["frame_num"],0), (frame["frame_num"]+interval,8), (125,255,0,255), -1)
                
                if "Ladder" in frame and frame["Ladder"] > 0:
                    cv2.rectangle(img, (frame["frame_num"],10), (frame["frame_num"]+interval,18), (0,252,252,255), -1)
                
                if "Broken wood" in frame and frame["Broken wood"] > 0:
                    cv2.rectangle(img, (frame["frame_num"],20), (frame["frame_num"]+interval,28), (131,255,217,255), -1)
                
                if "Rope" in frame and frame["Rope"] > 0:
                    cv2.rectangle(img, (frame["frame_num"],30), (frame["frame_num"]+interval,38), (239,255,254,255), -1)

        asd = cv2.resize(img, (1920, 40))
        return asd
    
    def add_visualisation(self, filename, totalframes, interval):
        vis = self.visualise(interval)
        
        for frame in self.frames:
            pos = frame["frame_num"]
            asd = int((pos+(interval/2))/totalframes*1920)
            f = filename + str(pos) + ".jpg"
            print("Adding visualisation to: " + f)
            img = cv2.imread(f)
            img[1040:1040+40, 0:0+1920] = vis
            cv2.line(img, (asd,1040), (asd,1080), (255,0,0), 1)
            cv2.imwrite(f, img)


"""
m = Metrics()


m.add_detection(240, {"Bollard": 2})
m.add_detection(480, {"Ladder": 1})
m.add_detection(720, {"Bollard": 1, "Ladder": 4})

m.visualise()

print(m.frames)

class Metrics:
    def __init__(self):
        self.frame = [{}]
        self.classes = {}
        self.total_detections = 0
        self.frames_with_detections = 0
        self.total_frames = 0

    def __str__(self):
        detection_rate = self.frames_with_detections / self.total_frames #Move
        
        ret = ""

        for label in self.classes:
            ret += str(label) + " | " + str(self.classes[label]) + " | " + str(self.classes[label] / self.total_frames) + "\n"

        ret += "Frames with detections: " + str(self.frames_with_detections) + "\n"
        ret += "Total detections: " + str(self.total_detections) + "\n"
        ret += "Detection rate: " + str(detection_rate) + "\n"

        return ret

    def add(self, thing=None, inc=1):
        if thing is not None:
            self.total_detections += inc

            if thing not in self.classes:
                self.classes[thing] = inc
            else:
                self.classes[thing] += inc
    
    def merge(self, other):
        self.total_frames += 1

        if len(other.classes) > 0:
            self.frames_with_detections += 1

        for label in other.classes:
            self.add(label, other.classes[label])

    def update(self):
        pass
"""