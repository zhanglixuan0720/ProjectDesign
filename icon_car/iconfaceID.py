from car import Car
from detector import Detector
from facedetector import FaceDetector
import cv2


def process(left, right):
    direction = 0
    angle = 0
    if left + right < 10 or abs(left-right) > 5:
        if left < right:
            angle = 15-abs(left-right)
            direction = 1
        elif right < left:
            angle = 15-abs(right-left)
            direction = 2

    return direction, angle


cap = cv2.VideoCapture(1)
facedetector = FaceDetector()

while 1:
    ret, img = cap.read()
    if not ret:
        print("usb-camera error, get into normal mode without faceID.")
        break
    faces = facedetector.detect(img)
    valid = facedetector.verifyfaces(faces)
    if valid:
        print("FaceID matched sucessfully,unlock the car.")
        break
    else:
        print("No matched face.")
cap.release()
del facedetector


car = Car()
detector = Detector()
cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    if not ret:
        print("sci-camera error, exit from process.")
        break

    left, right = detector.detect(img)
    # cv2.imshow("linesdetect", img)
    if cv2.waitKey(1) == 27:
        break

    # function to process the left and right information

    direction, angle = process(left, right)
    if direction == 1:
        print("turn left!", angle)
        car.turnleft(angle*2)
    elif direction == 2:
        print("turn right!", angle)
        car.turnright(angle*2)
    else:
        car.forward()
