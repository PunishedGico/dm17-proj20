import cv2
import numpy as np
import tensorflow as tf

from object_detection.utils import ops as utils_ops
from utils import label_map_util
from utils import visualization_utils as vis_util

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

        #TF data
        self.graph_name = "l_frozen_inference_graph.pb"
        self.label_name = "l_label_map.pbtxt"

        self.detection_graph = tf.Graph()
        self.category_index = None

    def load_graph(self):
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.graph_name, "rb") as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name="")
        
    def load_labels(self):
        self.category_index = label_map_util.create_category_index_from_labelmap(self.label_name, use_display_name=True)

    #Dummy function for loading metadata
    def load_metadata(self):
        self.metadata.append((37000, 87000, "msec"))

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
    def pick_frames(self, interval):
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

                if self.analyse_frame(frame):
                    print("Saving frame: " + str(i))
                    self.save_frame(frame, self.vidname + "-frame-" + str(i) + "." + self.imex)

    #
    def analyse_frame(self, frame):
        with self.detection_graph.as_default():
            with tf.Session() as sess:
                ops = tf.get_default_graph().get_operations()
                all_tensor_names = {output.name for op in ops for output in op.outputs}
                tensor_dict = {}
                for key in ["num_detections", "detection_boxes", "detection_scores", "detection_classes", "detection_masks"]:
                    tensor_name = key + ":0"
                    if tensor_name in all_tensor_names:
                        tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)
                
                if "detection_masks" in tensor_dict:
                    detection_boxes = tf.squeeze(tensor_dict["detection_boxes"], [0])
                    detection_masks = tf.squeeze(tensor_dict["detection_masks"], [0])

                    real_num_detection = tf.cast(tensor_dict["numb_detections"][0], tf.int32)
                    detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                    detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                    detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(detection_masks, detection_boxes, frame.shape[0], frame.shape[1])
                    detection_masks_reframed = tf.cast(tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                    tensor_dict["detection_masks"] = tf.expand_dims(detection_masks_reframed, 0)
                
                image_tensor = tf.get_default_graph().get_tensor_by_name("image_tensor:0")

                output_dict = sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(frame, 0)})

                output_dict["num_detection"] = int(output_dict["num_detections"][0])
                output_dict["detection_classes"] = output_dict["detection_classes"][0].astype(np.uint8)
                output_dict["detection_boxes"] = output_dict["detection_boxes"][0]
                output_dict["detection_scores"] = output_dict["detection_scores"][0]

                if "detection_masks" in output_dict:
                    output_dict["detection_masks"] = output_dict["detection_masks"][0]
            vis_util.visualize_boxes_and_labels_on_image_array(
                frame,
                output_dict["detection_boxes"],
                output_dict["detection_classes"],
                output_dict["detection_scores"],
                self.category_index,
                instance_masks=output_dict.get("detection_masks"),
                use_normalized_coordinates=True,
                line_thickness=8)
        return True

    #Saves a single frame to disk
    def save_frame(self, frame, filename):
        cv2.imwrite(self.dir + filename, frame)

#Test
x = Framepicker()
x.load_metadata()
x.load_graph()
x.load_labels()
if x.load_video("Test data/621982f28ad947308051d07c3e4d0df4.mp4"):
    x.pick_frames(60)
