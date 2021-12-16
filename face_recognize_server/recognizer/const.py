import configparser

config = configparser.ConfigParser()
config.read('/recognizer/Processing/recognision.ini')

# типа константы
FACE_ROUND = 0.54
FACE_LONG = 0.59

MOUTH_SMALL = 0.33
MOUTH_BIG = 0.39
MOUTH_WIDE_LIP = 0.051
MOUTH_SHORT_LIP = 0.04

NODULE_ANGLE_MIN = 160
NODULE_ANGLE_MAX = 170

EYES_BIG = 0.18
EYES_SMALL = 0.155

EYES_HEIGHT_BIG = 0.36
EYES_HEIGHT_SMALL = 0.25

EYEBROW_HEIGHT_BIG = 0.09
EYEBROW_HEIGHT_SMALL = 0.075

EYEBROW_THICKNESS_SMALL = 0.035
EYEBROW_THICKNESS_BIG = 0.045

CHIN_WIDTH_BIG = 135
CHIN_WIDTH_SMALL = 125

JAW_WEIGHT_BIG = 0.315
JAW_WEIGHT_SMALL = 0.27

NASOLABIAL_ZONE_BIG = 0.11
NASOLABIAL_ZONE_SMALL = 0.08

NOSE_HEIGHT_BIG = 0.38
NOSE_HEIGHT_SMALL = 0.34

NOSE_WIDTH_BIG = 0.77
NOSE_WIDTH_SMALL = 0.7

NOSE_NOSTRIL_CUT = 125
NOSE_NOSTRIL_FLAT = 130

NOSE_BRIDGE_MIN = 0.08
NOSE_BRIDGE_MAX = 0.094

NOSE_NASAL_BRIDGE_MIN = 0.08
NOSE_NASAL_BRIDGE_MAX = 0.094

FOREHEAD_HEIGHT_SMALL = 0.36
FOREHEAD_HEIGHT_BIG = 0.42

NOSE_NOSTRIL_CLOSE = 48
NOSE_NOSTRIL_OPEN = 63

NOSE_NOSTRIL_WIDTH_SMALL = 10
NOSE_NOSTRIL_WIDTH_BIG = 20

NOSE_WINGS_WIDTH_SMALL = 0.035
NOSE_WINGS_WIDTH_BIG = 0.058

# Профиль
PROFILE_NOSE_EVENNESS_MAX = 30 # нос прогнутый
PROFILE_NOSE_EVENNESS_MIN = 25 # нос с горбинкой


PROFILE_NOSE_LENGTH_MAX = 0.45  # нос длинный
PROFILE_NOSE_LENGTH_MIN = 0.39  # нос короткий

PROFILE_NOSTRILS_TYPE_MIN = 10 #закрытые ноздри в профиль
PROFILE_NOSTRILS_TYPE_MAX = 50 #открытые ноздри в профиль


PROFILE_FORHEAD_EVENNESS_MAX = 175 # выдающийся лоб 
PROFILE_FORHEAD_EVENNESS_MIN = 168 # скошенный лоб 

PROFILE_JAW_TREND_MAX = 168 # Челюсть вперед
PROFILE_JAW_TREND_MIN = 160 # Челюсть назад

PROFILE_CHIN_PRESENCE_MAX = 155 # Подбородка нету
PROFILE_CHIN_PRESENCE_MIN = 135 # Подбородок есть

FACET_SHAPE_PREDICTOR = "./recognizer/Predictors/FacePredictor.dat"
PROFILE_SHAPE_PREDICTOR = "./recognizer/Predictors/ProfilePredictor.dat"

PROFILE_DETECTOR = "./recognizer/Detectors/detector_profile.svm"

PREDICTOR_THREADS = 20  # количество независимых потоков распознаваня
USE_DEBUG_DRAW = True

# константы дескрипшинов

# Лицо
FACE_SHAPE_ROUND_TEXT = "Интуитивное мышление, " \
                        "действует по ощущениям, " \
                        "быстро принимает решение, " \
                        "не любит жестких схем, " \
                        "легко переключается, " \
                        "умеет хорошо подстраиваться"  # Круглое лицо
