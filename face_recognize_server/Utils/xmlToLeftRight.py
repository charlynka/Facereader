import xml.etree.ElementTree as ET
import sys

if len(sys.argv) != 2:
    print(
        "Укажите исходный xml-файл!")
    exit()

xml_file = sys.argv[1]
root = ET.parse(xml_file).getroot()
images_root = root.find('images')

treeLeft = ET.Element("dataset")
rootLeft = ET.SubElement(treeLeft, "images")

treeRight = ET.Element("dataset")
rootRight = ET.SubElement(treeRight, "images")

p = len(images_root)
i = 0
for i in range(p):
    imageNode = images_root[i]
    boxNode = imageNode.find('box')
    partNodes = boxNode.findall('part')
    x1 = int(partNodes[8].attrib['x'])
    x2 = int(partNodes[24].attrib['x'])
    if x2 - x1 > 0:
        rootLeft.append(imageNode)
    else:
        rootRight.append(imageNode)


treeLeft = ET.ElementTree(treeLeft)
treeLeft.write(xml_file + 'Left.xml')

treeRight = ET.ElementTree(treeRight)
treeRight.write(xml_file + 'Right.xml')
