import math
import numpy
import cv2
from matplotlib import pyplot as plt
from collections import OrderedDict
from recognizer import const

FACIAL_LANDMARKS_IDXS = OrderedDict([
	("mouth", (48, 68)),
	("right_eyebrow", (17, 22)),
	("left_eyebrow", (22, 27)),
	("right_eye", (36, 42)),
	("left_eye", (42, 48)),
	("nose", (27, 36)),
	("jaw", (0, 17)),
    ("right_eyebrow_bottom", (76, 79)),
    ("left_eyebrow_bottom", (79, 82)),
    ("nose_contour", (68, 76)),
    ("forehead", (82, 90)) #тут косяк по идее, должно до 89 быть. Надо перепроверить!
])

PROFILE_LANDMARKS_IDXS = OrderedDict([
    ("profile", (0, 28))
])

# Возвращает -1 если точка р лежит слева от р1р2 прямой и 1 если справа 
def pointRelativelyStraight(p, p1, p2):
    if p1[1]>p[1]:
        if p[0]-p1[0]>0:
            return 1
        else:
            return -1

    if p2[1]<p[1]:
        if p[0]-p2[0]>0:
            return 1
        else:
            return -1

    (heightTop, center) = getPerpendAndLen(p, p1, p2)	
    if p[0]-center[0]>0:
        return 1
    
    return -1

# p1 и p2 - координаты p - точка, из которой опускаем перпендикуляр. Функа вернет координаты пересечения перпендикуляра с отрезком и его длину
# raiseOnNotInRange - поднять райз, если координаты перпендикуляра лежат за границами отрезка (на той же прямой, но не попадают в отрезок)
def getPerpendAndLen(p, p1, p2, raiseOnNotInRange=False):
    L = pow((p1[0] - p2[0]), 2) + pow((p1[1] - p2[1]), 2)
    PR = (p[0] - p1[0]) * (p2[0] - p1[0]) + (p[1] - p1[1]) * (p2[1] - p1[1])
    cf = PR / L
    if raiseOnNotInRange:
        if cf < 0:
            raise Exception("Perpendicular not in line segment")
        if cf > 1:
            raise Exception("Perpendicular not in line segment")
    xres = p1[0] + cf * (p2[0] - p1[0])
    yres = p1[1] + cf * (p2[1] - p1[1])
    d = math.sqrt((p[0] - xres) ** 2 + (p[1] - yres) ** 2)
    return d, (xres, yres)


# находит крайние точки контура. pointList - [(x, y), (x, y), ....]
def getExtremePoints(pointList):
    x = 0
    y = 1
    left = pointList[0]
    right = pointList[0]
    top = pointList[0]
    bottom = pointList[0]
    i = 1
    while i < len(pointList):
        if left[1][x] > pointList[i][1][x]:
            left = pointList[i]
        if right[1][x] < pointList[i][1][x]:
            right = pointList[i]
        if top[1][y] > pointList[i][1][y]:
            top = pointList[i]
        if bottom[y][1] < pointList[i][1][y]:
            bottom = pointList[i]
        i += 1
    return left, right, top, bottom