FACE_SHAPE_ELLIPSE_TEXT = "Medium drawn face"  # Средневытянутое лицо
FACE_SHAPE_LONG_TEXT = "Логическое мышление, " \
                       "заложник схем, " \
                       "плохо видит альтернативу, " \
                       "долго решает, " \
                       "медленно перестраивается"  # Длинное лицо

# Глаза
EYES_SIZE_BIG_TEXT = "Видит ситуацию во всем многообразии, " \
                     "планируетстратегически, с учетом разных вариантов развития событий"  # Большие глаза
EYES_SIZE_MIDDLE_TEXT = "Medium eyes"  # Средние глаза
EYES_SIZE_SMALL_TEXT = "Хитрый, " \
                       "меняет договоренности, " \
                       "действует тактически"  # Маленькие глаза

EYES_HEIGHT_BIG_TEXT = "Не загадывает надолго, " \
                       "принимает короткие прямые решения"  # Большая высота глаз
EYES_HEIGHT_MIDDLE_TEXT = "Medium eye height"  # Средняя высота глаз
EYES_HEIGHT_SMALL_TEXT = "Внимательный к мелочам, " \
                         "строит детальные планы"  # Маленькая высота глаз

# Желвак
NODULE_EXPRESSED_TEXT = "Волевой, " \
                        "не пасует перед трудностями, " \
                        "трудолюбивый, " \
                        "работоспособный"  # Желвак выражен
NODULE_NOT_EXPRESSED_TEXT = "Безвольный, " \
                            "плывет по течению"  # Желвак не выражен

# Рот
MOUTH_WIDTH_BIG_TEXT = "Амбициозный, " \
                       "активный, " \
                       "открыт для экспериментов"  # Большой рот
MOUTH_WIDTH_MEDIUM_TEXT = "Medium mouth"  # Средний рот
MOUTH_WIDTH_SMALL_TEXT = "Скромный, " \
                         "разборчивый, " \
                         "нерешительный"  # Маленький рот

# Губы
LIPS_UPPER_LIP_BIG_TEXT = "Хорошо развита интуиция, " \
                          "чувствует опасность и мгновенно реагирует," \
                          "чувствует изменения в собеседнике, ситуации м т.п."  # Пухлая верхняя губа
LIPS_UPPER_LIP_MEDIUM_TEXT = "Medium lip"  # Средняя верхняя губа
LIPS_UPPER_LIP_SMALL_TEXT = "Глух к эмоциям окружающих, " \
                            "не чувствителен к изменениям в собеседнике, ситуации и т.п."  # Тонкая верхняя губа

# Челюсть
JAW_CHIN_WIDTH_BIG_TEXT = "Многозадачный, " \
                          "мобильный, " \
                          "способный к быстрому переключению"  # Большой подбородок
JAW_CHIN_WIDTH_MEDIUM_TEXT = "Medium chin"  # Средний подбородок
JAW_CHIN_WIDTH_SMALL_TEXT = "Целеустремленный, " \
                            "но хорошо концентрируется на чем-то одном"  # Маленький подбородок

JAW_WEIGHT_BIG_TEXT = "Основательный, " \
                      "методичный, " \
                      "упорный, " \
                      "целеустремленный"  # Тяжелая челюсть
JAW_WEIGHT_MEDIUM_TEXT = "Medium jaw"  # Средняя челюсть
JAW_WEIGHT_SMALL_TEXT = "Мобильный, " \
                        "легкий, " \
                        "оперативный, " \
                        "подвижный, " \
                        "'схватывает на  лету'"  # Легкая челюсть

# Носогубная зона
NASOLABIAL_ZONE_BIG_TEXT = "Готов на риск, " \
                           "действует в ситуации неполноты данных, " \
                           "игнорирует тревожные сигналы," \
                           "авантюрист"  # Большая носогубная зона
NASOLABIAL_ZONE_MEDIUM_TEXT = "Medium nasolabial zone"  # Средняя носогубная зона
NASOLABIAL_ZONE_SMALL_TEXT = "Скептик, " \
                             "практичный, " \
                             "избегает риска, " \
                             "пользуется проверенными данными, " \
                             "быстро переходит от слов к делу"  # Маленькая носогубная зона

