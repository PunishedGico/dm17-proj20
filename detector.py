from inference_base import *
from metrics import Metrics
import cv2

class Detector(InferenceBase):
    def __init__(self):
        super().__init__()
        self.graph_name = "nmask.pb"
        self.label_name = "mask_rcnn.pbtxt"

    def setup_session(self, vidinfo):
        with self.inference_graph.as_default():
            self.sess = tf.Session()

            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            self.tensor_dict = {}
            for key in ["num_detections", "detection_boxes", "detection_scores", "detection_classes", "detection_masks"]:
                tensor_name = key + ":0"
                if tensor_name in all_tensor_names:
                    self.tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)

            if "detection_masks" in self.tensor_dict:
                detection_boxes = tf.squeeze(self.tensor_dict["detection_boxes"], [0])
                detection_masks = tf.squeeze(self.tensor_dict["detection_masks"], [0])

                real_num_detection = tf.cast(self.tensor_dict["num_detections"][0], tf.int32)
                detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(detection_masks, detection_boxes, vidinfo["height"], vidinfo["width"])
                detection_masks_reframed = tf.cast(tf.greater(detection_masks_reframed, 0.5), tf.uint8)
            
                self.tensor_dict["detection_masks"] = tf.expand_dims(detection_masks_reframed, 0)

            self.image_tensor = tf.get_default_graph().get_tensor_by_name("image_tensor:0")

    def close_session(self):
        self.sess.close()

    def new_run(self, image):
        output_dict = self.sess.run(self.tensor_dict, feed_dict={self.image_tensor: np.expand_dims(image, 0)})

        output_dict["num_detections"] = int(output_dict["num_detections"][0])
        output_dict["detection_classes"] = output_dict["detection_classes"][0].astype(np.uint8)
        output_dict["detection_boxes"] = output_dict["detection_boxes"][0]
        output_dict["detection_scores"] = output_dict["detection_scores"][0]

        if "detection_masks" in output_dict:
            output_dict["detection_masks"] = output_dict["detection_masks"][0]

        return output_dict

    def run_inference(self, image):
        with self.inference_graph.as_default():
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

                    real_num_detection = tf.cast(tensor_dict["num_detections"][0], tf.int32)
                    detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                    detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                    detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(detection_masks, detection_boxes, image.shape[0], image.shape[1])
                    detection_masks_reframed = tf.cast(tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                    tensor_dict["detection_masks"] = tf.expand_dims(detection_masks_reframed, 0)
                
                image_tensor = tf.get_default_graph().get_tensor_by_name("image_tensor:0")
                
                output_dict = sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(image, 0)})

                output_dict["num_detections"] = int(output_dict["num_detections"][0])
                output_dict["detection_classes"] = output_dict["detection_classes"][0].astype(np.uint8)
                output_dict["detection_boxes"] = output_dict["detection_boxes"][0]
                output_dict["detection_scores"] = output_dict["detection_scores"][0]

                if "detection_masks" in output_dict:
                    output_dict["detection_masks"] = output_dict["detection_masks"][0]
            
            detections = {}
            #Temporary? metric code
            for idx, detection in enumerate(output_dict["detection_scores"]):
                if detection > 0.5:
                    det_class = output_dict["detection_classes"][idx]
                    det_name = self.category_index.get(det_class)["name"]
                    if det_name not in detections:
                        detections[det_name] = 1
                    else:
                        detections[det_name] += 1

            vis_util.visualize_boxes_and_labels_on_image_array(
                image,
                output_dict["detection_boxes"],
                output_dict["detection_classes"],
                output_dict["detection_scores"],
                self.category_index,
                instance_masks=output_dict.get("detection_masks"),
                use_normalized_coordinates=True,
                line_thickness=4)
        return detections
