# import sys
# from sys import argv
import random
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
from recognizer import const
import debugDraw
from recognizer import utils
from recognizer import recognize
import argparse
import atexit
import json

# def exit_handler():
#     print('My application is ending!')

def recognizeCallBack(obj):
    if const.USE_DEBUG_DRAW: #юзанье гуи из калбека оберется дедлоком при включенной дебажной рисовалке.
        return #Ибо нефиг
    txtOutput.insert(END, obj.recognizeResult)

def openpicture():
    global curFileName
    FileTypes = [('JPG Image Files', '*.jpg'), ('All files', '*')]
    op = filedialog.askopenfilename(filetypes=FileTypes)
    if op:
        curFileName = op
        img = Image.open(curFileName)
        img.thumbnail((300, 300))
        img = ImageTk.PhotoImage(img)
        imgLabel.imgtk = img
        imgLabel.configure(image=img)
        txtOutput.delete('1.0', END)

    else:
        curFileName = ''

def recognizepicture():
    print(curFileName)
    # global f
    if curFileName != '':
        stream = open(curFileName, "rb")
        rawbytes = bytearray(stream.read())
        if isProfile.get()==1:
            recognizer = recognize.recognize_precessor.getProfileRecognizer(not const.USE_DEBUG_DRAW, recognizeCallBack)
        else:
            recognizer = recognize.recognize_precessor.getFacetRecognizer(not const.USE_DEBUG_DRAW, recognizeCallBack)
        if recognizer is not None:
            if const.USE_DEBUG_DRAW:
                try:
                    recognizer.load(rawbytes)
                    recognizer.endJobEvent.wait()
                    # отладка морщин глаз
                    # #правый
                    # x1 = dict(recognizer.points[0]['left_eye'])[46][0]
                    # x2 =  dict(recognizer.points[0]['left_eye'])[46][0]  +  (dict(recognizer.points[0]['left_eye'])[46][0] - dict(recognizer.points[0]['left_eye'])[43][0])
                    # x2 = x2 - int(round((x2 - x1)/2, 0))
                    # y1 = dict(recognizer.points[0]['left_eye'])[45][1]
                    # y2 = dict(recognizer.points[0]['left_eye'])[47][1] + abs(dict(recognizer.points[0]['left_eye'])[45][1] - dict(recognizer.points[0]['left_eye'])[47][1])
                    # utils.correctImage4(recognizer.getRectFromGrayImage(x1,
                    #                                                     x2,
                    #                                                     y1,
                    #                                                     y2),
                    #                     x1,
                    #                     y1, 'right')

                    # #левый
                    # x1 = dict(recognizer.points[0]['right_eye'])[37][0]  -  (dict(recognizer.points[0]['right_eye'])[40][0] - dict(recognizer.points[0]['right_eye'])[37][0])
                    # x2 = dict(recognizer.points[0]['right_eye'])[37][0]
                    # x2 = x2 - int(round((x2 - x1)/2, 0))
                    # y1 = dict(recognizer.points[0]['right_eye'])[38][1]
                    # y2 = dict(recognizer.points[0]['right_eye'])[42][1] + abs(dict(recognizer.points[0]['right_eye'])[38][1] - dict(recognizer.points[0]['right_eye'])[42][1])
                    # utils.correctImage4(recognizer.getRectFromGrayImage(x1,
                    #                                                     x2,
                    #                                                     y1,
                    #                                                     y2),
                    #                     x1,
                    #                     y1, 'left')


                    #ОТЛАДКА МОРЩИН СКУЛ
                    # #правый
                    # x1 = dict(recognizer.points[0]['left_eye'])[46][0]
                    # x2 =  dict(recognizer.points[0]['left_eye'])[46][0]  +  (dict(recognizer.points[0]['left_eye'])[46][0] - dict(recognizer.points[0]['left_eye'])[43][0])
                    # x2 = x2 - int(round((x2 - x1)/2, 0))
                    # y1 = dict(recognizer.points[0]['nose'])[29][1]
                    # y2 = dict(recognizer.points[0]['nose'])[30][1]
                    # utils.correctImage4(recognizer.getRectFromGrayImage(x1,
                    #                                                     x2,
                    #                                                     y1,
                    #                                                     y2),
                    #                     x1,
                    #                     y1, 'right')

                    # #левый
                    # x1 = dict(recognizer.points[0]['right_eye'])[37][0]  -  (dict(recognizer.points[0]['right_eye'])[40][0] - dict(recognizer.points[0]['right_eye'])[37][0])
                    # x2 = dict(recognizer.points[0]['right_eye'])[37][0]
                    # x2 = x2 - int(round((x2 - x1)/2, 0))
                    # y1 = dict(recognizer.points[0]['nose'])[29][1]
                    # y2 = dict(recognizer.points[0]['nose'])[30][1]
                    # utils.correctImage4(recognizer.getRectFromGrayImage(x1,
                    #                                                     x2,
                    #                                                     y1,
                    #                                                     y2),
                    #                     x1,
                    #                     y1, 'left')


                    #ОТЛАДКА МОРЩИН ПЕРЕНОСИЦЫ
                    # delta = int(round((dict(recognizer.points[0]['left_eye'])[43][0] - dict(recognizer.points[0]['nose'])[28][0])/4, 0))
                    # x1 = dict(recognizer.points[0]['nose'])[28][0] + delta
                    # x2 = dict(recognizer.points[0]['left_eye'])[43][0]
                    # #y1 - верхняя точка брови минус высота глаза
                    # y1 = dict(recognizer.points[0]['right_eyebrow'])[20][1] - (dict(recognizer.points[0]['right_eye'])[42][1] - dict(recognizer.points[0]['right_eye'])[38][1])
                    # y2 = dict(recognizer.points[0]['right_eye'])[40][1]
                    # utils.correctImage4(recognizer.getRectFromGrayImage(x1,
                    #                                                     x2,
                    #                                                     y1,
                    #                                                     y2),
                    #                     x1,
                    #                     y1, 'left')
                    #далее можно юзать любые гуи и рисовалки для отладки

                    ss = json.dumps(recognizer.recognizeResult, ensure_ascii=False, indent=4, sort_keys=True)
                    txtOutput.insert(END, ss)
                    # utils.getFaceOrientation(recognizer.imageCv, dict(recognizer.points[0]))
                    debugDraw.showDebugDraw(recognizer.imageCv, recognizer.points)

                finally:
                    recognize.recognize_precessor.releaseFacetRecognizer(recognizer.objId)
            else:
                recognizer.load(rawbytes)


