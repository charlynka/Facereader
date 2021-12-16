import cv2
from recognizer import analyze

def drawNodule(cvImg, points):
    tmp = dict(points["jaw"])
    cv2.line(cvImg, tmp[4], tmp[5], (255, 0, 0), 2)
    cv2.line(cvImg, tmp[5], tmp[6], (255, 0, 0), 2)
    cv2.line(cvImg, tmp[12], tmp[13], (255, 0, 0), 2)
    cv2.line(cvImg, tmp[13], tmp[14], (255, 0, 0), 2)

def drawJaw(cvImg, points):
    tmp = analyze.AnalyzeMethods.getJawParams(points["jaw"])
    cv2.line(cvImg, tmp['left'][1], (tmp['left'][1][0] + tmp['width'], tmp['left'][1][1]), (128, 128, 0), 2)
    #высоту рыла теперь
    leftBrow = analyze.AnalyzeMethods.getEyeBrowParams(points["left_eyebrow"])
    mouth = analyze.AnalyzeMethods.getMouthParams(points["mouth"])
    rightBrow = analyze.AnalyzeMethods.getEyeBrowParams(points["right_eyebrow"])
    rightEye = analyze.AnalyzeMethods.getEyeParams(points["right_eye"])
    leftEye = analyze.AnalyzeMethods.getEyeParams(points["left_eye"])
    y = leftBrow["top"][1][1] + (leftEye["top"][1][1] - leftBrow["top"][1][1]) / 2  # точка между глазом и бровью
    cv2.line(cvImg, (leftBrow["top"][1][0], int(round(y))), (leftBrow["top"][1][0], int(round(mouth["center"][1]))), (128, 128, 0), 2)
    y = rightBrow["top"][1][1] + (rightEye["top"][1][1] - rightBrow["top"][1][1]) / 2  # точка между глазом и бровью
    cv2.line(cvImg, (rightBrow["top"][1][0], int(round(y))), (rightBrow["top"][1][0], int(round(mouth["center"][1]))), (128, 128, 0), 2)

def drawChin(cvImg, points):
    # рисуем подбородок
    tmp = dict(points["jaw"])
    cv2.line(cvImg, tmp[7], tmp[9], (128, 128, 255), 2)
    # cv2.line(cvImg, tmp[8], tmp[9], (128, 128, 128), 2)
    cv2.line(cvImg, tmp[9], tmp[11], (128, 128, 255), 2)
    # cv2.line(cvImg, tmp[10], tmp[11], (128, 128, 128), 2)
    # tmp = dict(points["mouth"])
    # cv2.circle(cvImg, (int(tmp[49][0]), int(tmp[49][1])), 3, (0, 255, 0), -1)

def drawNostrils(cvImg, points):
    tmp = dict(points["nose"])
    cv2.line(cvImg, tmp[32], tmp[33], (128, 255, 128), 2)
    cv2.line(cvImg, tmp[33], tmp[34], (128, 255, 128), 2)
    cv2.line(cvImg, tmp[34], tmp[35], (128, 255, 128), 2)
    cv2.line(cvImg, tmp[35], tmp[36], (128, 255, 128), 2)

def drawEyebrow(cvImg, points):
    tmp = dict(points["right_eyebrow"])
    cv2.line(cvImg, tmp[18], tmp[19], (255, 128, 128), 2)
    cv2.line(cvImg, tmp[19], tmp[20], (255, 128, 128), 2)
    cv2.line(cvImg, tmp[20], tmp[21], (255, 128, 128), 2)
    cv2.line(cvImg, tmp[21], tmp[22], (255, 128, 128), 2)

def drawnoseWrinkles(cvImg, points):
    tmp = dict(points["noseWrinkleRight"])
    if tmp['length'] != -1:
        cv2.circle(cvImg, (tmp['X'], tmp['Y']), 3, (0, 0, 255), -1)
    tmp = dict(points["noseWrinkleLeft"])
    if tmp['length'] != -1:
        cv2.circle(cvImg, (tmp['X'], tmp['Y']), 3, (0, 0, 255), -1)

def drawMouthWrinkles(cvImg, points):
    tmp = dict(points["mouthWrinkleRight"])
    if tmp['length'] != -1:
        cv2.circle(cvImg, (tmp['X'], tmp['Y']), 3, (0, 0, 255), -1)
    tmp = dict(points["mouthWrinkleLeft"])
    if tmp['length'] != -1:
        cv2.circle(cvImg, (tmp['X'], tmp['Y']), 3, (0, 0, 255), -1)

    tmp = dict(points["mouth"])
    cv2.circle(cvImg, (tmp[49][0], tmp[49][1]), 3, (0, 255, 255), -1)
    cv2.circle(cvImg, (tmp[55][0], tmp[55][1]), 3, (0, 255, 255), -1)

def showDebugDraw(cvImg, points):
    for (i, rec_point) in enumerate(points):
        drawJaw(cvImg, rec_point)
        drawNodule(cvImg, rec_point)
        drawChin(cvImg, rec_point)
        drawEyebrow(cvImg, rec_point)
        drawNostrils(cvImg, rec_point)
        drawnoseWrinkles(cvImg, rec_point)
        drawMouthWrinkles(cvImg, rec_point)



    # cv2.imshow('DebugDraw', cvImg)
    # cv2.imshow('canny__', cv2.Canny(cv2.cvtColor(cvImg, cv2.COLOR_BGR2GRAY), 50, 20))