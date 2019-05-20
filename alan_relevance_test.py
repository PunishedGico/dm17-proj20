from alan import Alan
from framepicker import Framepicker
from detector import Detector

import os

relevance_list = [{}]
relevance_list.pop(0)

a = Alan()
video_list = a.get_all_videos()

for v in video_list:
    filename = a.download_video(v)
    
    d = Detector()
    d.load_graph(d.graph_name)
    d.load_labels(d.label_name)

    x = Framepicker()
    x.load_metadata()
    if x.load_video(filename):
        x.pick_frames(1000, d)

    with open("output/" + filename.split("/")[-1] + ".txt", "r") as f:
        content = f.read()
    os.remove("output/" + filename.split("/")[-1] + ".txt")

    relevance_list.append({"name" : filename.split("/")[-1], "relevance" : float(content)})

out_list = sorted(relevance_list, key=lambda k: k["relevance"], reverse=True)

with open("output/result.txt", "w") as f:
    for item in out_list:
        f.write(str(item) + "\n")
