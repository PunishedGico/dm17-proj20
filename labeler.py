import cv2

class Labeler:
    def __init__(self):
        self.frame = None

    def loadframe(self, filename):
        self.frame = cv2.imread(filename)

    def cropframe(self, bb):
        (x1, x2, y1, y2) = bb
        self.crop = self.frame[y1:y2, x1:x2].copy()

    def save(self):
        cv2.imwrite("crop.jpg", self.crop)

#Very testy
p = Labeler()
p.loadframe("output/bdo-frame-500.jpg")
test = (0, 200, 0, 200)
p.cropframe(test)
p.save()
