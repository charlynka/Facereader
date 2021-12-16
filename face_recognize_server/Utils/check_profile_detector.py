import dlib
import sys
import cv2
import imutils
from imutils import face_utils


if len(sys.argv) != 2:
    print(
        "Укажите фото! ")
    exit()

photo = sys.argv[1]

detector_file = "./Predictors/profile_detector.svm"

detector = dlib.simple_object_detector(detector_file)

im = cv2.imread(photo)
im = imutils.resize(im, width=500)
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

rects = detector(gray, 1)

for (i, rect) in enumerate(rects):
    (x, y, w, h) = face_utils.rect_to_bb(rect)
    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("Output", im)
cv2.waitKey(0)