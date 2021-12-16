import xml.etree.ElementTree as ET
import sys
import cv2
import numpy as np
import imutils

max_size = 400

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

        # if height < max_size or width < max_size:
        for box in image:

            #im_height = int(box.attrib['height'])
            #im_width = int(box.attrib['width'])
            y1 = int(box.attrib['top'])
            y2 = int(box.attrib['top']) + int(box.attrib['height'])
            x1 = int(box.attrib['left'])
            x2 = int(box.attrib['left']) + int(box.attrib['width'])

            if y1 < 0:
                y1 = 0
            if y2 < 0:
                y2 = 0
            if x1 < 0:
                x1 = 0
            if x2 < 0:
                x2 = 0

            im_height = abs(y2-y1)
            im_width = abs(x2-x1)

            if ((im_height == max_size) and (im_width>=max_size)) or ((im_width == max_size) and (im_height>=max_size)):
                continue
            else:
                im_part = im[y1: y2, x1: x2]

                try:
                    if im_width < im_height:
                        im_part = imutils.resize(im_part,width=max_size)
                    else:
                        im_part = imutils.resize(im_part,height=max_size)
                except:
                    print(image.attrib['file'])
                    continue

                box.set('top', '0')
                box.set('left', '0')
                box.set('width', str(np.size(im_part, 1)-1))
                box.set('height', str(np.size(im_part, 0)-1))

                # image.set('box', box)
                cv2.imwrite(image.attrib['file'], im_part)
           

    tree.write(xml_file)

except IOError as e:
    print('nERROR - не найден файл: %sn' % e)