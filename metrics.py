#Class containing data and functionality related to detection metrics
class Metrics:
    def __init__(self):
        self.frame = []
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
