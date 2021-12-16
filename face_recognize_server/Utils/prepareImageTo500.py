import xml.etree.ElementTree as ET
import sys
import cv2
import numpy as np
import imutils

max_size = 500

if len(sys.argv) != 2:
    print(
        "Укажите исходный xml-файл!")
    exit()

xml_file = sys.argv[1]

try:
    # tree = ET.ElementTree(file=xml_file)
    tree = ET.parse(xml_file)
    root = tree.getroot()

    images_root = root.find('images')

    for image in images_root:
        try:
            im = cv2.imread(image.attrib['file'])

            height, width = im.shape[:2]
            if width == max_size:
                continue

            im = imutils.resize(im, width=max_size)
            cv2.imwrite(image.attrib['file'], im)

            new_height, new_width = im.shape[:2]
        except:
            print(image.attrib['file'])
            continue

        # if height < max_size or width < max_size:
        for box in image:

            y1 = int(box.attrib['top'])
            y2 = int(box.attrib['top']) + int(box.attrib['height'])
            x1 = int(box.attrib['left'])
            x2 = int(box.attrib['left']) + int(box.attrib['width'])

            if y1 < 0:
                y1 = 0
            if y1 > height-1:
                y1 = height-1
            if y2 < 0:
                y2 = 0
            if y2 > height-1:
                y2 = height-1
            if x1 < 0:
                x1 = 0
            if x1 > width-1:
                x1 = width-1
            if x2 < 0:
                x2 = 0
            if x2 > width-1:
                x2 = width-1

            im_height = abs(y2-y1)
            im_width = abs(x2-x1)

            ratio_w = width/new_width
            ratio_h = height/new_height

            box.set('top', str(round(y1/ratio_h)))
            box.set('left', str(round(x1/ratio_w)))
            box.set('width', str(round(im_width/ratio_w)))
            box.set('height', str(round(im_height/ratio_h)))

           

    tree.write(xml_file)

except IOError as e:
    print('nERROR - не найден файл: %sn' % e)