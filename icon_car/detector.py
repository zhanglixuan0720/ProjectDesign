import cv2
import numpy as np
import math


# author: Lixuan Zhang
# usage: 1. init the Detector
#        2. using detect(img) to process the img and return the left and right line angele.


class Detector:
    def __init__(self):
        self.up = 200
        self.down = 481

    def detect(self, img):

        img = img[self.up:self.down:]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY_INV
            | cv2.THRESH_OTSU)

        binary_modify = cv2.morphologyEx(binary, cv2.MORPH_OPEN,
                                         cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
        #cv2.imshow("temp1", binary_modify)

        edges = cv2.Canny(binary_modify, 50, 200)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30,
                                minLineLength=50, maxLineGap=20)
        if lines is None:
            return 0, 0
        lines = lines[:, 0, :]
        hist = np.zeros(33)
        for x1, y1, x2, y2 in lines:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
            if (x1-x2) != 0:
                k = int(np.around(math.atan((y1 - y2) / (x1 - x2)) * 10))
                delta = abs(x1 - x2) + abs(y1 - y2)
                hist[16 + k] += delta
        np.where(hist > 200, hist, 0)
        left1 = right1 = 0
        sl = sum(hist[0:16])
        sr = sum(hist[17:33])
        mx03 = max(sl, sr)*0.1
        if sl > 0 and sl > mx03:
            left1 = np.dot(hist[0:16], np.array(
                range(-16, 0, 1))) / sl
        if sr > 0 and sr > mx03:
            right1 = np.dot(hist[17:33], np.array(
                range(1, 17, 1))) / sr
        cv2.putText(img, "left: "+str(int(left1))+"  right: "+str(int(right1)), (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 200, 200), 2)

        return -left1, right1
