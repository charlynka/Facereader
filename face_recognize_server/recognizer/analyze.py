from recognizer import utils
from recognizer import const
from enum import Enum



class characteristic_indicator(Enum):
    mild_characteristic =  "mild" # слабовыраженная характеристика
    moderate_characteristic = "moderate" # средневыраженная характеристика
    strong_characteristic = "strong" # сильновыраженная характеристика

class face_characteristic(Enum):
    # для лица в фас
    face_height = "faceHeight"  # лицо - длина

    mouth_width = "mouthWidth"  # ширина рта
    upper_lip_height = "upperLipHeight"  # верхняя губа - высота

    eye_size = "eyeSize"  # размер глаз
    eye_height_size = "eyeHeightSize"  # высота глаз

    eyebrow_height = "eyebrowHeight"  # высота бровей
    eyebrow_thiсkness = "eyebrowThiсkness"  # толщина бровей

    nodule = "nodule"  # желвак
    chin_width = "chinWidth"  # ширина подбородка
    jaw_weight = "jawWeight"  # вес челюсти

    nasolabial_zone = "nasolabialZone"  # размер носогубной зоны
    nose_height = "noseHeight"  # высота носа
    nose_width = "noseWidth"  # ширина носа в области ноздрей
    nose_nostrils_form = "nostrilsForm"  # форма ноздрей (прямые/срезанные)
    nose_nostrils_type = "nostrilsType"  # тип ноздрей (открытые/закрытые)
    nose_bridge = "noseBridge"  # переносица
    nose_nasal_bridge = "nasalBridge"  # спинка носа
    nose_wings_width = "noseWingsWidth"  # ширина крільев носа
    nose_nostrils_width = "noseNostrilsWidth" #размер ноздрей

    forehead_height = "foreheadHeight"  # высота лба
    nose_wrinkle = "noseWrinkle" # носогубная морщина
    mouth_wrinkle = "mouthWrinkle" # морщина "удлинитель" рта
    eye_wrinkle = "eyeWrinkle"  # морщина в уголках глаз
    cheekbone_wrinkle = "cheekboneWrinkle"  # морщина скул
    nosebridgecentral_wrinkle = "nosebridgecentralWrinkle"
    nosebridge_wrinkle = "nosebridgeWrinkle"

    # для лица в профиль
    profile_nose_length = "noseLength"
    profile_nose_evenness = "noseEvenness"  # с горбинкой или без

    profile_forehead_evenness = "foreheadEvenness"  #выдающийся или скошенный
    profile_chin_presence = "chinPresence"  #подбородок есть или нету

    profile_jaw_trend = "jawTrend"  # челюсть вперед или назад
    profile_nostrils_type = "nostrilsProfileType"

class general_characteristic(Enum):
    ambitions = "ambitions" # амбиции
    # психопатию пока не считаем
    #psychopathy = "psychopathy" # психопатия
    nervous_system = "nervousSystem" # нервная система
    behavior = "behavior" # поведение
    perception_of_information = "perceptionOfInformation" # восприятие информации
    risk_appetite = "riskAppetite" # склонность к риску
    intellectual_abilities = "intellectualAbilities" # интеллектуальные способности
    reference = "reference" # референция


profile_type = "profile"
facet_type = "facet" 



class characteristic():
    def __init__(self, char_name, char_value, char_type):
        self.name = char_name

        self.type = char_type

        self.values = char_value

class chracteristic_value():
    def __init__(self, strong, moderate, mild):
        self.value = {
            characteristic_indicator.mild_characteristic.value: mild,
            characteristic_indicator.moderate_characteristic.value: moderate,
            characteristic_indicator.strong_characteristic.value: strong
        }

