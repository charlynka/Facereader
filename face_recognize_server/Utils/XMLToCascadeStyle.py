import xml.etree.ElementTree as ET
import sys

if len(sys.argv) != 3:
    print(
        "Укажите исходный xml-файл и тип исходного файла!")
    exit()

xml_file = sys.argv[1]
file_type = sys.argv[2]

if not file_type in ['pos', 'neg']:
    print(
        "Неизвестный тип исходного файла!")
    exit()

f = open(file_type + '.txt', 'w')

try:
    # tree = ET.ElementTree(file=xml_file)
    tree = ET.parse(xml_file)
    root = tree.getroot()

    images_root = root.find('images')

    for image in images_root:
        f.write(image.attrib['file'])

        if file_type == "pos":
            boxes_count = len(image.findall('box'))

            f.write(' ' + str(boxes_count))
            for box in image:
                f.write(' ' + box.attrib['left'] + ' ' + box.attrib['top'] + ' ' + box.attrib['width'] + ' ' + box.attrib['height'])
        f.write('\n')


    # print(top)
    #
except IOError as e:
    print('nERROR - не найден файл: %sn' % e)

finally:
   f.close()



