import xml.etree.ElementTree as ET
import sys
import cv2
import copy
import os.path as path
import imutils
from PIL import Image


if len(sys.argv) != 2:
    print(
        "Укажите исходный xml-файл!")
    exit()

xml_file = sys.argv[1]

try:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # mirror_images = ET.Element()

    images_root = root.find('images')


    i = 0
    # for image in images_root:
    p = len(images_root)
    for i in range(p):

        image = images_root[i]
        im = Image.open(image.attrib['file'])

        im_width, im_height = im.size

        image_mirror = copy.deepcopy(image)

        s = path.splitext(image.attrib['file'])
        name = s[0]+'_mirror' + s[1]

        image_mirror.set('file', name)
        # im.show()
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        # im.show()
        for box in image_mirror:

            left = int(box.attrib['left'])
            width = int(box.attrib['width'])

            res_left = abs(left + width - im_width)

            box.set('left', str(res_left))


        im.save(image_mirror.attrib['file'])
        images_root.append(image_mirror)


    tree.write(xml_file)
    # images_root.append(mirror_images)
    print('Success!')

except IOError as e:
    print('nERROR - не найден файл: %sn' % e)