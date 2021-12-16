# скрипт заменяет width Box-а на X указанной точки
import xml.etree.ElementTree as ET
import sys

def getNodeNumberByName(aNodes, aName):
    p = len(aNodes)
    i = 0
    for i in range(p):
        node = aNodes[i]
        if node.attrib['name'] == aName:
            return i
    raise  Exception("node not found")


# if len(sys.argv) != 3:
#     print(
#         "Usage: <PathToFile> <pointNumber>")
#     exit()

xml_file = 'e:\\ProfileDetector\\NewWomenTiknutie.xml'#sys.argv[1]
pointNum = '22'#int(sys.argv[2])
root = ET.parse(xml_file).getroot()
images_root = root.find('images')

p = len(images_root)
i = 0
for i in range(p):
    imageNode = images_root[i]
    boxNode = imageNode.find('box')

    partNodes = boxNode.findall('part')
    x = int(partNodes[getNodeNumberByName(partNodes, pointNum)].attrib['x'])


    x1 = int(partNodes[getNodeNumberByName(partNodes, '8')].attrib['x']) #точка шнобеля
    x2 = int(partNodes[getNodeNumberByName(partNodes, '24')].attrib['x'])# точка уха

    if x1 > x2:#смотрит вправо
        boxNode.attrib['left'] = str(x)
        boxNode.attrib['width'] = str(abs(x - x1))

    else:
        boxNode.attrib['width'] = str(abs(x - int(boxNode.attrib['left'])))

root = ET.ElementTree(root)
root.write(xml_file + 'Processed.xml')
pass