#расстояние между двумя точками
def getVectorLen(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


#находит угол между отрезками (p, p1) и (p, p2). То есть оба отрезка начинаются с точки p
def getAngle(p1, p, p2):
    x1 = p1[0] - p[0]
    y1 = p1[1] - p[1]
    d1 = getVectorLen(p1, p)

    x2 = p2[0] - p[0]
    y2 = p2[1] - p[1]
    d2 = getVectorLen(p2, p)
    if d1*d2 == 0:
        return None

    alpha = (x1 * x2 + y1 * y2)/(d1 * d2)
    return math.acos(alpha)*180/math.pi

#находит угол между отрезками (p1, p2) и (k1, k2) образованный при параллельном переносе точки k1 в p2
def getSnippetAngle(p1, p2, k1, k2):
    dx = k1[0] - p2[0]
    dy = k1[1] - p2[1]
    newK = (k2[0] - dx, k2[1] - dy)
    return getAngle(p1, newK, k2)


def getMiddleCoords(p1, p2):
    return (p1[0] + p2[0])/2, (p1[1] + p2[1])/2

def getXDiff(p1, p2):
    # расстояние по Х между точками р1 и р2
    return abs(p1[0]-p2[0])


def getYDiff(p1, p2):
    # расстояние по Y между точками р1 и р2
    return abs(p1[1] - p2[1])

#im - картинка, points - точки 68-модели https://www.learnopencv.com/head-pose-estimation-using-opencv-and-dlib/
def getFaceOrientation(im, points):
    # Read Image
    # im = cv2.imread("headPose.jpg");
    size = im.shape
    zzz = points['nose']

    # 2D image points. If you change the image, you need to change vector
    image_points = numpy.array([
        dict(points['nose'])[31],  # Nose tip
        dict(points['jaw'])[9],  # Chin
        #с глазами не косяк. У нас они поменяны местами просто
        dict(points['right_eye'])[37],  # Left eye left corner
        dict(points['left_eye'])[46],  # Right eye right corner
        dict(points['mouth'])[49],  # Left Mouth corner
        dict(points['mouth'])[55]  # Right mouth corner
    ], dtype="double")

    # 3D model points.
    model_points = numpy.array([
        (0.0, 0.0, 0.0),  # Nose tip
        (0.0, -330.0, -65.0),  # Chin
        (-225.0, 170.0, -135.0),  # Left eye left corner
        (225.0, 170.0, -135.0),  # Right eye right corne
        (-150.0, -150.0, -125.0),  # Left Mouth corner
        (150.0, -150.0, -125.0)  # Right mouth corner

    ])

    # Camera internals

    focal_length = size[1]
    center = (size[1] / 2, size[0] / 2)
    camera_matrix = numpy.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double"
    )

    print("Camera Matrix :\n {0}".format(camera_matrix))

    dist_coeffs = numpy.zeros((4, 1))  # Assuming no lens distortion
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)#стояла cv2.CV_ITERATIVE, но обсералась

    print("Rotation Vector:\n {0}".format(rotation_vector))
    print("Translation Vector:\n {0}".format(translation_vector))

    # Project a 3D point (0, 0, 1000.0) onto the image plane.
    # We use this to draw a line sticking out of the nose

    (nose_end_point2D, jacobian) = cv2.projectPoints(numpy.array([(0.0, 0.0, 1000.0)]), rotation_vector,  translation_vector, camera_matrix, dist_coeffs)

    for p in image_points:
        cv2.circle(im, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

    p1 = (int(image_points[0][0]), int(image_points[0][1]))
    p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

    cv2.line(im, p1, p2, (255, 0, 0), 2)

    # Display image
    cv2.imshow("Output", im)
    cv2.waitKey(0)

def correctImage(input_img):

    lab = cv2.cvtColor(input_img, cv2.COLOR_BGR2LAB)
    # cv2.imshow("lab", lab)

    # -----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)
    # cv2.imshow('l_channel', l)
    # cv2.imshow('a_channel', a)
    # cv2.imshow('b_channel', b)

    # -----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    # cv2.imshow('CLAHE output', cl)

    # -----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl, a, b))
    # cv2.imshow('limg', limg)

    # -----Converting image from LAB Color model to RGB model--------------------
    result_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    cv2.imshow('final', result_img)


    return result_img

def equalizeHistColored(input_img):
    input_img2 = cv2.cvtColor(input_img, cv2.COLOR_BGR2YUV)
    input_img2[:, :, 0] = cv2.equalizeHist(input_img2[:,:,0])
    return cv2.cvtColor(input_img2, cv2.COLOR_YUV2BGR)

def equalizeHistGrayed(input_img):
    return cv2.equalizeHist(input_img)

def sharpenImage(input_img): #добавить резкости
    kernel = numpy.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    return cv2.filter2D(input_img, -1, kernel)

def build_Gabor_filters():
    filters = []
    ksize = 31
    for theta in numpy.arange(0, numpy.pi, numpy.pi / 16):
        kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, 10.0, 0.5, 0, ktype=cv2.CV_32F)
    kern /= 1.5 * kern.sum()
    filters.append(kern)
    return filters

def process_Gabor(img, filters):
    accum = numpy.zeros_like(img)
    for kern in filters:
        fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
        numpy.maximum(accum, fimg, accum)
    return accum

def findContourExtremePoints(cnt):
    leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
    rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
    topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
    bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
    return (leftmost, rightmost, topmost, bottommost)