# Нос
NOSE_HEIGHT_BIG_TEXT = "Вдумчивый, " \
                       "высокие интелектуальные и аналитические способности"  # Высокий нос
NOSE_HEIGHT_MEDIUM_TEXT = "Medium nose"  # Средний нос
NOSE_HEIGHT_SMALL_TEXT = "Поверхностный, " \
                         "невысокие интелектуальные способности"  # Низкий нос

NOSE_WIDTH_BIG_TEXT = "Настойчивый, " \
                      "напористый в получении нужной информации"  # Широкий нос
NOSE_WIDTH_MEDIUM_TEXT = "Medium nose"  # Средний нос
NOSE_WIDTH_SMALL_TEXT = "Деликатный, " \
                        "осторожный при выяснении необходимой информации"  # Узкий нос

NOSE_NOSTRIL_CUT_TEXT = "Импульсивен, " \
                        "действует в условиях не до конца обработанной информации"  # Срезанные ноздри
NOSE_NOSTRIL_CUT_FLAT_TEXT = "Medium nostrils"  # Средние ноздри
NOSE_NOSTRIL_FLAT_TEXT = "Не склонен к импульсивным действиям"  # Ровные ноздри

NOSE_BRIDGE_MIN_TEXT = "Дотошный, " \
                       "вдумчивый, внимателен к нюансам и мелочам"  # Маленькая переносица
NOSE_BRIDGE_MEDIUM_TEXT = "Medium nose bridge"  # Средняя переносица
NOSE_BRIDGE_MAX_TEXT = "Изучает ситуацию поверхностно, " \
                       "легко делегирует полномочия"  # Большая переносица

NOSE_NASAL_BRIDGE_MIN_TEXT = "Истеричный, " \
                             "высокая эмоциональная реакция на внешние раздражители"  # Маленькая спинка носа
NOSE_NASAL_BRIDGE_MEDIUM_TEXT = "Medium nasal bridge"  # Средняя спинка носа
NOSE_NASAL_BRIDGE_MAX_TEXT = "Стрессоустойчивый, " \
                             "нечувствителен к социальным оценкам"  # Большая спинка носа

NOSE_NOSTRIL_CLOSE_TEXT = "Сдержанный, " \
                          "умеет скрывать свои намерения, " \
                          "желания"  # Закрытые ноздри
NOSE_NOSTRIL_MEDIUM_TEXT = "Medium nostrils"  # Средние ноздаи
NOSE_NOSTRIL_OPEN_TEXT = "Инфантильный, " \
                         "непосредственный, " \
                         "открытый, " \
                         "бесхитростный"  # Открытые ноздри

NOSE_WINGS_WIDTH_SMALL_TEXT = "В стрессовой ситуации теряет способность " \
                              "воспринимать и анализировать информацию"  # Маленькие крылья носа
NOSE_WINGS_WIDTH_MEDIUM_TEXT = "Medium wings of the nose"  # Средние крылья носа
NOSE_WINGS_WIDTH_BIG_TEXT = "Воспринимает и анализирует информацию " \
                            "в стрессовой ситуации"  # Большие крылья носа

# Брови
EYEBROW_HEIGHT_HIGH_TEXT = "Фантазер, " \
                           "принимает желаемое за действительное"  # Высокие брови
EYEBROW_HEIGHT_MEDIUM_TEXT = "Medium eyebrow"  # Средние брови
EYEBROW_HEIGHT_LOW_TEXT = "Практичный, " \
                          "живет без иллюзий, " \
                          "предпочитает словам дело"  # Низкие брови

EYEBROW_THICKNESS_LOW_TEXT = "Неудовлетворенный в эмоциональном плане, " \
                             "с высоким самоконтролем, " \
                             "холодный и циничный, " \
                             "делает что нужно, а не то, что хочет"  # тонкие брови
EYEBROW_THICKNESS_MEDIUM_TEXT = "Medium eyebrow"  # средние брови
EYEBROW_THICKNESS_HIGH_TEXT = "Способен на необдуманные поступки, " \
                              "не умеет отказывать своим желаниям, " \
                              "делает то, что хочет"  # толстіе брови

