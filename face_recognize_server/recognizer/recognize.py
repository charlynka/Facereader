import sys
import cv2
import dlib
import numpy
from abc import ABCMeta, abstractmethod, abstractproperty
from imutils import face_utils
from recognizer import const
from recognizer import analyze
import time
import threading
from recognizer import utils
import copy

import zlib

# класс - точка входа в распознавание
# Сразу при создании класс инициирует пул отдельных потоков распознавания
# Захват потока на распознавание происходит через вызов getFacetRecognizer или getProfileRecognizer
# которые вернут объект распознавания
#   методы могут иметь два параметра:
#   selfRelesase = True, callBack = None
#     selfRelesase - если True, то по окончанию распознавания объект вернет сам себя в пул свободных потоков
#       в противном случае это должен сделать скрипт-родитель через вызовом метода releaseFacetRecognizer или releaseProfileRecognizer
#   callBack - через этот параметр можно передать калбэк-функцию, которая будет вызвана по окончанию распознавания
class FaceRecognizing:
    def __init__(self):
        self.facetPredictor = dlib.shape_predictor(const.config.get('Predictors', 'facet_shape_predictor', fallback = const.FACET_SHAPE_PREDICTOR))
        self.facetDetector = dlib.get_frontal_face_detector()
        self.profile_shape_predictor = dlib.shape_predictor(const.config.get('Predictors', 'profile_shape_predictor', fallback = const.PROFILE_SHAPE_PREDICTOR))
        self.profileDetector = dlib.simple_object_detector(const.config.get('Detectors', 'profile_detector', fallback = const.PROFILE_DETECTOR))
        #создаем классы распознвания фаса и профиля рыла
        #Фасс
        self.facetCritSec = threading.Lock()
        self.facetRecognizerList = {}
        for i in range(const.config.get('Main', 'predictor_threads', fallback=const.PREDICTOR_THREADS)):
            self.facetRecognizerList[i] = [0, FacetRecognizing(self, i)]
        #профиль
        self.profileCritSec = threading.Lock()
        self.profileRecognizerList = {}
        for i in range(const.config.get('Main', 'predictor_threads', fallback=const.PREDICTOR_THREADS)):
            self.profileRecognizerList[i] = [0, ProfileRecognizing(self, i)]


    def recognize(self, facet_image, profile_image):
        recognize_result_facet = ''
        recognize_result_profile = ''

        def callback_func_facet(obj):
            nonlocal recognize_result_facet
            recognize_result_facet = obj.recognizeResult

        def callback_func_profile(obj):
            nonlocal recognize_result_profile
            recognize_result_profile = obj.recognizeResult

        def check_summ(input_hash, img):
            # current_hash = hex(zlib.crc32(img))
            current_hash = zlib.crc32(img)
            if input_hash != str(current_hash):
                return False

            return True

        try:
            facet_recognizer = self.getFacetRecognizer(True, callback_func_facet)
            facet_recognizer.load(bytearray(facet_image))

            profile_recognizer = self.getProfileRecognizer(True, callback_func_profile)
            profile_recognizer.load(bytearray(profile_image))

            facet_recognizer.endJobEvent.wait()
            profile_recognizer.endJobEvent.wait()

            # Тут надо проанализировать данные что пришли и отдать уже конечный резултат работы


            return analyze.Analyze.analyze(recognize_result_facet, recognize_result_profile)

            #return {'result': 'ok',
            #      'data':
            #          {
            #              'facet':recognize_result_facet,
            #              'profile':recognize_result_profile
            #          }
            #      }
        except Exception:
            e = sys.exc_info()[1]
            result = {'result': 'error',
                      'description': 'bad request',
                      'errorText': e.args[0]}
        

    def getFacetRecognizer(self, selfRelesase = True, callBack = None):
        self.facetCritSec.acquire()
        try:
            for (key, [state, obj]) in self.facetRecognizerList.items():
                if state == 0:
                    self.facetRecognizerList[key][0] = 1 #пометили тред как такой, что чухает картинку
                    obj.endJobEvent.clear()
                    obj.callBackFunc = callBack
                    obj.returnToPoolBySelf = selfRelesase
                    return obj
        finally:
            self.facetCritSec.release()

        return None #это вернется когда все треды чухают картинки

    def releaseFacetRecognizer(self, objId):
        self.facetCritSec.acquire()
        try:
            self.facetRecognizerList[objId][0] = 0 #0 - маркер, что данный тред свободен и его можно юзать
        finally:
            self.facetCritSec.release()

    def releaseProfileRecognizer(self, objId):
        self.profileCritSec.acquire()
        try:
            self.profileRecognizerList[objId][0] = 0 #0 - маркер, что данный тред свободен и его можно юзать
        finally:
            self.profileCritSec.release()

    def getProfileRecognizer(self, selfRelesase = True, callBack = None):
        self.profileCritSec.acquire()
        try:
            for (key, [state, obj]) in self.profileRecognizerList.items():
                if state == 0:
                    self.profileRecognizerList[key][0] = 1 #пометили тред как такой, что чухает картинку
                    obj.endJobEvent.clear()
                    obj.callBackFunc = callBack
                    obj.returnToPoolBySelf = selfRelesase
                    return obj
        finally:
            self.profileCritSec.release()
        return None #это вернется когда все треды чухают картинки
    def terminate(self):
        self.facetCritSec.acquire()
        try:
            for (key, [state, obj]) in self.facetRecognizerList.items():
                obj.terminateEvent.set()
                obj.iddleEvent.set()
        finally:
            self.facetCritSec.release()

        self.profileCritSec.acquire()
        try:
            for (key, [state, obj]) in self.profileRecognizerList.items():
                obj.terminateEvent.set()
                obj.iddleEvent.set()
        finally:
            self.profileCritSec.release()

