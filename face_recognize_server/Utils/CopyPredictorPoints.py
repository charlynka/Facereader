import dlib
import sys
import cv2
import imutils
from imutils import face_utils
import os
import xml.etree.ElementTree as ET


f1 = './NewImages8.xml'
f = './Immmmmge.xml'

f2 = './NewImages8Summ.xml'

tree = ET.parse(f)
tree2 = ET.parse(f1)

root = tree.getroot()
root2 = tree2.getroot()

images_root = root.find('images')
images_root2 = root2.find('images')
images_root3 = ET.Element('images')



p = len(images_root)
i = 0
for i in range(p):
    image = images_root[i]
    l = False
    for box in image:
        j = 0
        p2 = len(images_root2)

        for j in range(p2):
            image2 = images_root2[j]
            if image.attrib['file'] == image2.attrib['file']:
                for box2 in image2:
                    for part in box2:
                        box.append(part)
                        l = True
                break
            else:
                continue
    if l == True:
        images_root3.append(image)

tree3 = ET.ElementTree(images_root3)
tree3.write(f2)
    # images_root.append(mirror_images)
print('Success!')