# Лоб
FOREHEAD_HEIGHT_SMALL_TEXT = "Нерациональный"  # Низкий лоб
FOREHEAD_HEIGHT_MIDDLE_TEXT = "Middle forehead"  # Средний лоб
FOREHEAD_HEIGHT_BIG_TEXT = "Рациональный"  # Высокий лоб

#морщина сбоку рта
NOSE_WRINKLE_CANNYPARAM_1 = 60
NOSE_WRINKLE_CANNYPARAM_2 = 100
NOSE_WRINKLE_MIN_LEN_MULTIPLIER = 0.4 #минимальная длина контура относительно высоты прямоугольника распознавания (высота прямоугольника - от верхней до нижней губы) для валидации его как морщины
NOSE_WRINKLE_MAX_LEN_MULTIPLIER = 1.5 #максимальная длина контура относительно высоты прямоугольника распознавания (высота прямоугольника - от верхней до нижней губы) для валидации его как морщины
NOSE_WRINKLE_MIN_X_ANGLE = 60 # минимальный угол контура между осью Х для валидации его как морщины
NOSE_WRINKLE_MAX_Y_ANGLE = 30 # максимальный угол контура между осью Y для валидации его как морщины
NOSE_WRINKLE_LENGTH_DIFF = 0.7 #отношение длины от рта до морщины слева и справа. Если выше, то считаем что морщина выражена. По сути еще одна затычка ложных детектов (волосы, борода)
NOSE_WRINKLE_FACE_DELTA = 0.7 #чтобы отбросить ложные детекты на краю рыла (бывает часто у баб, когда волосы по бокам детекит как морщины)
NOSE_WRINKLE_NO_WRINKLE_TEXT = "Носогубная морщина отсутсвует"
NOSE_WRINKLE_KOEF_MIN = 0.3
NOSE_WRINKLE_KOEF_MAX = 0.5
NOSE_WRINKLE_KOEF_MIN_TEXT = "Носогубная морщина близко"
NOSE_WRINKLE_KOEF_MIDDLE_TEXT = "Носогубная морщина средне"
NOSE_WRINKLE_KOEF_MAX_TEXT = "Носогубная морщина далеко"

#морщина "удлинитель" рта
MOUTH_WRINKLE_CANNYPARAM_1 = 50
MOUTH_WRINKLE_CANNYPARAM_2 = 20
MOUTH_WRINKLE_MIN_LEN_MULTIPLIER = 0.08 #минимальная длина контура относительно высоты прямоугольника распознавания (высота прямоугольника - от верхней до нижней губы) для валидации его как морщины
MOUTH_WRINKLE_MAX_LEN_MULTIPLIER = 1.5 #максимальная длина контура относительно высоты прямоугольника распознавания (высота прямоугольника - от верхней до нижней губы) для валидации его как морщины
MOUTH_WRINKLE_MIN_X_ANGLE = 10 # минимальный угол контура между осью Х для валидации его как морщины
MOUTH_WRINKLE_MAX_Y_ANGLE = 80 # максимальный угол контура между осью Y для валидации его как морщины
MOUTH_WRINKLE_LENGTH_DIFF = 0.5 #отношение длины от рта до морщины слева и справа. Если выше, то считаем что морщина выражена. По сути еще одна затычка ложных детектов (волосы, борода)
MOUTH_WRINKLE_FACE_DELTA = 0.7 #чтобы отбросить ложные детекты на краю рыла (бывает часто у баб, когда волосы по бокам детекит как морщины)
MOUTH_WRINKLE_NO_WRINKLE_TEXT = "Морщина в уголке рта отсутсвует"
MOUTH_WRINKLE_WRINKLE_TEXT = "Морщина в уголке рта есть"

#морщины возле глаз
EYE_WRINKLE_CANNYPARAM_1 = 240
EYE_WRINKLE_CANNYPARAM_2 = 250
EYE_WRINKLE_MIN_LEN_MULTIPLIER = 0.6 #минимальная длина контура относительно высоты прямоугольника распознавания (высота прямоугольника - от верхней до нижней губы) для валидации его как морщины
EYE_WRINKLE_MAX_LEN_MULTIPLIER = 2 #максимальная длина контура относительно высоты прямоугольника распознавания (высота прямоугольника - от верхней до нижней губы) для валидации его как морщины
EYE_WRINKLE_MIN_X_ANGLE = -1 # минимальный угол контура между осью Х для валидации его как морщины
EYE_WRINKLE_MAX_Y_ANGLE = 70 # максимальный угол контура между осью Y для валидации его как морщины
EYE_WRINKLE_NO_WRINKLE_TEXT = "Морщины в уголках глаз отсутсвуют"
EYE_WRINKLE_WRINKLE_TEXT = "Морщины в уголках глаз есть"