class BaseRecognizing:

    def __init__(self, owner, objId):
        self.objId = objId
        self.recognizeResult = None
        self.points = None
        self.imageCv = None #обект, полученный из cv2.imdecode
        self.imageGray = None #"серый" имадж
        self.rawImage = None
        self.owner = owner #владелец
        self.detector = None
        self.callBackFunc = None #калбек, который дергаем по окончанию распознавания
        self.returnToPoolBySelf = True #флаг, что поток возвращает сам себя в пул свободных потоков
        #self.shape_predictor_path = shape_predictor
        self.predictor = None#shape_predictor#dlib.shape_predictor(self.shape_predictor_path)
        self.iddleEvent = threading.Event() #евент для перевода треда в состояние ожидания
        self.iddleEvent.clear()
        self.endJobEvent = threading.Event() #евент, сигнализирующий что распознавание окончено
        self.endJobEvent.set()
        self.terminateEvent = threading.Event()
        self.terminateEvent.clear() #евент, что надо таки завершить потоковую функу
        thread = threading.Thread(target=self.__threadFunc__)
        thread.start()

    def load(self, rawImage):
        self.rawImage = numpy.asarray(rawImage, dtype=numpy.uint8)
        self.imageCv = cv2.imdecode(self.getRawImage(), cv2.IMREAD_UNCHANGED)
        self.imageGray = cv2.cvtColor(self.imageCv, cv2.COLOR_BGR2GRAY)
        self.iddleEvent.set()

    @abstractmethod
    def release(self):
        pass

    def __threadFunc__(self):
        while True:
            if self.terminateEvent.is_set():
                break
            self.iddleEvent.wait() #ждем, пока не зазжетс евент, что загрузили данные
            if self.terminateEvent.is_set():
                break
            self.iddleEvent.clear()
            self.recognizeResult = self.recognize()
            if self.callBackFunc:
                self.callBackFunc(self)
            self.endJobEvent.set()
            if self.returnToPoolBySelf:
                self.release() #помечаем поток, как свободный для использования

    @abstractmethod
    def getRawImage(self):
        return self.rawImage

    @abstractmethod
    def recognize(self):
        pass

    def getRectFromGrayImage(self, x1, x2, y1, y2):
        return self.imageGray[y1:y2, x1:x2]

    def getRectFromOrigImage(self, x1, x2, y1, y2):
        return self.imageCv[y1:y2, x1:x2]
    def findAreaContours(self, x1, x2, y1, y2):
        imCrop = utils.correctImage2(self.imageGray[y1:y2, x1:x2])
        return


        # imCrop = cv2.normalize(imCrop)
        # imCrop2 = self.imageGray[y1:y2, x1:x2]

        # blur = cv2.GaussianBlur(imCrop, (3, 3), 0)
        # ret3, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_OTSU)

        # thresh = cv2.adaptiveThreshold(imCrop, 205,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        for i in range(200, 255, 1):
            for j in range(150, 151, 5):
                imCrop2 = copy.deepcopy(imCrop)
                ret, thresh = cv2.threshold(imCrop2, i, j, cv2.THRESH_TOZERO)
                _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                for cnt in contours:
                    cv2.drawContours(imCrop2, [cnt], -1, (0, 255, 0), 1)

                cv2.imshow(str(i) + " " + str(j), imCrop2)
        return

        for cnt in contours:
            x = round((x2-x1)/2, 0)
            y = round((y2-y1)/2, 0)
            # if cv2.pointPolygonTest(cnt, (int(x), int(y)), False) > 0.8:
            cv2.drawContours(imCrop, [cnt], -1, (0, 255, 0), 1)
        # contours = cv2.approxPolyDP(contours, 3, True)

        cv2.imshow("Image", imCrop)