#atexit.register(exit_handler)
curFileName = ''
root = Tk()

root.title('Face recognizer console')  # окно пиложения
root.geometry('416x800')
openbtn = Button(root, text='Open picture')
openbtn.config(command=lambda: openpicture())
openbtn.pack()
openbtn.place(x=4, y=20, width=94)

btnrecognize = Button(root, text='Recognize picture')
btnrecognize.config(command=lambda: recognizepicture())
btnrecognize.pack()
btnrecognize.place(x=4, y=50, width=94)

isProfile = IntVar()
ProfileCheckBox = Checkbutton(root, text = "It is profile", onvalue = 1, variable=isProfile, offvalue = 0)
ProfileCheckBox.pack()
ProfileCheckBox.place(x=4, y=100)

# imgPanel = Frame(root, bd = 1, relief = SOLID)#RAISED, SUNKEN, FLAT, RIDGE, GROOVE, SOLID
# imgPanel.pack()
# imgPanel.place(x = 110, y = 20, height = 302, width = 302)

imgLabel = Label(root, borderwidth=1, relief=SOLID)
imgLabel.pack()
imgLabel.place(x=110, y=20, width=300, height=300)

txtOutput = Text(root, borderwidth=1, relief=SOLID)
txtOutput.pack()
txtOutput.place(x = 4, y = 330, width=407, height=465)

def on_closing():
    recognize.recognize_precessor.terminate()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
