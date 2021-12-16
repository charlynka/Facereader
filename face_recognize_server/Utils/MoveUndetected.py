import os
import shutil
IMAGE_DIR = 'trainset'
DEST_DIR = 'Undetected'
f1 = open('./notDetected.txt', 'r')
content = f1.readlines()
content = [x.strip() for x in content]
for line in content:
    shutil.move('./' + IMAGE_DIR + '/' + line, './' + DEST_DIR + '/' + line)
    print(line)
f1.close()