class group_face_characteristic(Enum):
    ambitions_set = [ # амбиции
        # фас
        characteristic( #большой рот/маленький рот
            face_characteristic.mouth_width,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        characteristic( #морщины удлинители есть/нет
            face_characteristic.mouth_wrinkle,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = None
            ),
            facet_type
        )
        # профиль
    ]
    # психопатию пока не считаем
    #psychopathy_set = set( # психопатия
        # фас
        # профиль
    #)
    nervous_system_set = [ # нервная система
        # фас
        characteristic( #высокая челюсть/низкая челюсть
            face_characteristic.jaw_weight,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        characteristic( #широкая челюсть/узкая челюсть
            face_characteristic.chin_width,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        characteristic( #желвак есть/нет
            face_characteristic.nodule,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        characteristic( #широкая спинка носа/тонкая спинка носа
            face_characteristic.nose_nasal_bridge,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        characteristic( #крепкие ноздри/тонкие ноздри
            face_characteristic.nose_wings_width,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),

        characteristic( #крепкие ноздри/тонкие ноздри
            face_characteristic.nose_nostrils_width,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        )
        # профиль
    ]
    behavior_set = [ # поведение
        # фас
        characteristic( #круглое лицо/длинное лицо
            face_characteristic.face_height,
            chracteristic_value(
                strong = -1,
                moderate = None,
                mild = 1
            ),
            facet_type
        ),
        characteristic( #короткая челюсть/высокая челюсть
            face_characteristic.jaw_weight,
            chracteristic_value(
                strong = -1,
                moderate = None,
                mild = 1
            ),
            facet_type
        ),
        characteristic( #тонкая спинка носа/широкая спинка носа
            face_characteristic.nose_nasal_bridge,
            chracteristic_value(
                strong = -1,
                moderate = None,
                mild = 1
            ),
            facet_type
        ),
        characteristic( #срезанные ноздри/ровные ноздри
            face_characteristic.nose_nostrils_form,
            chracteristic_value(
                strong = -1,
                moderate = None,
                mild = 1
            ),
            facet_type
        ),
        characteristic( #тонкие крылья носа/крепкие крылья носа
            face_characteristic.nose_wings_width,
            chracteristic_value(
                strong = -1,
                moderate = None,
                mild = 1
            ),
            facet_type
        ),
        characteristic( #выраженные брови/слабые брови
            face_characteristic.eyebrow_thiсkness,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        # профиль
        characteristic( #нос с горбинкой/-
            face_characteristic.profile_nose_evenness,
            chracteristic_value(
                strong = None,
                moderate = None,
                mild = 1
            ),
            profile_type
        ),
        characteristic(  # для профиля открытые/закрытые ноздри
            face_characteristic.profile_nostrils_type,
            chracteristic_value(
                strong=1,
                moderate=None,
                mild=-1
            ),
            facet_type
        ),
        # characteristic( # -/прогнутая переносица
        #    face_characteristic.profile_nose_evenness,
        #    chracteristic_value(
        #        strong = None,
        #        moderate = None,
        #        mild = 1
        #    ),

        #    profile_type
        #),
        characteristic( #скошенный лоб/выдающийся лоб
            face_characteristic.profile_forehead_evenness,
            chracteristic_value(
                strong = -1,
                moderate = None,
                mild = 1
            ),
            profile_type
        )
        # -/высокая линия роста волос - ?
    ]
    perception_of_information_set = [ # восприятие информации
        # фас
        characteristic( #длинные глаза/узкие глаза
            face_characteristic.eye_size,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        characteristic( #большие глаза/маленькие глаза
            face_characteristic.eye_height_size,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        characteristic( #высокие брови/низкие брови
            face_characteristic.eyebrow_height,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        characteristic( #открытые ноздри/закрытые ноздри
            face_characteristic.nose_nostrils_type,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        #characteristic( #большие ноздри/- 
        # не меряем пока
        #    face_characteristic.,
        #    characteristic_indicator.mild_characteristic,
        #),
        #не меряем мы пока уши
        #characteristic( #развернутые уши/прижатые уши
        #    face_characteristic.profile_forehead_evenness,
        #    characteristic_indicator.mild_characteristic,
        #),
        characteristic( #большой рот/маленький рот
            face_characteristic.mouth_width,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        )

        # профиль
    ]
    risk_appetite_set = [ # склонность к риску
        # фас
        characteristic( #высокая носогубная зона/низкая носогубная зона
            face_characteristic.nasolabial_zone,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        characteristic( #большой рот/маленький рот
            face_characteristic.mouth_width,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        characteristic( #высокая челюсть/легкая челюсть
            face_characteristic.jaw_weight,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        characteristic( #длинное лицо/круглое лицо
            face_characteristic.face_height,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        characteristic( #тонкие губы/-
            face_characteristic.upper_lip_height,
            chracteristic_value(
                strong = None,
                moderate = None,
                mild = 1
            ),
            facet_type
        ),
        # профиль
        characteristic( #выдвинутая челюсть/челюсть назад - ?
        # (возможно перепутаны значения для определния вперед или назад челюсть)
            face_characteristic.profile_jaw_trend,
            chracteristic_value(
                strong = -1,
                moderate = None,
                mild = 1
            ),
            profile_type
        ),
        characteristic( #скошенный лоб/выдающийся лоб
            face_characteristic.profile_forehead_evenness,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            profile_type
        )
    ]
    intellectual_abilities_set = [ # интеллектуальные способности
        # фас
        characteristic( #высокий нос/низкий нос
            face_characteristic.nose_height,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        characteristic( #высокий лоб/узкий лоб
            face_characteristic.forehead_height,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        characteristic( #длинное лицо/круглое лицо
            face_characteristic.face_height,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            facet_type
        ),
        #шишки в зоне сборки на лбу/-  ?
        # профиль
        #characteristic( #большие уши/маленькие уши
        #    face_characteristic.,
        #    characteristic_indicator.strong_characteristic,
        #),
        characteristic( #длинный нос/короткий нос
            face_characteristic.profile_nose_length,
            chracteristic_value(
                strong = 1,
                moderate = None,
                mild = -1
            ),
            profile_type
        )
    ]
    reference_set = [ # референция
        # фас

        # профиль
    ]


class AnalyzeMethods:
    # отдельные функи для каждой части рыла
    @staticmethod
    def getEyeParams(points):
        (left, right, top, bottom) = utils.getExtremePoints(points)
        (heightTop, center) = utils.getPerpendAndLen(top[1], left[1], right[1])
        (heightBottom, center) = utils.getPerpendAndLen(bottom[1], left[1], right[1])
        height = heightTop + heightBottom
        width = utils.getVectorLen(left[1], right[1])

        return {"left": left, "right": right, "top": top, "bottom": bottom, "heightTop": heightTop,
                "heightBottom": heightBottom, "height": height, "width": width, "center": center}

    @staticmethod
    def getMouthParams(points):
        (left, right, top, bottom) = utils.getExtremePoints(points)
        width = utils.getVectorLen(left[1], right[1])
        dt = dict(points)
        # хардкод индексов
        heightTop = ((dt[62][1] - dt[51][1]) + (dt[64][1] - dt[53][1])) / 2
        heightBottom = ((dt[59][1] - dt[68][1]) + (dt[57][1] - dt[66][1]) + (dt[58][1] - dt[67][1])) / 3
        height = heightTop + heightBottom
        center = utils.getMiddleCoords(left[1], right[1])
        return {"left": left, "right": right, "top": top, "bottom": bottom, "heightTop": heightTop,
                "heightBottom": heightBottom, "height": height, "width": width, "center": center}

    @staticmethod
    def getEyeBrowParams(points):
        (left, right, top, bottom) = utils.getExtremePoints(points)
        width = utils.getVectorLen(left[1], right[1])
        (height, center) = utils.getPerpendAndLen(bottom[1], left[1], right[1])
        return {"left": left, "right": right, "top": top, "bottom": bottom, "height": height, "width": width,
                "center": center}

    @staticmethod
    def getJawParams(points):
        (left, right, top, bottom) = utils.getExtremePoints(points)
        width = right[1][0] - left[1][0]
        center = utils.getMiddleCoords(left[1], right[1])
        return {"left": left, "right": right, "top": top, "bottom": bottom, "width": width, "center": center}

    @staticmethod
    def getForeheadParams(points):
        (left, right, top, bottom) = utils.getExtremePoints(points)
        width = right[1][0] - left[1][0]
        center = utils.getMiddleCoords(left[1], right[1])
        return {"left": left, "right": right, "top": top, "bottom": bottom, "width": width, "center": center}

    @staticmethod
    def getResult(value=None, minKoef=None, maxKoef=None):
        if value >= maxKoef:
            res = characteristic_indicator.strong_characteristic.value
        elif minKoef is None:
            # Значит без промежуточного значения (большой, маленький)
            res = characteristic_indicator.mild_characteristic.value
        elif value > minKoef:
            res = characteristic_indicator.moderate_characteristic.value
        else:
            res = characteristic_indicator.mild_characteristic.value

        return res



class Analyze:
    @staticmethod
    def __get_shape_result__(analyze_result):
        if len(analyze_result) != 1:
            result = {
                "result": "error"
            }
            if len(analyze_result) == 0:
                result["description"] = "Shape not found"
            else:
                result["description"] = "Found more than one shape"
        else:
            result = {
                "result": "ok",
                "recognize": analyze_result[0]
            } 
        
        return result
    
    @staticmethod
    def __get_general_result__(characteristic_set, facet, profile):
        b = 0
        total_max = 0
        total_min = 0
        charact = {}
        for c in characteristic_set.value:
            if c.type == facet_type:
                if len(facet) == 1:
                    if c.name.value in facet[0]:
                        if c.values.value[facet[0][c.name.value]["result"]] != None:
                            b += c.values.value[facet[0][c.name.value]["result"]]
                    else:
                        continue
                else:
                    continue

            if c.type == profile_type:
                if len(profile) == 1:
                    if c.name.value in profile[0]:
                        if c.values.value[profile[0][c.name.value]["result"]] != None:
                            b += c.values.value[profile[0][c.name.value]["result"]]
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
                
            for k, v in c.values.value.items():
                if v != None:
                    if v < 0 :
                        total_min += v
                    else:
                        total_max += v
   
        charact["value"] = b 
        charact["range_min"] = total_min
        charact["range_max"] = total_max

        return charact


    @staticmethod
    def __get_general_results__(facet, profile):
        result = {}

        # Передаем в ответе насколько все хорошо отдетектило анфас
        f = {}
        if len(facet) != 1:
            f["result"] = "error"
            if len(facet) == 0:    
                f["description"] = "Shape not found"
            else:
                f["description"] = "Found more than one shape"

        else:
            f["result"] = "ok"

        result["facet"] = f

        # Передаем в ответе насколько все хорошо отдетектило профиль
        p = {}
        if len(profile) != 1:
            p["result"] = "error"
            if len(profile) == 0:    
                p["description"] = "Shape not found"
            else:
                p["description"] = "Found more than one shape"

        else:
            p["result"] = "ok"

        result["profile"] = p
            

        result["characteristic"] = {}

        result["characteristic"][general_characteristic.ambitions.value] = Analyze.__get_general_result__(group_face_characteristic.ambitions_set, facet, profile)
        result["characteristic"][general_characteristic.nervous_system.value] = Analyze.__get_general_result__(group_face_characteristic.nervous_system_set, facet, profile)
        result["characteristic"][general_characteristic.behavior.value] = Analyze.__get_general_result__(group_face_characteristic.behavior_set, facet, profile)
        result["characteristic"][general_characteristic.perception_of_information.value] = Analyze.__get_general_result__(group_face_characteristic.perception_of_information_set, facet, profile)
        result["characteristic"][general_characteristic.risk_appetite.value] = Analyze.__get_general_result__(group_face_characteristic.risk_appetite_set, facet, profile)
        result["characteristic"][general_characteristic.intellectual_abilities.value] = Analyze.__get_general_result__(group_face_characteristic.intellectual_abilities_set, facet, profile)
        result["characteristic"][general_characteristic.reference.value] = Analyze.__get_general_result__(group_face_characteristic.reference_set, facet, profile)
        
        return result

    @staticmethod
    def analyze(facet_result, profile_result):
        result = {
            "result": "ok",
            "data": {
                #"facet" : Analyze.__get_shape_result__(facet_result),
                #"profile": Analyze.__get_shape_result__(profile_result),
                "characteristic": Analyze.__get_general_results__(facet_result, profile_result)
            }    
        }
        
        return result




class AnalyzeFacet:
    def __init__(self):
        self.facePoins = None

        self.rightEye = None
        self.leftEye = None
        self.leftBrow = None
        self.rightBrow = None
        self.mouth = None
        self.jaw = None
        self.forehead = None
        # self.noseWrinkle = None

    def analyze(self, facePoints):
        self.facePoins = facePoints
        self.result = {}
        self.__compute__()
        return self.result

    def __compute__(self):
        self.rightEye = AnalyzeMethods.getEyeParams(self.facePoins["right_eye"])
        self.leftEye = AnalyzeMethods.getEyeParams(self.facePoins["left_eye"])
        self.leftBrow = AnalyzeMethods.getEyeBrowParams(self.facePoins["left_eyebrow"])
        self.rightBrow = AnalyzeMethods.getEyeBrowParams(self.facePoins["right_eyebrow"])
        self.mouth = AnalyzeMethods.getMouthParams(self.facePoins["mouth"])
        self.jaw = AnalyzeMethods.getJawParams(self.facePoins["jaw"] + self.facePoins["forehead"])
        self.forehead = AnalyzeMethods.getForeheadParams(self.facePoins["forehead"])
        # self.noseWrinkle = self.facePoins["noseWrinkleRight"] + self.facePoins["noseWrinkleLeft"]

        self.__faceCompute__()
        self.__eyeCompute__()
        self.__eyebrowCompute__()
        self.__mouthCompute__()
        self.__noduleCompute__()
        self.__chinCompute__()
        self.__jawCompute__()
        self.__nasolabialZoneCompute__()
        self.__noseCompute__()
        self.__foreheadCompute__()
        self.__noseWrinkleCompute__()
        self.__mouthWrinkleCompute__()
        self.__eyeWrinkleCompute__()
        self.__cheekboneWrinkleCompute__()
        self.__nosebridgecentralWrinkleCompute__()
        self.__nosebridgeWrinkleCompute__()

    def __nosebridgecentralWrinkleCompute__(self):
        b1 = self.facePoins["nosebridgecentralWrinkle"]['length'] > 0
        if b1:
            res = characteristic_indicator.strong_characteristic.value
        else:
            res = characteristic_indicator.mild_characteristic.value
        self.result[face_characteristic.nosebridgecentral_wrinkle.value] = {"result": res, "value": 0}


    def __nosebridgeWrinkleCompute__(self):
        b1 = self.facePoins["nosebridgeWrinkleLeft"]['length'] > 0
        b2 = self.facePoins["nosebridgeWrinkleRight"]['length'] > 0
        if b1 and b2:
            res = characteristic_indicator.strong_characteristic.value
        else:
            if b1 or b2:
                res = characteristic_indicator.moderate_characteristic.value
            else:
                res = characteristic_indicator.mild_characteristic.value
        self.result[face_characteristic.nosebridge_wrinkle.value] = {"result": res, "value": 0}

    def __eyeWrinkleCompute__(self):
        b1 = self.facePoins["eyeWrinkleRight"]['length'] > 0
        b2 = self.facePoins["eyeWrinkleLeft"]['length'] > 0
        if b1 and b2:
            res = characteristic_indicator.strong_characteristic.value
        else:
            if b1 or b2:
                res = characteristic_indicator.moderate_characteristic.value
            else:
                res = characteristic_indicator.mild_characteristic.value
        self.result[face_characteristic.eye_wrinkle.value] = {"result": res, "value": 0}

    def __cheekboneWrinkleCompute__(self):
        b1 = self.facePoins["cheekboneWrinkleRight"]['length'] > 0
        b2 = self.facePoins["cheekboneWrinkleLeft"]['length'] > 0
        if b1 and b2:
            res = characteristic_indicator.strong_characteristic.value
        else:
            if b1 or b2:
                res = characteristic_indicator.moderate_characteristic.value
            else:
                res = characteristic_indicator.mild_characteristic.value
        self.result[face_characteristic.cheekbone_wrinkle.value] = {"result": res, "value": 0}


    def __noseWrinkleCompute__(self):
        koef = 0
        val1 = min(self.facePoins["noseWrinkleRight"]['length'], self.facePoins["noseWrinkleLeft"]['length'])

        val2 = max(self.facePoins["noseWrinkleRight"]['length'], self.facePoins["noseWrinkleLeft"]['length'])
        if (val1 > -1) and (val2 > -1) and (val1/val2 > const.config.getfloat('Wrinkle.NoseWrinkle', 'len_diff', fallback=const.NOSE_WRINKLE_LENGTH_DIFF)):
            #val = (val1 + val2)/2
            koef = (self.facePoins["noseWrinkleRight"]['koef'] + self.facePoins["noseWrinkleLeft"]['koef'])/2

            res = AnalyzeMethods.getResult(koef, const.config.getfloat('Wrinkle.NoseWrinkle', 'koef_min',
                                                                          fallback=const.NOSE_WRINKLE_KOEF_MIN),
                                             const.config.getfloat('Wrinkle.NoseWrinkle', 'koef_max',
                                                                          fallback=const.NOSE_WRINKLE_KOEF_MAX))

        else:
            #descr = const.NOSE_WRINKLE_NO_WRINKLE_TEXT
            res = characteristic_indicator.mild_characteristic.value

        self.result[face_characteristic.nose_wrinkle.value] = {"result": res, "value":koef}

    def __mouthWrinkleCompute__(self):
        val = 0
        val1 = min(self.facePoins["mouthWrinkleRight"]['length'], self.facePoins["mouthWrinkleLeft"]['length'])

        val2 = max(self.facePoins["mouthWrinkleRight"]['length'], self.facePoins["mouthWrinkleLeft"]['length'])
        
        if (val1 > -1) and (val2 > -1) and (val1/val2 > const.config.getfloat('Wrinkle.MouthWrinkle', 'len_diff', fallback=const.MOUTH_WRINKLE_LENGTH_DIFF)):
            val = (val1 + val2)/2
            #descr = const.MOUTH_WRINKLE_WRINKLE_TEXT
            res = characteristic_indicator.strong_characteristic.value
        else:
            #descr = const.MOUTH_WRINKLE_NO_WRINKLE_TEXT
            res = characteristic_indicator.mild_characteristic.value

        # self.result[face_characteristic.mouth_wrinkle.value] = {"description": descr, "result": val}

        self.result[face_characteristic.mouth_wrinkle.value] = {"result": res, "value": val}


    def __foreheadCompute__(self):
        # высота лба
        tmp = dict(self.facePoins["forehead"] + self.facePoins["left_eyebrow"] + self.facePoins["right_eyebrow"])
        val1 = utils.getYDiff(self.forehead["top"][1], tmp[20]) / self.jaw["width"]
        val2 = utils.getYDiff(self.forehead["top"][1], tmp[25]) / self.jaw["width"]
        val = (val1 + val2) / 2

        res = AnalyzeMethods.getResult(value = val,
                                        minKoef=const.config.getfloat('Recognition.Forehead', 'forehead_height_small',
                                                                      fallback=const.FOREHEAD_HEIGHT_SMALL),
                                        maxKoef=const.config.getfloat('Recognition.Forehead', 'forehead_height_big',
                                                                      fallback=const.FOREHEAD_HEIGHT_BIG))
        #+
        self.result[face_characteristic.forehead_height.value] = {"result": res, "value":val}

    def __eyeCompute__(self):
        # Размер глаз
        averEyeWidth = (self.leftEye["width"] + self.rightEye["width"]) / 2
        averEyeHeight = (self.leftEye["height"] + self.rightEye["height"]) / 2

        val = averEyeWidth / self.jaw["width"]

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Eyes', 'eye_small',
                                                                      fallback=const.EYES_SMALL),
                                        maxKoef=const.config.getfloat('Recognition.Eyes', 'eye_big',
                                                                      fallback=const.EYES_BIG))

        self.result[face_characteristic.eye_size.value] = {"result": res, "value":val}

        val = averEyeHeight / averEyeWidth

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Eyes', 'eye_height_small',
                                                                      fallback=const.EYES_HEIGHT_SMALL),
                                        maxKoef=const.config.getfloat('Recognition.Eyes', 'eye_height_big',
                                                                      fallback=const.EYES_HEIGHT_BIG))

        self.result[face_characteristic.eye_height_size.value] = {"result": res, "value":val}

    def __faceCompute__(self):
        # Считаем длину лица
        y = self.leftBrow["top"][1][1] + (
                self.leftEye["top"][1][1] - self.leftBrow["top"][1][1]) / 2  # точка между глазом и бровью
        gauging1 = (self.mouth["center"][1] - y) / self.jaw["width"]
        y = self.rightBrow["top"][1][1] + (
                self.rightEye["top"][1][1] - self.rightBrow["top"][1][1]) / 2  # точка между глазом и бровью
        gauging2 = (self.mouth["center"][1] - y) / self.jaw["width"]
        val = (gauging1 + gauging2) / 2

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Face', 'face_round',
                                                                      fallback=const.FACE_ROUND),
                                        maxKoef=const.config.getfloat('Recognition.Face', 'face_long',
                                                                      fallback=const.FACE_LONG))
        #+
        self.result[face_characteristic.face_height.value] = {"result": res, "value":val}

    def __mouthCompute__(self):
        # Считаем ширину
        val = self.mouth["width"] / self.jaw["width"]

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Mouth', 'mouth_small',
                                                                      fallback=const.MOUTH_SMALL),
                                        maxKoef=const.config.getfloat('Recognition.Mouth', 'mouth_big',
                                                                      fallback=const.MOUTH_BIG))
        #+
        self.result[face_characteristic.mouth_width.value] = {"result": res, "value":val}

        # Считаем высоту верхней губы
        val = self.mouth["heightTop"] / self.jaw["width"]

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Mouth', 'mouth_short_lip',
                                                                      fallback=const.MOUTH_SHORT_LIP),
                                        maxKoef=const.config.getfloat('Recognition.Mouth', 'mouth_wide_lip',
                                                                      fallback=const.MOUTH_WIDE_LIP))
        #+
        self.result[face_characteristic.upper_lip_height.value] = {"result": res, "value":val}

    def __noduleCompute__(self):
        # Считаем желвак
        tmp = dict(self.facePoins["jaw"])
        val = utils.getAngle(tmp[4], tmp[5], tmp[6])


        res = AnalyzeMethods.getResult(value=val*(-1),
                                       #значениея в обратную сторону считаются
                                       minKoef=const.config.getfloat('Recognition.Nodule', 'nodule_angle',
                                                                     fallback=const.NODULE_ANGLE_MIN)*(-1),
                                       maxKoef=const.config.getfloat('Recognition.Nodule', 'nodule_angle',
                                                                      fallback=const.NODULE_ANGLE_MAX)*(-1))
        #+
        self.result[face_characteristic.nodule.value] = {"result": res, "value":val}

    def __chinCompute__(self):
        # Считаем подбородок
        pass

    def __jawCompute__(self):
        # Считаем челюсть
        # ширина

        tmp = dict(self.facePoins["jaw"] + self.facePoins["mouth"])
        val = utils.getAngle(tmp[6], tmp[9], tmp[12])

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Jaw', 'chin_width_small',
                                                                      fallback=const.CHIN_WIDTH_SMALL),
                                        maxKoef=const.config.getfloat('Recognition.Jaw', 'chin_width_big',
                                                                      fallback=const.CHIN_WIDTH_BIG))
        #+
        self.result[face_characteristic.chin_width.value] = {"result": res, "value":val}

        # вес

        val = utils.getYDiff(tmp[67], tmp[9]) / self.jaw["width"]
        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Jaw', 'jaw_weight_small',
                                                                      fallback=const.JAW_WEIGHT_SMALL),
                                        maxKoef=const.config.getfloat('Recognition.Jaw', 'jaw_weight_big',
                                                                      fallback=const.JAW_WEIGHT_BIG))
        # +
        self.result[face_characteristic.jaw_weight.value] = {"result": res, "value":val}

    def __nasolabialZoneCompute__(self):
        # Считаем носогубную зону
        tmp = dict(self.facePoins["jaw"] + self.facePoins["mouth"] + self.facePoins["nose"])
        noseToMouth = utils.getYDiff(tmp[34], tmp[52])

        val = noseToMouth / self.jaw["width"]

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.NasolabialZone',
                                                                      'nasolabial_zone_small',
                                                                      fallback=const.NASOLABIAL_ZONE_SMALL),
                                        maxKoef=const.config.getfloat('Recognition.NasolabialZone',
                                                                      'nasolabial_zone_big',
                                                                      fallback=const.NASOLABIAL_ZONE_BIG))
        #+
        self.result[face_characteristic.nasolabial_zone.value] = {"result": res, "value":val}

    def __noseCompute__(self):
        # Считаем параметры носа
        tmp = dict(self.facePoins["nose"] + self.facePoins["nose_contour"])

        noseH = utils.getYDiff(tmp[28], tmp[34])
        val = noseH / self.jaw["width"]

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Nose', 'nose_height_small',
                                                                      fallback=const.NOSE_HEIGHT_SMALL),
                                        maxKoef=const.config.getfloat('Recognition.Nose', 'nose_height_big',
                                                                      fallback=const.NOSE_HEIGHT_BIG))
        #+
        self.result[face_characteristic.nose_height.value] = {"result": res, "value":val}

        noseW = utils.getXDiff(tmp[73], tmp[76])
        # val = noseW/self.jaw["width"]
        val = noseW / noseH

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Nose', 'nose_width_small',
                                                                      fallback=const.NOSE_WIDTH_SMALL),
                                        maxKoef=const.config.getfloat('Recognition.Nose', 'nose_width_big',
                                                                      fallback=const.NOSE_WIDTH_BIG))
        #+
        self.result[face_characteristic.nose_width.value] = {"result": res, "value":val}

        val = utils.getAngle(tmp[73], tmp[34], tmp[76])

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Nose', 'nostrils_cut',
                                                                      fallback=const.NOSE_NOSTRIL_CUT),
                                        maxKoef=const.config.getfloat('Recognition.Nose', 'nostrils_flat',
                                                                      fallback=const.NOSE_NOSTRIL_FLAT))
        #+!
        self.result[face_characteristic.nose_nostrils_form.value] = {"result": res, "value":val}

        # переносица
        val = utils.getXDiff(tmp[69], tmp[70]) / self.jaw["width"]

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Nose', 'nose_bridge_min',
                                                                      fallback=const.NOSE_BRIDGE_MIN),
                                        maxKoef=const.config.getfloat('Recognition.Nose', 'nose_bridge_max',
                                                                      fallback=const.NOSE_BRIDGE_MAX))
        #+
        self.result[face_characteristic.nose_bridge.value] = {"result": res, "value":val}

        # спинка носа
        val = utils.getXDiff(tmp[71], tmp[72]) / self.jaw["width"]

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Nose', 'nose_nasal_bridge_min',
                                                                      fallback=const.NOSE_NASAL_BRIDGE_MIN),
                                        maxKoef=const.config.getfloat('Recognition.Nose', 'nose_nasal_bridge_max',
                                                                      fallback=const.NOSE_NASAL_BRIDGE_MAX))
        #+
        self.result[face_characteristic.nose_nasal_bridge.value] = {"result": res, "value":val}

        # открытые/закрытые ноздри
        val1 = utils.getAngle(tmp[74], tmp[32],
                              tmp[33])  # utils.getYDiff(tmp[74], tmp[33])/utils.getXDiff(tmp[73], tmp[76])
        val2 = utils.getAngle(tmp[75], tmp[36],
                              tmp[35])  # utils.getYDiff(tmp[75], tmp[35]) / utils.getXDiff(tmp[73], tmp[76])

        val = (val1 + val2) / 2

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Nose', 'nostrils_closed',
                                                                      fallback=const.NOSE_NOSTRIL_CLOSE),
                                        maxKoef=const.config.getfloat('Recognition.Nose', 'nostrils_opened',
                                                                      fallback=const.NOSE_NOSTRIL_OPEN))

        self.result[face_characteristic.nose_nostrils_type.value] = {"result": res, "value":val}

        #Добавить размер ноздрей (31-32) и (34-35) нумерация +1 идет
        val = (utils.getXDiff(tmp[32], tmp[33]) + utils.getXDiff(tmp[35], tmp[36])) / 2 / self.jaw["width"]
        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Nose', 'nostrils_width_small',
                                                                      fallback=const.NOSE_NOSTRIL_WIDTH_SMALL),
                                        maxKoef=const.config.getfloat('Recognition.Nose', 'nostrils_width_big',
                                                                      fallback=const.NOSE_NOSTRIL_WIDTH_BIG))
        self.result[face_characteristic.nose_nostrils_width.value] = {"result": res, "value": val}


        # ширина крыльев носа

        val = (utils.getXDiff(tmp[73], tmp[74]) + utils.getXDiff(tmp[75], tmp[76])) / 2 /self.jaw["width"] #/ utils.getXDiff(tmp[73],
                                                                                        #                 tmp[76])

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Nose', 'nose_wings_width_small',
                                                                      fallback=const.NOSE_WINGS_WIDTH_SMALL),
                                        maxKoef=const.config.getfloat('Recognition.Nose', 'nose_wings_width_big',
                                                                      fallback=const.NOSE_WINGS_WIDTH_BIG))

        self.result[face_characteristic.nose_wings_width.value] = {"result": res, "value":val}

    def __eyebrowCompute__(self):
        tmp = dict(
            self.facePoins["left_eye"] + self.facePoins["right_eye"] + self.facePoins["left_eyebrow"] + self.facePoins[
                "right_eyebrow"] + self.facePoins["right_eyebrow_bottom"] + self.facePoins["left_eyebrow_bottom"])

        l_eye = (utils.getYDiff(tmp[77], tmp[38]) + utils.getYDiff(tmp[78], tmp[39])) / 2
        r_eye = (utils.getYDiff(tmp[80], tmp[45]) + utils.getYDiff(tmp[81], tmp[44])) / 2

        aver_eye = (l_eye + r_eye) / 2

        val = aver_eye / self.jaw["width"]

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Eyebrow', 'eyebrow_height_small',
                                                                      fallback=const.EYEBROW_HEIGHT_SMALL),
                                        maxKoef=const.config.getfloat('Recognition.Eyebrow', 'eyebrow_height_big',
                                                                      fallback=const.EYEBROW_HEIGHT_BIG))
        #+
        self.result[face_characteristic.eyebrow_height.value] = {"result": res, "value":val}

        # val_left = (utils.getYDiff(tmp[19], tmp[77]) + utils.getYDiff(tmp[20], tmp[78]) + utils.getYDiff(tmp[21],
        #                                                                                                  tmp[
        #                                                                                                      79])) / 3 # / utils.getXDiff(
            # tmp[18], tmp[22])
        val_left = utils.getYDiff(tmp[20], tmp[78])

        # val_right = (utils.getYDiff(tmp[24], tmp[80]) + utils.getYDiff(tmp[25], tmp[81]) + utils.getYDiff(tmp[26],
        #                                                                                                   tmp[
        #                                                                                                       82])) / 3 # / utils.getXDiff(
            # tmp[23], tmp[27])

        val_right = utils.getYDiff(tmp[25], tmp[81])
        val = (val_left + val_right) / 2 / self.jaw["width"]

        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Eyebrow', 'eyebrow_thickness_small',
                                                                      fallback=const.EYEBROW_THICKNESS_SMALL),
                                        maxKoef=const.config.getfloat('Recognition.Eyebrow', 'eyebrow_thickness_big',
                                                                      fallback=const.EYEBROW_THICKNESS_BIG))
        #+
        self.result[face_characteristic.eyebrow_thiсkness.value] = {"result": res, "value":val}


