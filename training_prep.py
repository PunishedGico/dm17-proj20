import os
import cv2
import shutil

from mask_to_bb import *
import data_converter

os.chdir(os.getcwd() + "\\output\\relevant")
root = os.getcwd()

#Create folder structure
os.makedirs("maskrcnn/model", exist_ok=True)
os.makedirs("maskrcnn/dataset", exist_ok=True)
os.makedirs("maskrcnn/dataset/annotations", exist_ok=True)
os.makedirs("maskrcnn/dataset/annotations/xml", exist_ok=True)
os.makedirs("maskrcnn/dataset/annotations/masks", exist_ok=True)
os.makedirs("maskrcnn/dataset/train", exist_ok=True)
os.makedirs("maskrcnn/dataset/test", exist_ok=True)
os.makedirs("maskrcnn/inferencegraph", exist_ok=True)
os.makedirs("maskrcnn/checkpoints", exist_ok=True)

#Get all files with jpg extension
files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), f)) and f.split(".")[-1] == "jpg"]

#Create bounding box from masks and save as Pascal VOC
for f in files:
    print(f)
    base = f.split(".")[0]
    mask = base + "_color_mask.png"

    d = data_converter.DataConverter()
    d.data = mask_to_bb(cv2.imread(mask))
    d.source_img = os.getcwd() + "\\" + base + ".jpg"

    d.save_pascalvoc(root + "\\maskrcnn\\dataset\\annotations\\xml\\" + base + ".xml")
    
    shutil.copyfile(f, root + "\\maskrcnn\\dataset\\train\\" + base + ".jpg")

    shutil.copyfile(mask, root + "\\maskrcnn\\dataset\\annotations\\masks\\" + base + ".png")
