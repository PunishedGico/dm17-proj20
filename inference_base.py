import numpy as np
import tensorflow as tf

from object_detection.utils import ops as utils_ops
from utils import label_map_util
from utils import visualization_utils as vis_util

class InferenceBase():
    def __init__(self):
        self.graph_name = ""
        self.label_name = ""

        self.inference_graph = tf.Graph()
        self.category_index = None

    def load_graph(self, filename):
        with self.inference_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(filename, "rb") as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name="")

    def load_labels(self, filename):
        self.category_index = label_map_util.create_category_index_from_labelmap(filename, use_display_name=True)

    def run_inference(self):
        pass