def createBlankImage(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = numpy.zeros((height, width, 3), numpy.uint8)
    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color
    return image

def createBlankGrayscaleImage(width, height):
    return cv2.cvtColor(createBlankImage(width, height),  cv2.COLOR_BGR2GRAY)

#correctImage4 - отладочная шляпа для морщин
def correctImage4(input_img, startX, startY, aName):
    cv2.imshow(aName + 'Input_img', input_img)
    a1 = const.EYE_WRINKLE_CANNYPARAM_1
    a2 = const.EYE_WRINKLE_CANNYPARAM_2
    #input_img = cv2.GaussianBlur(input_img, (5, 5), 0)
    #Делаем пачку имаджей всяких фильтрованых
    input_img_sharpen = sharpenImage(input_img)
    input_img_hist = equalizeHistGrayed(input_img)
    filters = build_Gabor_filters()
    input_img_gabor = process_Gabor(input_img, filters)
    # cv2.imshow('input_img_sharpen', input_img_sharpen)
    cv2.imshow('input_img_hist', input_img_hist)
    # cv2.imshow('input_img_gabor', input_img_gabor)

    #canny всякие
    canny_img = cv2.Canny(input_img, a1, a2)
    canny_img_sharpen = cv2.Canny(input_img_sharpen, a1, a2)
    canny_img_hist = cv2.Canny(input_img_hist, a1, a2)
    canny_img_gabor = cv2.Canny(input_img_gabor, a1, a2)
    # cv2.imshow(aName + 'canny_img', canny_img)
    # cv2.imshow(aName + 'canny_img_sharpen', canny_img_sharpen)
    cv2.imshow(aName + 'canny_img_hist', canny_img_hist)
    # cv2.imshow(aName + 'canny_img_gabor', canny_img_gabor)

    #бинарные операции
    b1 = cv2.bitwise_and(canny_img, canny_img_gabor) #пока самый лучший результат
    b2 = cv2.bitwise_and(canny_img_hist, canny_img_gabor)
    b3 = cv2.bitwise_or(b1, b2)
    # cv2.imshow('b1=', b1)
    # cv2.imshow('b2=', b2)
    # cv2.imshow('b3=', b3)

    linesImg = createBlankImage(input_img.shape[1], input_img.shape[0])
    linesImg2 = createBlankImage(input_img.shape[1], input_img.shape[0])
    linesImg3 = createBlankImage(input_img.shape[1], input_img.shape[0])

    # return
    # lines = cv2.HoughLinesP(b1, 1, numpy.pi/180, 5)
    # for x in range(0, len(lines)):
    #     for x1, y1, x2, y2 in lines[x]:
    #         cv2.line(linesImg, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # cv2.imshow('linesImg', linesImg)
    # return

    # b4 = cv2.Canny(b1, 0, 50, apertureSize=5)
    # cv2.imshow('b4=', b4)

    ret, thresh = cv2.threshold( canny_img_hist, 60, 255, cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #input_img.shape[0] - высота рисунка!!!. В opencv походу одни евреи

    for cnt in contours:
        cv2.drawContours(linesImg2, [cnt], -1, (255, 255, 255), 1)
    cv2.imshow('contours=' + aName, linesImg2)

    contours = getContourByParams(contours, aMinXAngle = -1, aMaxYAngle = 70, aMinLen = input_img.shape[0] * 0.6, aMaxLen = input_img.shape[0]*2)
    #contours = getContourByParams(contours)

    for cnt in contours:
        cv2.drawContours(linesImg3, [cnt], -1, (255, 255, 255), 1)
    cv2.imshow('first processed contours=' + aName, linesImg3)

    contours = getNearestContour(contours, startX, startY)

    for cnt in contours:
        cv2.drawContours(linesImg, [cnt], -1, (255, 255, 255), 1)
    cv2.imshow('processed contours=' + aName, linesImg)

def getContourByParams(aContours, aMinLen = -1, aMaxLen = -1, aMinXAngle = -1, aMaxXAngle = -1, aMinYAngle = -1, aMaxYAngle = -1):
    """
    из контуров, полученных через findContours находит нужный(е) по параметрам
    если значение параметра -1, то он не учитывается
    aXAngle, aYAngle - максимально допустимые углы между соответсвующими осями. Диапазон - [0 .. 90], то есть всегда берется меньший угол между осью и контуром
    расчет углов берется по точке начала и точке конца контура
    """
    res = []
    if ((aMinLen == -1) and (aMaxLen == -1) and (aMinXAngle == -1) and (aMaxXAngle == -1) and (aMinYAngle == -1) and (
        aMaxYAngle == -1)):#если всё по дефолту, то вертаем список всех контуров
        for cnt in aContours:
            res.append(cnt)
        return res
    #сюды попадаем, когда есть отличные от дефолта параметры
    for cnt in aContours:
        clen = cv2.arcLength(cnt, False)
        l, r, t, b = findContourExtremePoints(cnt)
        xAngle = getAngle(t, b, (b[0] + 10, b[1]))
        if xAngle is None:
            continue
        if (xAngle > 90):
            xAngle = 180 - xAngle
        yAngle = getAngle(l, r, (r[0], r[1] + 10))
        if yAngle is None:
            continue
        if (yAngle > 90):
            yAngle = 180 - yAngle
        if ((aMinLen != -1) and (aMinLen > clen)):
            continue
        if ((aMaxLen != -1) and (aMaxLen < clen)):
            continue
        if ((aMinXAngle != -1) and (aMinXAngle > xAngle)):
            continue
        if ((aMaxXAngle != -1) and (aMaxXAngle < xAngle)):
            continue
        if ((aMinYAngle != -1) and (aMinYAngle > yAngle)):
            continue
        if ((aMaxYAngle != -1) and (aMaxYAngle < yAngle)):
            continue
        res.append(cnt)
    return res

def getNearestContour(contours, aX, aY):
    l = -1;
    res = []
    for cnt in contours:

        k = abs(cv2.pointPolygonTest(cnt, (aX, aY), True))
        if (l == -1):
            l = k
            res = [cnt]
        else:
            if (k < l):
                l = k
                res = [cnt]
    return res




def correctImage3(input_img):
    a1 = 80
    a2 = 120
    ret, mask = cv2.threshold(input_img, 10, 255, cv2.THRESH_BINARY)
    canny_img = cv2.Canny(input_img, a1, a2)
    cv2.imshow('canny_img', canny_img)

    input_img = sharpenImage(input_img)

    canny_img_sharpen = cv2.Canny(input_img, a1, a2)
    cv2.imshow('canny_img_sharpen', canny_img_sharpen)
    cv2.imshow('img_sharpen', input_img)
    # cv2.imshow('bitwise_and', cv2.bitwise_or(canny_img, canny_img_sharpen))
    # return





    input_img = equalizeHistColored(input_img)
    cv2.imshow('img_hist', input_img)

    filters = build_Gabor_filters()

    gabor_img = process_Gabor(input_img, filters)
    cv2.imshow('gabor_img', gabor_img)

    canny_img_hist = cv2.Canny(input_img, a1, a2)
    cv2.imshow('hist_canny_img', canny_img_hist)

    canny_gabor_img = cv2.Canny(gabor_img, a1, a2)
    cv2.imshow('canny_gabor_img', canny_gabor_img)
    b1 = cv2.bitwise_xor(canny_gabor_img, canny_img)
    b1 = cv2.bitwise_and(b1, canny_img)
    b2 = cv2.bitwise_and(canny_img_hist, canny_img_sharpen)
    cv2.imshow('bitwise_and', b1)
    # return



    input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(b1, 0, 255, cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        cv2.drawContours(input_img, [cnt], -1, (255, 255, 255), 1)
    cv2.imshow('contours', input_img)

def correctImage2(input_img):

    img = input_img
    # equ = cv2.equalizeHist(img)
    # img = np.hstack((img, equ))  # stacking images side-by-side
    # cv2.imshow('res.png', res)

    clahe = cv2.createCLAHE(clipLimit=1.8, tileGridSize=(3,3))
    cl1 = clahe.apply(img)
    cv2.imshow("edges!!!!", cl1)
    return cl1





    # с этой херней лучше
    # img = input_img
    # equ = cv2.equalizeHist(img)
    # res = np.hstack((img, equ))  # stacking images side-by-side
    # cv2.imshow('res.png', res)
    # return




    # cv2.imshow("qqqq", input_img)
    # edges = cv2.Canny(input_img, 60, 20)
    # cv2.imshow("edges!!!!", edges)
    # return

    tmpImg = cv2.cvtColor(input_img, cv2.COLOR_BGR2YUV)
    # cv2.imshow('hist', cv2.equalizeHist(tmpImg))
    b, g, r = cv2.split(tmpImg)

    cv2.imshow('b', b)
    cv2.imshow('g', g)
    cv2.imshow('r', r)

    b = cv2.equalizeHist(b)
    g = cv2.equalizeHist(g)
    r = cv2.equalizeHist(r)



    tmpImg = cv2.merge((b, g, r))
    tmpImg = cv2.cvtColor(tmpImg, cv2.COLOR_YUV2BGR)
    tmpImg = cv2.cvtColor(tmpImg, cv2.COLOR_BGR2GRAY)
    return tmpImg


def shape_to_np_facet(shape, dtype="int"):
	# initialize the list of (x, y)-coordinates
	coords = numpy.zeros((89, 2), dtype=dtype)

	# loop over the 89 facial landmarks and convert them
	# to a 2-tuple of (x, y)-coordinates
	for i in range(0, 89):
		coords[i] = (shape.part(i).x, shape.part(i).y)

	# return the list of (x, y)-coordinates
	return coords

def shape_to_np_profile(shape, dtype="int"):
	# initialize the list of (x, y)-coordinates
	coords = numpy.zeros((28, 2), dtype=dtype)

	# loop over the 89 facial landmarks and convert them
	# to a 2-tuple of (x, y)-coordinates
	for i in range(0, 28):
		coords[i] = (shape.part(i).x, shape.part(i).y)

	# return the list of (x, y)-coordinates
	return coords