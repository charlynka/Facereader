import xml.etree.ElementTree as ET
import sys
from PIL import Image
import os

#if len(sys.argv) != 2:
#    print(
#        "Укажите исходный xml-файл!")
#    exit()

#xml_file = sys.argv[1]
xml_file = 'OnlyFullProfile_NoMirror.xml'

root = ET.parse(xml_file).getroot()
images_root = root.find('images')

treeRight = ET.Element("dataset")
rootRight = ET.SubElement(treeRight, "images")

p = len(images_root)
i = 0
for i in range(p):
    imageNode = images_root[i]
    boxNode = imageNode.find('box')
    partNodes = boxNode.findall('part')

    file_path = 'right_set\\'+imageNode.attrib['file']
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    x1 = int(partNodes[24].attrib['x'])
    x2 = int(partNodes[8].attrib['x'])


    im = Image.open(imageNode.attrib['file'])

    im_width, im_height = im.size

    if x2 - x1 < 0:
        # шобі все смотрели вправо
        im = im.transpose(Image.FLIP_LEFT_RIGHT)

        for part in boxNode:
            x = int(part.attrib['x'])
            res_x = abs(im_width - x)
            part.set('x', str(res_x))

    # читаем новіе значения
    x1 = int(partNodes[24].attrib['x'])
    x2 = int(partNodes[8].attrib['x'])
    y1 = int(partNodes[0].attrib['y'])
    y2 = int(partNodes[19].attrib['y'])

    boxNode.attrib['left'] = str(x1)
    boxNode.attrib['width'] = str(abs(x2 - x1))

    boxNode.attrib['top'] = str(y1)
    boxNode.attrib['height'] = str(abs(y2 - y1))

    im.save(file_path)
    imageNode.attrib['file'] = file_path
    rootRight.append(imageNode)

treeRight = ET.ElementTree(treeRight)
treeRight.write(xml_file + 'Right.xml')