class FacetRecognizing(BaseRecognizing):

    def __init__(self, owner, objId):
        BaseRecognizing.__init__(self, owner, objId)
        self.predictor = self.owner.facetPredictor
        self.detector = self.owner.facetDetector

    def recognize(self):
        if (self.imageGray is None) or (self.detector is None):
            return
        rects = self.detector(self.imageGray, 1)
        ar_res = []
        for (i, rect) in enumerate(rects):
            shape = self.predictor(self.imageGray, rect)
            shape = utils.shape_to_np_facet(shape)
            res = {}
            for (name, (i, j)) in utils.FACIAL_LANDMARKS_IDXS.items():
                tmp = []
                n = i + 1 #подгонка нумерации точек под картинку с демки
                for (x, y) in shape[i:j]:
                    tmp += [(n,(x, y))]
                    n += 1
                res[name] = tmp
            ar_res.append(res)
        #докидываем морщины
        for res in ar_res:
            # носогубная морщина
            roi = self.getRectFromGrayImage(dict(res['mouth'])[55][0], dict(res['jaw'])[13][0], dict(res['mouth'])[53][1], dict(res['mouth'])[57][1])
            res['noseWrinkleRight'] = self.__getNoseWrinkle__('right', roi,
                                                         0,
                                                         dict(res['mouth'])[55][1] - dict(res['mouth'])[53][1],
                                                         dict(res['mouth'])[55][0],
                                                         dict(res['mouth'])[55][1],
                                                         dict(res['mouth'])[55][0],
                                                         cannyParam1 = const.config.getint('Wrinkle.NoseWrinkle', 'cannyparam1', fallback=const.NOSE_WRINKLE_CANNYPARAM_1),
                                                         cannyParam2=const.config.getint('Wrinkle.NoseWrinkle', 'cannyparam2', fallback=const.NOSE_WRINKLE_CANNYPARAM_2)
                                                              )

            roi = self.getRectFromGrayImage(dict(res['jaw'])[5][0], dict(res['mouth'])[49][0], dict(res['mouth'])[53][1], dict(res['mouth'])[57][1])
            res['noseWrinkleLeft'] = self.__getNoseWrinkle__('left', roi,
                                                         dict(res['mouth'])[49][0],
                                                         dict(res['mouth'])[49][1] - dict(res['mouth'])[53][1],
                                                         dict(res['jaw'])[5][0],
                                                         dict(res['mouth'])[49][1],
                                                         dict(res['mouth'])[49][0],
                                                         cannyParam1 = const.config.getint('Wrinkle.NoseWrinkle', 'cannyparam1', fallback=const.NOSE_WRINKLE_CANNYPARAM_1),
                                                         cannyParam2=const.config.getint('Wrinkle.NoseWrinkle', 'cannyparam2', fallback=const.NOSE_WRINKLE_CANNYPARAM_2)
                                                              )

            # "удлинитель" рта
            roi = self.getRectFromGrayImage(dict(res['mouth'])[55][0], dict(res['jaw'])[12][0],
                                            dict(res['mouth'])[55][1], dict(res['jaw'])[12][1])
            res['mouthWrinkleRight'] = self.__getMouthWrinkle__('right', roi,
                                                         0,
                                                         0,
                                                         dict(res['mouth'])[55][0],
                                                         dict(res['mouth'])[55][1],
                                                         dict(res['mouth'])[55][0],
                                                         dict(res['mouth'])[55][1],
                                                         cannyParam1 = const.config.getint('Wrinkle.MouthWrinkle', 'cannyparam1', fallback=const.MOUTH_WRINKLE_CANNYPARAM_1),
                                                         cannyParam2=const.config.getint('Wrinkle.MouthWrinkle', 'cannyparam2', fallback=const.MOUTH_WRINKLE_CANNYPARAM_2)
                                                              )
            roi = self.getRectFromGrayImage(dict(res['jaw'])[6][0], dict(res['mouth'])[49][0],
                                            dict(res['mouth'])[49][1], dict(res['jaw'])[6][1])
            res['mouthWrinkleLeft'] = self.__getMouthWrinkle__('left', roi,
                                                         roi.shape[0],#dict(res['mouth'])[49][0],
                                                         0,#dict(res['mouth'])[49][1],
                                                         dict(res['jaw'])[6][0],
                                                         dict(res['mouth'])[49][1],
                                                         dict(res['mouth'])[49][0],
                                                         dict(res['mouth'])[49][1],
                                                         cannyParam1 = const.config.getint('Wrinkle.MouthWrinkle', 'cannyparam1', fallback=const.MOUTH_WRINKLE_CANNYPARAM_1),
                                                         cannyParam2=const.config.getint('Wrinkle.MouthWrinkle', 'cannyparam2', fallback=const.MOUTH_WRINKLE_CANNYPARAM_2)
                                                              )

            # МОРЩИНЫ ВОЗЛЕ ГЛАЗ
            #Определяем прямоугольник возле левого глаза
            x1 = dict(res['right_eye'])[37][0] - (dict(res['right_eye'])[40][0] - dict(res['right_eye'])[37][0])
            x2 = dict(res['right_eye'])[37][0]
            x2 = x2 - int(round((x2 - x1) / 2, 0))
            y1 = dict(res['right_eye'])[38][1]
            y2 = dict(res['right_eye'])[42][1] + abs(
                dict(res['right_eye'])[38][1] - dict(res['right_eye'])[42][1])
            roi = self.getRectFromGrayImage(x1,
                                            x2,
                                            y1,
                                            y2)

            # (self, aName, input_img, startX, startY, absoluteX, absoluteY, mouthX, mouthY,
            res['eyeWrinkleLeft'] = self.__getEyeWrinkle__('left', roi,
                                                         roi.shape[0],
                                                         0,
                                                         x1,
                                                         y1,
                                                         dict(res['right_eye'])[37][0],
                                                         dict(res['right_eye'])[37][1],
                                                         cannyParam1 = const.config.getint('Wrinkle.EyeWrinkle', 'cannyparam1', fallback=const.EYE_WRINKLE_CANNYPARAM_1),
                                                         cannyParam2=const.config.getint('Wrinkle.EyeWrinkle', 'cannyparam2', fallback=const.EYE_WRINKLE_CANNYPARAM_2)
                                                              )

        # Определяем прямоугольник возле правого глаза
        x1 = dict(res['left_eye'])[46][0]
        x2 = dict(res['left_eye'])[46][0] + (
        dict(res['left_eye'])[46][0] - dict(res['left_eye'])[43][0])
        x2 = x2 - int(round((x2 - x1) / 2, 0))
        y1 = dict(res['left_eye'])[45][1]
        y2 = dict(res['left_eye'])[47][1] + abs(
            dict(res['left_eye'])[45][1] - dict(res['left_eye'])[47][1])
        roi = self.getRectFromGrayImage(x1,
                                        x2,
                                        y1,
                                        y2)

        res['eyeWrinkleRight'] = self.__getEyeWrinkle__('right', roi,
                                                       0,
                                                       0,
                                                       x1,
                                                       y1,
                                                       dict(res['left_eye'])[46][0],
                                                       dict(res['left_eye'])[46][1],
                                                       cannyParam1=const.config.getint('Wrinkle.EyeWrinkle',
                                                                                       'cannyparam1',
                                                                                       fallback=const.EYE_WRINKLE_CANNYPARAM_1),
                                                       cannyParam2=const.config.getint('Wrinkle.EyeWrinkle',
                                                                                       'cannyparam2',
                                                                                       fallback=const.EYE_WRINKLE_CANNYPARAM_2)
                                                       )

        #МОРЩИНЫ СКУЛ
        # Определяем скульный прямоугольник возле левого глаза
        x1 = dict(res['right_eye'])[37][0] - (
        dict(res['right_eye'])[40][0] - dict(res['right_eye'])[37][0])
        x2 = dict(res['right_eye'])[37][0]
        x2 = x2 - int(round((x2 - x1) / 2, 0))
        y1 = dict(res['nose'])[29][1]
        y2 = dict(res['nose'])[30][1]
        roi = self.getRectFromGrayImage(x1,
                                        x2,
                                        y1,
                                        y2)

        # (self, aName, input_img, startX, startY, absoluteX, absoluteY, mouthX, mouthY,
        res['cheekboneWrinkleLeft'] = self.__getCheekboneWrinkle__('left', roi,
                                                       roi.shape[0],
                                                       0,
                                                       x1,
                                                       y1,
                                                       dict(res['right_eye'])[37][0],
                                                       dict(res['right_eye'])[37][1],
                                                       cannyParam1=const.config.getint('Wrinkle.CheekboneWrinkle',
                                                                                       'cannyparam1',
                                                                                       fallback=const.CHEEKBONE_WRINKLE_CANNYPARAM_1),
                                                       cannyParam2=const.config.getint('Wrinkle.CheekboneWrinkle',
                                                                                       'cannyparam2',
                                                                                       fallback=const.CHEEKBONE_WRINKLE_CANNYPARAM_2)
                                                       )


        # Определяем скульный прямоугольник возле правого глаза
        x1 = dict(res['left_eye'])[46][0]
        x2 = dict(res['left_eye'])[46][0] + (
        dict(res['left_eye'])[46][0] - dict(res['left_eye'])[43][0])
        x2 = x2 - int(round((x2 - x1) / 2, 0))
        y1 = dict(res['nose'])[29][1]
        y2 = dict(res['nose'])[30][1]
        roi = self.getRectFromGrayImage(x1,
                                        x2,
                                        y1,
                                        y2)

        res['cheekboneWrinkleRight'] = self.__getEyeWrinkle__('right', roi,
                                                       0,
                                                       0,
                                                       x1,
                                                       y1,
                                                       dict(res['left_eye'])[46][0],
                                                       dict(res['left_eye'])[46][1],
                                                       cannyParam1=const.config.getint('Wrinkle.CheekboneWrinkle',
                                                                                       'cannyparam1',
                                                                                       fallback=const.CHEEKBONE_WRINKLE_CANNYPARAM_1),
                                                       cannyParam2=const.config.getint('Wrinkle.CheekboneWrinkle',
                                                                                       'cannyparam2',
                                                                                       fallback=const.CHEEKBONE_WRINKLE_CANNYPARAM_2)
                                                       )



        #МОРЩИНА ПО ЦЕНТРУ ПЕРЕНОСИЦЫ
        delta = int(
            round((dict(res['left_eye'])[43][0] - dict(res['nose'])[28][0]) / 3, 0))
        x1 = dict(res['nose'])[28][0] - delta
        x2 = dict(res['nose'])[28][0] + delta
        # y1 - верхняя точка брови минус высота глаза
        y1 = dict(res['right_eyebrow'])[20][1] - (
        dict(res['right_eye'])[42][1] - dict(res['right_eye'])[38][1])
        y2 = dict(res['right_eye'])[40][1]
        roi = self.getRectFromGrayImage(x1,
                                        x2,
                                        y1,
                                        y2)
        # (self, aName, input_img, startX, startY, absoluteX, absoluteY, mouthX, mouthY,
        res['nosebridgecentralWrinkle'] = self.__getNosebridgecentralWrinkle__('right', roi,
                                                       dict(res['nose'])[28][0],
                                                       dict(res['nose'])[28][1],
                                                       x1,
                                                       y1,
                                                       dict(res['nose'])[28][0],
                                                       dict(res['nose'])[28][1],
                                                       cannyParam1=const.config.getint('Wrinkle.NosebridgecentralWrinkle',
                                                                                       'cannyparam1',
                                                                                       fallback=const.NOSEBRIDGECENTRAL_WRINKLE_CANNYPARAM_1),
                                                       cannyParam2=const.config.getint('Wrinkle.NosebridgecentralWrinkle',
                                                                                       'cannyparam2',
                                                                                       fallback=const.NOSEBRIDGECENTRAL_WRINKLE_CANNYPARAM_2)
                                                       )

        #МОРЩИНЫ ПЕРЕНОСИЦЫ
        #левая морщина переносицы
        delta = int(
            round((dict(res['left_eye'])[43][0] - dict(res['nose'])[28][0]) / 4, 0))
        x1 = dict(res['right_eye'])[40][0]
        x2 = dict(res['nose'])[28][0] - delta
        # y1 - верхняя точка брови минус высота глаза
        y1 = dict(res['right_eyebrow'])[20][1] - (
        dict(res['right_eye'])[42][1] - dict(res['right_eye'])[38][1])
        y2 = dict(res['right_eye'])[40][1]
        roi = self.getRectFromGrayImage(x1,
                                        x2,
                                        y1,
                                        y2)
        res['nosebridgeWrinkleLeft'] = self.__getNosebridgeWrinkle__('left', roi,
                                                       dict(res['nose'])[28][0],
                                                       dict(res['nose'])[28][1],
                                                       x1,
                                                       y1,
                                                       dict(res['nose'])[28][0],
                                                       dict(res['nose'])[28][1],
                                                       cannyParam1=const.config.getint('Wrinkle.NosebridgeWrinkle',
                                                                                       'cannyparam1',
                                                                                       fallback=const.NOSEBRIDGE_WRINKLE_CANNYPARAM_1),
                                                       cannyParam2=const.config.getint('Wrinkle.NosebridgeWrinkle',
                                                                                       'cannyparam2',
                                                                                       fallback=const.NOSEBRIDGE_WRINKLE_CANNYPARAM_2)
                                                       )



    #правая морщина переносицы
        delta = int(
            round((dict(res['left_eye'])[43][0] - dict(res['nose'])[28][0]) / 4, 0))
        x1 = dict(res['nose'])[28][0] + delta
        x2 = dict(res['left_eye'])[43][0]
        # y1 - верхняя точка брови минус высота глаза
        y1 = dict(res['right_eyebrow'])[20][1] - (
        dict(res['right_eye'])[42][1] - dict(res['right_eye'])[38][1])
        y2 = dict(res['right_eye'])[40][1]
        roi = self.getRectFromGrayImage(x1,
                                        x2,
                                        y1,
                                        y2)
        res['nosebridgeWrinkleRight'] = self.__getNosebridgeWrinkle__('right', roi,
                                                       dict(res['nose'])[28][0],
                                                       dict(res['nose'])[28][1],
                                                       x1,
                                                       y1,
                                                       dict(res['nose'])[28][0],
                                                       dict(res['nose'])[28][1],
                                                       cannyParam1=const.config.getint('Wrinkle.NosebridgeWrinkle',
                                                                                       'cannyparam1',
                                                                                       fallback=const.NOSEBRIDGE_WRINKLE_CANNYPARAM_1),
                                                       cannyParam2=const.config.getint('Wrinkle.NosebridgeWrinkle',
                                                                                       'cannyparam2',
                                                                                       fallback=const.NOSEBRIDGE_WRINKLE_CANNYPARAM_2)
                                                                      )

        return self.__analyze__(ar_res)

    def __analyze__(self, rec_points):
        arRes = {}
        self.points = rec_points
        analyzeObj = analyze.AnalyzeFacet()
        for (i, rec_point) in enumerate(rec_points):

            arRes[i] = analyzeObj.analyze(rec_point)

        return arRes

    def release(self):
        self.owner.releaseFacetRecognizer(self.objId)


    def __getNoseWrinkle__(self, aName, input_img, startX, startY, absoluteX, absoluteY, mauseX, cannyParam1=const.NOSE_WRINKLE_CANNYPARAM_1, cannyParam2=const.NOSE_WRINKLE_CANNYPARAM_2):
        bluredImg = input_img #cv2.GaussianBlur(input_img, (3, 3), 0)
        canny_img = cv2.Canny(bluredImg, cannyParam1, cannyParam2)
        ret, thresh = cv2.threshold(canny_img, 60, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour = utils.getNearestContour(
            utils.getContourByParams(contours, aMinXAngle=const.config.getfloat('Wrinkle.NoseWrinkle', 'minXangle', fallback=const.NOSE_WRINKLE_MIN_X_ANGLE),
                                     aMaxYAngle=const.config.getfloat('Wrinkle.NoseWrinkle', 'maxYangle', fallback=const.NOSE_WRINKLE_MAX_Y_ANGLE), aMinLen=input_img.shape[0] * const.config.getfloat('Wrinkle.NoseWrinkle', 'minlenmultiplier', fallback=const.NOSE_WRINKLE_MIN_LEN_MULTIPLIER),
                                     aMaxLen= const.config.getfloat('Wrinkle.NoseWrinkle', 'maxlenmultiplier', fallback=const.NOSE_WRINKLE_MAX_LEN_MULTIPLIER) * input_img.shape[0]), startX, startY)
        # input_img.shape[0] - высота рисунка!!!. В opencv походу одни евреи
        #const.config.getint('Wrinkle.NoseWrinkle', 'cannyparam1', fallback=const.NOSE_WRINKLE_CANNYPARAM_1)
        x, y = (-1, -1)
        l = -1


        # linesImg = utils.createBlankImage(input_img.shape[1], input_img.shape[0])
        # for cnt in contour:
        #     cv2.drawContours(linesImg, [cnt], -1, (255, 255, 255), 1)
        # if aName == 'rig':
        #     cv2.imshow(aName, linesImg)
        #     cv2.waitKey(1)


        if len(contour) > 0:
            x, y = contour[0][0][0]
            l = abs(startY - contour[0][0][0][1])
            for i in range(1, len(contour[0]) - 1):
                k = abs(startY - contour[0][i][0][1])
                if k < l:
                    l = k
                    x, y = contour[0][i][0]
            l = abs(x + absoluteX - mauseX)
            _, width = input_img.shape
            # условие ниже чтобы отбросить ложные детекты на краю рыла (бывает часто у баб, когда волосы по бокам детекит как морщины)
            if l/width > const.config.getfloat('Wrinkle.NoseWrinkle', 'face_delta', fallback=const.NOSE_WRINKLE_FACE_DELTA):
                l = -1
            return {'X': x + absoluteX, 'Y': abs(absoluteY), 'length': l, 'koef': l/width}
        else: # возвращаем -1
            return {'X': x, 'Y': y, 'length': l}


    def __getMouthWrinkle__(self, aName, input_img, startX, startY, absoluteX, absoluteY, mouthX, mouthY,
                               cannyParam1=const.MOUTH_WRINKLE_CANNYPARAM_1,
                               cannyParam2=const.MOUTH_WRINKLE_CANNYPARAM_2):
        bluredImg = input_img #cv2.GaussianBlur(input_img, (3, 3), 0)
        canny_img = cv2.Canny(bluredImg, cannyParam1, cannyParam2)
        ret, thresh = cv2.threshold(canny_img, 60, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contour = utils.getNearestContour(
            utils.getContourByParams(contours, aMinXAngle=const.config.getfloat('Wrinkle.MouthWrinkle', 'minXangle', fallback=const.MOUTH_WRINKLE_MIN_X_ANGLE),
                                     aMaxYAngle=const.config.getfloat('Wrinkle.MouthWrinkle', 'maxYangle', fallback=const.MOUTH_WRINKLE_MAX_Y_ANGLE), aMinLen=input_img.shape[0] * const.config.getfloat('Wrinkle.MouthWrinkle', 'minlenmultiplier', fallback=const.MOUTH_WRINKLE_MIN_LEN_MULTIPLIER),
                                     aMaxLen= const.config.getfloat('Wrinkle.MouthWrinkle', 'maxlenmultiplier', fallback=const.MOUTH_WRINKLE_MAX_LEN_MULTIPLIER) * input_img.shape[0]),
            startX, startY)
        x, y = (-1, -1)
        l = -1
        if len(contour) > 0:
            _, _, _, b = utils.findContourExtremePoints(contour[0]) #тут у нас только один контур
            x, y = b

            l = utils.getVectorLen((mouthX, mouthY), (absoluteX + x, absoluteY + y))
            _, width = input_img.shape
            # условие ниже чтобы отбросить ложные детекты на краю рыла (бывает часто у баб, когда волосы по бокам детекит как морщины)
            if l/width > const.config.getfloat('Wrinkle.MouthWrinkle', 'face_delta', fallback=const.MOUTH_WRINKLE_FACE_DELTA):
                l = -1
            return {'X': x + absoluteX, 'Y': y + absoluteY, 'length': l, 'koef': l/width}
        else: # возвращаем -1
            return {'X': x, 'Y': y, 'length': l}


    def __getEyeWrinkle__(self, aName, input_img, startX, startY, absoluteX, absoluteY, mouthX, mouthY,
                               cannyParam1=const.EYE_WRINKLE_CANNYPARAM_1,
                               cannyParam2=const.EYE_WRINKLE_CANNYPARAM_2):
        input_img_hist = utils.equalizeHistGrayed(input_img)
        canny_img_hist = cv2.Canny(input_img_hist, cannyParam1, cannyParam2)
        ret, thresh = cv2.threshold(canny_img_hist, 60, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = utils.getContourByParams(contours, aMinXAngle = const.config.getfloat('Wrinkle.EyeWrinkle', 'minXangle', fallback=const.EYE_WRINKLE_MIN_X_ANGLE),
                                            aMaxYAngle = const.config.getfloat('Wrinkle.EyeWrinkle', 'maxYangle', fallback=const.EYE_WRINKLE_MAX_Y_ANGLE),
                                            aMinLen = input_img.shape[0] * const.config.getfloat('Wrinkle.EyeWrinkle', 'minlenmultiplier', fallback=const.EYE_WRINKLE_MIN_LEN_MULTIPLIER),
                                            aMaxLen = input_img.shape[0]*const.config.getfloat('Wrinkle.EyeWrinkle', 'maxlenmultiplier', fallback=const.EYE_WRINKLE_MAX_LEN_MULTIPLIER))
        # рисовалка
        # linesImg2 = utils.createBlankImage(input_img.shape[1], input_img.shape[0])
        # for cnt in contours:
        #     cv2.drawContours(linesImg2, [cnt], -1, (255, 255, 255), 1)
        # cv2.imshow('contours=' + aName, linesImg2)
        # cv2.waitKey(1)
        contour = utils.getNearestContour(contours, startX, startY)
        x, y = (-1, -1)
        l = -1
        if len(contour) > 0:
            _, _, _, b = utils.findContourExtremePoints(contour[0]) #тут у нас только один контур
            x, y = b
            l = utils.getVectorLen((mouthX, mouthY), (absoluteX + x, absoluteY + y))
            _, width = input_img.shape
            return {'X': x + absoluteX, 'Y': y + absoluteY, 'length': l}
        else: # возвращаем -1
            return {'X': x, 'Y': y, 'length': l}



    def __getCheekboneWrinkle__(self, aName, input_img, startX, startY, absoluteX, absoluteY, mouthX, mouthY,
                               cannyParam1=const.CHEEKBONE_WRINKLE_CANNYPARAM_1,
                               cannyParam2=const.CHEEKBONE_WRINKLE_CANNYPARAM_2):
        input_img_hist = utils.equalizeHistGrayed(input_img)
        canny_img_hist = cv2.Canny(input_img_hist, cannyParam1, cannyParam2)
        ret, thresh = cv2.threshold(canny_img_hist, 60, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = utils.getContourByParams(contours, aMinXAngle = const.config.getfloat('Wrinkle.CheekboneWrinkle', 'minXangle', fallback=const.CHEEKBONE_WRINKLE_MIN_X_ANGLE),
                                            aMaxYAngle = const.config.getfloat('Wrinkle.CheekboneWrinkle', 'maxYangle', fallback=const.CHEEKBONE_WRINKLE_MAX_Y_ANGLE),
                                            aMinLen = input_img.shape[0] * const.config.getfloat('Wrinkle.CheekboneWrinkle', 'minlenmultiplier', fallback=const.CHEEKBONE_WRINKLE_MIN_LEN_MULTIPLIER),
                                            aMaxLen = input_img.shape[0]*const.config.getfloat('Wrinkle.CheekboneWrinkle', 'maxlenmultiplier', fallback=const.CHEEKBONE_WRINKLE_MAX_LEN_MULTIPLIER))
        contour = utils.getNearestContour(contours, startX, startY)
        x, y = (-1, -1)
        l = -1
        if len(contour) > 0:
            _, _, _, b = utils.findContourExtremePoints(contour[0]) #тут у нас только один контур
            x, y = b
            l = utils.getVectorLen((mouthX, mouthY), (absoluteX + x, absoluteY + y))
            _, width = input_img.shape
            return {'X': x + absoluteX, 'Y': y + absoluteY, 'length': l}
        else: # возвращаем -1
            return {'X': x, 'Y': y, 'length': l}


    #морнщина центра переносицы
    def __getNosebridgecentralWrinkle__(self, aName, input_img, startX, startY, absoluteX, absoluteY, mouthX, mouthY,
                               cannyParam1=const.NOSEBRIDGECENTRAL_WRINKLE_CANNYPARAM_1,
                               cannyParam2=const.NOSEBRIDGECENTRAL_WRINKLE_CANNYPARAM_2):
        input_img_hist = utils.equalizeHistGrayed(input_img)
        canny_img_hist = cv2.Canny(input_img_hist, cannyParam1, cannyParam2)
        ret, thresh = cv2.threshold(canny_img_hist, 60, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = utils.getContourByParams(contours, aMinXAngle = const.config.getfloat('Wrinkle.NosebridgecentralWrinkle', 'minXangle', fallback=const.NOSEBRIDGECENTRAL_WRINKLE_MIN_X_ANGLE),
                                            aMaxYAngle = const.config.getfloat('Wrinkle.NosebridgecentralWrinkle', 'maxYangle', fallback=const.NOSEBRIDGECENTRAL_WRINKLE_MAX_Y_ANGLE),
                                            aMinLen = input_img.shape[0] * const.config.getfloat('Wrinkle.NosebridgecentralWrinkle', 'minlenmultiplier', fallback=const.NOSEBRIDGECENTRAL_WRINKLE_MIN_LEN_MULTIPLIER),
                                            aMaxLen = input_img.shape[0]*const.config.getfloat('Wrinkle.NosebridgecentralWrinkle', 'maxlenmultiplier', fallback=const.NOSEBRIDGECENTRAL_WRINKLE_MAX_LEN_MULTIPLIER))
        contour = utils.getNearestContour(contours, startX, startY)
        x, y = (-1, -1)
        l = -1
        if len(contour) > 0:
            _, _, _, b = utils.findContourExtremePoints(contour[0]) #тут у нас только один контур
            x, y = b
            l = utils.getVectorLen((mouthX, mouthY), (absoluteX + x, absoluteY + y))
            _, width = input_img.shape
            return {'X': x + absoluteX, 'Y': y + absoluteY, 'length': l}
        else: # возвращаем -1
            return {'X': x, 'Y': y, 'length': l}


    #морщины по краям переносицы
    def __getNosebridgeWrinkle__(self, aName, input_img, startX, startY, absoluteX, absoluteY, mouthX, mouthY,
                               cannyParam1=const.NOSEBRIDGE_WRINKLE_CANNYPARAM_1,
                               cannyParam2=const.NOSEBRIDGE_WRINKLE_CANNYPARAM_2):
        input_img_hist = utils.equalizeHistGrayed(input_img)
        canny_img_hist = cv2.Canny(input_img_hist, cannyParam1, cannyParam2)
        ret, thresh = cv2.threshold(canny_img_hist, 60, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = utils.getContourByParams(contours, aMinXAngle = const.config.getfloat('Wrinkle.NosebridgeWrinkle', 'minXangle', fallback=const.NOSEBRIDGE_WRINKLE_MIN_X_ANGLE),
                                            aMaxYAngle = const.config.getfloat('Wrinkle.NosebridgeWrinkle', 'maxYangle', fallback=const.NOSEBRIDGE_WRINKLE_MAX_Y_ANGLE),
                                            aMinLen = input_img.shape[0] * const.config.getfloat('Wrinkle.NosebridgeWrinkle', 'minlenmultiplier', fallback=const.NOSEBRIDGE_WRINKLE_MIN_LEN_MULTIPLIER),
                                            aMaxLen = input_img.shape[0]*const.config.getfloat('Wrinkle.NosebridgeWrinkle', 'maxlenmultiplier', fallback=const.NOSEBRIDGE_WRINKLE_MAX_LEN_MULTIPLIER))
        contour = utils.getNearestContour(contours, startX, startY)
        x, y = (-1, -1)
        l = -1
        if len(contour) > 0:
            _, _, _, b = utils.findContourExtremePoints(contour[0]) #тут у нас только один контур
            x, y = b
            l = utils.getVectorLen((mouthX, mouthY), (absoluteX + x, absoluteY + y))
            _, width = input_img.shape
            return {'X': x + absoluteX, 'Y': y + absoluteY, 'length': l}
        else: # возвращаем -1
            return {'X': x, 'Y': y, 'length': l}


class ProfileRecognizing(BaseRecognizing):

    def __init__(self, owner, objId):
        BaseRecognizing.__init__(self, owner, objId)
        self.predictor = self.owner.profile_shape_predictor
        self.detector = self.owner.profileDetector

    def recognize(self):
        if (self.imageGray is None) or (self.detector is None):
            return
        rects = self.detector(self.imageGray, 1)
        ar_res = []
        for (i, rect) in enumerate(rects):
            shape = self.predictor(self.imageGray, rect)
            shape = utils.shape_to_np_profile(shape)
            res = {}
            for (name, (i, j)) in utils.PROFILE_LANDMARKS_IDXS.items():
                tmp = []
                n = i + 1 #подгонка нумерации точек под картинку с демки
                for (x, y) in shape[i:j]:
                    tmp += [(n,(x, y))]
                    n += 1
                res[name] = tmp
            ar_res.append(res)

        return self.__analyze__(ar_res)

    def __analyze__(self, rec_points):
        arRes = {}
        self.points = rec_points
        analyzeObj = analyze.AnalyzeProfile()
        for (i, rec_point) in enumerate(rec_points):

            arRes[i] = analyzeObj.analyze(rec_point)

        # print(arRes)
        return arRes


    def release(self):
        self.owner.releaseProfileRecognizer(self.objId)


recognize_precessor = FaceRecognizing()