#морщины скул
CHEEKBONE_WRINKLE_CANNYPARAM_1 = 240
CHEEKBONE_WRINKLE_CANNYPARAM_2 = 250
CHEEKBONE_WRINKLE_MIN_LEN_MULTIPLIER = 0.6 #минимальная длина контура относительно высоты прямоугольника распознавания (высота прямоугольника - от верхней до нижней губы) для валидации его как морщины
CHEEKBONE_WRINKLE_MAX_LEN_MULTIPLIER = 2 #максимальная длина контура относительно высоты прямоугольника распознавания (высота прямоугольника - от верхней до нижней губы) для валидации его как морщины
CHEEKBONE_WRINKLE_MIN_X_ANGLE = -1 # минимальный угол контура между осью Х для валидации его как морщины
CHEEKBONE_WRINKLE_MAX_Y_ANGLE = 70 # максимальный угол контура между осью Y для валидации его как морщины
CHEEKBONE_WRINKLE_NO_WRINKLE_TEXT = "морщины скул отсутсвуют"
CHEEKBONE_WRINKLE_WRINKLE_TEXT = "морщины скул есть"


#морщина переносицы по центру
NOSEBRIDGECENTRAL_WRINKLE_CANNYPARAM_1 = 240
NOSEBRIDGECENTRAL_WRINKLE_CANNYPARAM_2 = 250
NOSEBRIDGECENTRAL_WRINKLE_MIN_LEN_MULTIPLIER = 0.6 #минимальная длина контура относительно высоты прямоугольника распознавания (высота прямоугольника - от верхней до нижней губы) для валидации его как морщины
NOSEBRIDGECENTRAL_WRINKLE_MAX_LEN_MULTIPLIER = 1.1 #максимальная длина контура относительно высоты прямоугольника распознавания (высота прямоугольника - от верхней до нижней губы) для валидации его как морщины
NOSEBRIDGECENTRAL_WRINKLE_MIN_X_ANGLE = 85 # минимальный угол контура между осью Х для валидации его как морщины
NOSEBRIDGECENTRAL_WRINKLE_MAX_Y_ANGLE = -1 # максимальный угол контура между осью Y для валидации его как морщины
NOSEBRIDGECENTRAL_WRINKLE_NO_WRINKLE_TEXT = "морщина переносицы по центру отсутсвует"
NOSEBRIDGECENTRAL_WRINKLE_WRINKLE_TEXT = "морщина переносицы по центру есть"

#морщины переносицы слева и справа
NOSEBRIDGE_WRINKLE_CANNYPARAM_1 = 240
NOSEBRIDGE_WRINKLE_CANNYPARAM_2 = 250
NOSEBRIDGE_WRINKLE_MIN_LEN_MULTIPLIER = 0.6 #минимальная длина контура относительно высоты прямоугольника распознавания (высота прямоугольника - от верхней до нижней губы) для валидации его как морщины
NOSEBRIDGE_WRINKLE_MAX_LEN_MULTIPLIER = 1.1 #максимальная длина контура относительно высоты прямоугольника распознавания (высота прямоугольника - от верхней до нижней губы) для валидации его как морщины
NOSEBRIDGE_WRINKLE_MIN_X_ANGLE = 85 # минимальный угол контура между осью Х для валидации его как морщины
NOSEBRIDGE_WRINKLE_MAX_Y_ANGLE = -1 # максимальный угол контура между осью Y для валидации его как морщины
NOSEBRIDGE_WRINKLE_NO_WRINKLE_TEXT = "морщины переносицы отсутсвуют"
NOSEBRIDGE_WRINKLE_WRINKLE_TEXT = "морщины переносицы есть"