class AnalyzeProfile:
    # -1 - не выражена
    # 0 - средне-слабо выражена
    # 1 - выражена

    def __init__(self):
        self.facePoins = None

    def analyze(self, facePoints):
        self.facePoins = facePoints
        self.result = {}
        self.__compute__()
        return self.result

    def __compute__(self):
        self.__foreheadCompute__()
        self.__noseCompute__()
        self.__jawCompute__()
        self.__chinСompute__()

    def __noseCompute__(self):
        tmp = dict(self.facePoins["profile"])
        # Нос с горбинкой, нос прогнутый
        val = utils.getAngle(tmp[6], tmp[7], tmp[8])
        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Nose', 'profile_nose_evenness_min',
                                                                      fallback = const.PROFILE_NOSE_EVENNESS_MIN),
                                        maxKoef=const.config.getfloat('Recognition.Nose', 'profile_nose_evenness_max',
                                                                      fallback = const.PROFILE_NOSE_EVENNESS_MAX))

        self.result[face_characteristic.profile_nose_evenness.value] = {"result": res, "value":val}


        #для профиля открытые/закрытые ноздри
        val = utils.getAngle(tmp[9], tmp[10], tmp[12])
        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Nose', 'profile_nostrils_type_min',
                                                                      fallback = const.PROFILE_NOSTRILS_TYPE_MIN),
                                        maxKoef=const.config.getfloat('Recognition.Nose', 'profile_nostrils_type_max',
                                                                      fallback = const.PROFILE_NOSTRILS_TYPE_MAX))
        self.result[face_characteristic.profile_nostrils_type.value] = {"result": res, "value": val}


        # Короткий, длинный(9:10/6:9)
        val = utils.getXDiff(tmp[9],tmp[10])/utils.getYDiff(tmp[6], tmp[9])
        res = AnalyzeMethods.getResult(value=val,
                                        minKoef=const.config.getfloat('Recognition.Nose', 'profile_nose_length_min',
                                                                      fallback = const.PROFILE_NOSE_LENGTH_MIN),
                                        maxKoef=const.config.getfloat('Recognition.Nose', 'profile_nose_length_max',
                                                                      fallback = const.PROFILE_NOSE_LENGTH_MAX))
        #+
        self.result[face_characteristic.profile_nose_length.value] = {"result": res, "value":val}




    def __foreheadCompute__(self):
        tmp = dict(self.facePoins["profile"])
        # Скошенный, выдающийся
        val = utils.getAngle(tmp[3],tmp[5], tmp[10])
        # Проверка в какую сторону смотрит угол
        if utils.pointRelativelyStraight(tmp[5],tmp[3], tmp[10]) == -1:
            val = 360-val

        res = AnalyzeMethods.getResult(value = val,
                                        minKoef=const.config.getfloat('Recognition.Forehead', 'profile_forehead_evenness_min',
                                                                      fallback = const.PROFILE_FORHEAD_EVENNESS_MIN),
                                        maxKoef=const.config.getfloat('Recognition.Forehead', 'profile_forehead_evenness_max',
                                                                      fallback = const.PROFILE_FORHEAD_EVENNESS_MAX))
        #посмотреть не перепутано ли в результате скошенный или выдающийся лоб
        #+ Добавить проверку в какую сторону смотрит угол - точка 5 относительно прямой 3-10 слева или справа?
        self.result[face_characteristic.profile_forehead_evenness.value] = {"result": res, "value":val}

    def __jawCompute__(self):
        tmp = dict(self.facePoins["profile"])
        # Челюсть назад, челюсть вперед
        val = utils.getAngle(tmp[5],tmp[10], tmp[17])
        res = AnalyzeMethods.getResult(value = val,
                                        minKoef=const.config.getfloat('Recognition.Jaw', 'profile_jaw_trend_min',
                                                                      fallback = const.PROFILE_JAW_TREND_MIN),
                                        maxKoef=const.config.getfloat('Recognition.Jaw', 'profile_jaw_trend_max',
                                                                      fallback = const.PROFILE_JAW_TREND_MAX))     
        #+
        #посмотреть не перепутано ли в результате
        self.result[face_characteristic.profile_jaw_trend.value] = {"result": res, "value":val}
        

    def __chinСompute__(self):
        tmp = dict(self.facePoins["profile"])
        # Подбородок есть, нету (губа валиком?) чтобі убрать губу валиком - берем отрезок 5-10 и 17-18 и меряем между ними угол
        val = utils.getAngle(tmp[16],tmp[17], tmp[18])
        res = AnalyzeMethods.getResult(value = val,
                                        minKoef=const.config.getfloat('Recognition.Chin', 'profile_chin_presence_min',
                                                                      fallback = const.PROFILE_CHIN_PRESENCE_MIN),
                                        maxKoef=const.config.getfloat('Recognition.Chin', 'profile_chin_presence_max',
                                                                      fallback = const.PROFILE_CHIN_PRESENCE_MAX))  
        self.result[face_characteristic.profile_chin_presence.value] = {"result": res, "value":val}

