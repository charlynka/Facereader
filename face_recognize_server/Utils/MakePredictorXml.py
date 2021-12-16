import dlib
import sys
import cv2
import imutils
from imutils import face_utils
import os


# if len(sys.argv) != 2:
#     print(
#         "Укажите фото! ")
#     exit()

# photo = sys.argv[1]

f = open('./predictor.xml', 'w')
f1 = open('./notDetected.txt', 'w')
detector_file = "detector_Mirror_C=40.svm"
detector = dlib.simple_object_detector(detector_file)

f.write("<?xml version='1.0' encoding='ISO-8859-1'?>\n")
f.write("<?xml-stylesheet type='text/xsl' href='image_metadata_stylesheet.xsl'?>\n")
f.write("<dataset>\n")
f.write("<name>iBUG face point dataset - training images</name>\n")
f.write("<images>\n")

IMAGE_DIR = 'trainset'



files = os.listdir('./' + IMAGE_DIR)
for file in files:
    print(file)
    im = cv2.imread('./' + IMAGE_DIR + '/' + file)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)
    if len(rects) == 0:
        print("not detected")
        f1.write(file + "\n")
    for (i, rect) in enumerate(rects):
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        f.write("    <image file='" + IMAGE_DIR + '/' + file + "'>\n")
        f.write("        <box top='" + str(y) + "' left='" + str(x) + "' width='" + str(w) + "' height='" + str(h) + "'>\n")
        f.write("        </box>\n")
        f.write("    </image>\n")
        break



f.write("</images>\n")
f.write("</dataset>\n")
f.close()
f1.close()


exit
im = cv2.imread(photo)
im = imutils.resize(im, width=500)
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

rects = detector(gray, 1)

for (i, rect) in enumerate(rects):
    (x, y, w, h) = face_utils.rect_to_bb(rect)
    cv2.rectangle(im, (x, y), (x + w, y + h), (255, 255, 0), 2)

cv2.imshow("Output", im)
cv2.waitKey(0)