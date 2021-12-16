import xml.etree.ElementTree as ET
import sys
import cv2


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

    i = 0
    for image in images_root:
        im = cv2.imread(image.attrib['file'])

        height, width = im.shape[:2]

        image.append(ET.Element('box', {'top': '0', 'left': '0', 'width': str(width), 'height': str(height)}))

        i += 1

    tree.write(xml_file)
    print('Success! i=' + str(i))

except IOError as e:
    print('nERROR - не найден файл: %sn' % e)