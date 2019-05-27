import cv2
import numpy as np
from utils import visualization_utils as vis_util

colours = [(125,255,0,255), (0,252,252,255), (131,255,217,255), (239,255,254,255)]

#Class containing data and functionality related to detection metrics
class Metrics:
    def __init__(self):
        self.frames = [{}]
        self.frames.clear()
        self.total_frames = 0
        self.total_detections = 0
        self.frames_with_detections = 0

        #self.category_index = label_map_util.create_category_index_from_labelmap("mask_rcnn.pbtxt", use_display_name=True)

    def add_detection(self, frame_num, det_classes):
        self.total_frames += 1

        if len(det_classes) > 0:
            self.frames_with_detections += 1

        t = {"frame_num": frame_num}
        z = {**t, **det_classes}
        self.frames.append(z)

    def visualise(self, interval, vidinfo):
        tframes = vidinfo["totalframes"]
        img = np.zeros((40, tframes, 3), np.uint8)
        cv2.rectangle(img, (0,0), (tframes,40), (0,0,0,128), -1)
        
        for frame in self.frames:
            for key, value in frame.items():
                if "bollard" in frame and frame["bollard"] > 0:
                    cv2.rectangle(img, (frame["frame_num"],0), (frame["frame_num"]+interval,8), colours[0], -1)
                
                if "ladder" in frame and frame["ladder"] > 0:
                    cv2.rectangle(img, (frame["frame_num"],10), (frame["frame_num"]+interval,18), colours[1], -1)
                
                if "broken wood" in frame and frame["broken wood"] > 0:
                    cv2.rectangle(img, (frame["frame_num"],20), (frame["frame_num"]+interval,28), colours[2], -1)
                
                if "rope" in frame and frame["rope"] > 0:
                    cv2.rectangle(img, (frame["frame_num"],30), (frame["frame_num"]+interval,38), colours[3], -1)

        asd = cv2.resize(img, (vidinfo["width"], 40))

        r = self.frames_with_detections / self.total_frames
        #font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(asd, "Relevance: " + str(r), (0,30), font, 0.5, (255,255,255))
        
        return asd

    def add_visualisation(self, filename, interval, vidinfo, cat):
        vis = self.visualise(interval, vidinfo)
        
        for frame in self.frames:
            pos = frame["frame_num"]
            tframes = vidinfo["totalframes"]
            w = vidinfo["width"]
            h = vidinfo["height"]

            asd = int((pos+(interval/2))/tframes*w)
            f = filename + str(pos) + ".jpg"
            print("Adding visualisation to: " + f)
            img = cv2.imread(f)

            output_dict = self.load_data(filename, pos)
            self.draw_boxes(img, output_dict)
            """
            vis_util.visualize_boxes_and_labels_on_image_array(
                img,
                output_dict.item().get("detection_boxes"),
                output_dict.item().get("detection_classes"),
                output_dict.item().get("detection_scores"),
                cat,
                instance_masks=output_dict.item().get("detection_masks"),
                use_normalized_coordinates=True,
                line_thickness=4)
            """
            img[h-40:h, 0:0+w] = vis
            cv2.line(img, (asd,h-40), (asd,h), (0,0,255), 1)
            cv2.imwrite(f, img)

    def draw_boxes(self, image, output_dict):
        #for bb in output_dict.item().get("detection_boxes"):
        #    cv2.rectangle(image, (int(1920*bb[1]),int(1080*bb[0])), (int(1920*bb[3]),int(1080*bb[2])), (255,255,255,255), 1)

        for idx, bb in enumerate(output_dict.item().get("detection_boxes")):
            if output_dict.item().get("detection_scores")[idx] > 0.5:
                font = cv2.FONT_HERSHEY_DUPLEX

                label = str(output_dict.item().get("detection_classes")[idx]) + ": " + str(output_dict.item().get("detection_scores")[idx])
                
                cv2.rectangle(image, (int(1920*bb[1]),int(1080*bb[0])), (int(1920*bb[3]),int(1080*bb[2])), colours[output_dict.item().get("detection_classes")[idx]-1], 2)

                tsize = cv2.getTextSize(label, font, 0.75, 1)
                cv2.rectangle(image, (int(1920*bb[1]),int(1080*bb[0])), (int(1920*bb[1])+tsize[0][0],int(1080*bb[0])-tsize[0][1]), colours[output_dict.item().get("detection_classes")[idx]-1], -1)
                cv2.putText(image, label, (int(1920*bb[1]),int(1080*bb[0])), font, 0.75, (0,0,0), 1)

    def load_data(self, filename, pos):
        out = np.load(filename + str(pos) + ".npy")
        return out
