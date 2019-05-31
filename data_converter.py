import xml.etree.cElementTree as ET
import os

import numpy as np

class DataConverter():
    def __init__(self):
        self.data = None
        self.width = 1920
        self.height = 1080
        self.source_img = ""

    def load_npy(self, filename):
        self.source_img = os.getcwd() + "\\" + filename.split(".")[0] + ".jpg"
        num = np.load(filename)
        self.data = num.item()
    
    def load_pascalvoc(self):
        pass

    def save_pascalvoc(self, filename):
        #Header
        annotation = ET.Element("annotation")
        ET.SubElement(annotation, "path").text = self.source_img
        source = ET.SubElement(annotation, "source")
        ET.SubElement(source, "database").text = "Unknown"
        size = ET.SubElement(annotation, "size")
        ET.SubElement(size, "width").text = str(self.width)
        ET.SubElement(size, "height").text = str(self.height)
        ET.SubElement(size, "depth").text = str(3)

        #Objects
        for idx, bb in enumerate(self.data["detection_boxes"]):
            if(self.data["detection_scores"][idx] > 0.5):
                obj = ET.SubElement(annotation, "object")
                ET.SubElement(obj, "name").text = str(self.data["detection_classes"][idx]) #Name?
                ET.SubElement(obj, "pose").text = "Unspecified"
                ET.SubElement(obj, "truncated").text = "0"
                ET.SubElement(obj, "difficult").text = "0"

                box = ET.SubElement(obj, "bndbox")
                ET.SubElement(box, "xmin").text = str(int(bb[1] * self.width))
                ET.SubElement(box, "ymin").text = str(int(bb[0] * self.height))
                ET.SubElement(box, "xmax").text = str(int(bb[3] * self.width))
                ET.SubElement(box, "ymax").text = str(int(bb[2] * self.height))

        #Create tree and save to disk
        tree = ET.ElementTree(annotation)
        tree.write(filename)
