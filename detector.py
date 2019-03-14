import numpy as np
import tensorflow as tf

from object_detection.utils import ops as utils_ops
from utils import label_map_util
from utils import visualization_utils as vis_util

class Detector:
    def __init__(self):
        self.graph_name = "l_frozen_inference_graph.pb"
        self.label_name = "l_label_map.pbtxt"

        self.detection_graph = tf.Graph()
        self.category_index = None

    def load_graph(self, filename):
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(filename, "rb") as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name="")

    def load_labels(self, filename):
        self.category_index = label_map_util.create_category_index_from_labelmap(filename, use_display_name=True)

    def run_inference(self, image):
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

                output_dict = sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(image, 0)})

                output_dict["num_detection"] = int(output_dict["num_detections"][0])
                output_dict["detection_classes"] = output_dict["detection_classes"][0].astype(np.uint8)
                output_dict["detection_boxes"] = output_dict["detection_boxes"][0]
                output_dict["detection_scores"] = output_dict["detection_scores"][0]

                if "detection_masks" in output_dict:
                    output_dict["detection_masks"] = output_dict["detection_masks"][0]
            
            vis_util.visualize_boxes_and_labels_on_image_array(
                image,
                output_dict["detection_boxes"],
                output_dict["detection_classes"],
                output_dict["detection_scores"],
                self.category_index,
                instance_masks=output_dict.get("detection_masks"),
                use_normalized_coordinates=True,
                line_thickness=8)
