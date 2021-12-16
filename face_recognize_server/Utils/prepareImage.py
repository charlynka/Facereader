import xml.etree.ElementTree as ET
import sys
import cv2
import numpy as np
import imutils

max_size = 250

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
        im = cv2.imread(image.attrib['file'])

        height, width = im.shape[:2]

        if height > max_size or width > max_size:
            for box in image:
                y1 = int(box.attrib['top'])
                y2 = int(box.attrib['top']) + int(box.attrib['height'])
                x1 = int(box.attrib['left'])
                x2 = int(box.attrib['left']) + int(box.attrib['width'])

                im_part = im[y1: y2, x1: x2]

                im_part = imutils.resize(im_part, width=max_size)

                box.set('top', '0')
                box.set('left', '0')
                box.set('width', str(np.size(im_part, 1)-1))
                box.set('height', str(np.size(im_part, 0)-1))

                # image.set('box', box)
                cv2.imwrite(image.attrib['file'], im_part)

    tree.write(xml_file)

except IOError as e:
    print('nERROR - не найден файл: %sn' % e)