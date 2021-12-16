import configparser
from recognizer import const

config = configparser.ConfigParser()

config['Recognition.Face'] = {'face_round': const.FACE_ROUND, 'face_long': const.FACE_LONG}

config['Recognition.Mouth'] = {'mouth_small': const.MOUTH_SMALL, 'mouth_big': const.MOUTH_BIG,
                               'mouth_wide_lip': const.MOUTH_WIDE_LIP, 'mouth_short_lip': const.MOUTH_SHORT_LIP}

config['Recognition.Nodule'] = {'nodule_angle': const.NODULE_ANGLE}

config['Recognition.Eyes'] = {'eye_big': const.EYES_BIG, 'eye_small': const.EYES_SMALL,
                              'eye_height_big': const.EYES_HEIGHT_BIG, 'eye_height_small': const.EYES_HEIGHT_SMALL}

config['Recognition.Jaw'] = {'chin_width_big': const.CHIN_WIDTH_BIG, 'chin_width_small': const.CHIN_WIDTH_SMALL,
                             'jaw_weight_big': const.JAW_WEIGHT_BIG, 'jaw_weight_small': const.JAW_WEIGHT_SMALL}

config['Recognition.NasolabialZone'] = {'nasolabial_zone_big': const.NASOLABIAL_ZONE_BIG, 'nasolabial_zone_small': const.NASOLABIAL_ZONE_SMALL}

config['Recognition.Nose'] = {'nose_width_big': const.NOSE_WIDTH_BIG, 'nose_width_small': const.NOSE_WIDTH_SMALL,
                              'nose_height_big': const.NOSE_HEIGHT_BIG, 'nose_height_small': const.NOSE_HEIGHT_SMALL,
                              'nostrils_cut': const.NOSE_NOSTRIL_CUT, 'nostrils_flat': const.NOSE_NOSTRIL_FLAT}

config['Recognition.Eyebrow'] = {'eyebrow_height_big': const.EYEBROW_HEIGHT_BIG, 'eyebrow_height_small': const.EYEBROW_HEIGHT_SMALL}

config['Predictors'] = {'facet_shape_predictor': const.FACET_SHAPE_PREDICTOR,
                        'profile_shape_predictor': const.PROFILE_SHAPE_PREDICTOR}

config['Main'] = {'predictor_threads': const.PREDICTOR_THREADS}

config['Wrinkle.NoseWrinkle'] = {'cannyparam1': const.NOSE_WRINKLE_CANNYPARAM_1, 'cannyparam2': const.NOSE_WRINKLE_CANNYPARAM_2,
                                 'minlenmultiplier': const.NOSE_WRINKLE_MIN_LEN_MULTIPLIER, 'maxlenmultiplier': const.NOSE_WRINKLE_MAX_LEN_MULTIPLIER,
                                 'minXangle': const.NOSE_WRINKLE_MIN_X_ANGLE, 'maxYangle': const.NOSE_WRINKLE_MAX_Y_ANGLE,
                                 'face_delta': const.NOSE_WRINKLE_LENGTH_DIFF, '': const.NOSE_WRINKLE_FACE_DELTA,
                                 'koef_min': const.NOSE_WRINKLE_KOEF_MIN, 'koef_max': const.NOSE_WRINKLE_KOEF_MAX}

config['Wrinkle.MouthWrinkle'] = {'cannyparam1': const.MOUTH_WRINKLE_CANNYPARAM_1, 'cannyparam2': const.MOUTH_WRINKLE_CANNYPARAM_2,
                                 'minlenmultiplier': const.MOUTH_WRINKLE_MIN_LEN_MULTIPLIER, 'maxlenmultiplier': const.MOUTH_WRINKLE_MAX_LEN_MULTIPLIER,
                                 'minXangle': const.MOUTH_WRINKLE_MIN_X_ANGLE, 'maxYangle': const.MOUTH_WRINKLE_MAX_Y_ANGLE,
                                 'face_delta': const.MOUTH_WRINKLE_LENGTH_DIFF, '': const.MOUTH_WRINKLE_FACE_DELTA,
                                 'koef_min': const.MOUTH_WRINKLE_KOEF_MIN, 'koef_max': const.MOUTH_WRINKLE_KOEF_MAX}

config['Wrinkle.EyeWrinkle'] = {'cannyparam1': const.EYE_WRINKLE_CANNYPARAM_1, 'cannyparam2': const.EYE_WRINKLE_CANNYPARAM_2,
                                 'minlenmultiplier': const.EYE_WRINKLE_MIN_LEN_MULTIPLIER, 'maxlenmultiplier': const.EYE_WRINKLE_MAX_LEN_MULTIPLIER,
                                 'minXangle': const.EYE_WRINKLE_MIN_X_ANGLE, 'maxYangle': const.EYE_WRINKLE_MAX_Y_ANGLE}

config['Wrinkle.CheekboneWrinkle'] = {'cannyparam1': const.CHEEKBONE_WRINKLE_CANNYPARAM_1, 'cannyparam2': const.CHEEKBONE_WRINKLE_CANNYPARAM_2,
                                 'minlenmultiplier': const.CHEEKBONE_WRINKLE_MIN_LEN_MULTIPLIER, 'maxlenmultiplier': const.CHEEKBONE_WRINKLE_MAX_LEN_MULTIPLIER,
                                 'minXangle': const.CHEEKBONE_WRINKLE_MIN_X_ANGLE, 'maxYangle': const.CHEEKBONE_WRINKLE_MAX_Y_ANGLE}

config['Wrinkle.NosebridgecentralWrinkle'] = {'cannyparam1': const.NOSEBRIDGECENTRAL_WRINKLE_CANNYPARAM_1, 'cannyparam2': const.NOSEBRIDGECENTRAL_WRINKLE_CANNYPARAM_2,
                                 'minlenmultiplier': const.NOSEBRIDGECENTRAL_WRINKLE_MIN_LEN_MULTIPLIER, 'maxlenmultiplier': const.NOSEBRIDGECENTRAL_WRINKLE_MAX_LEN_MULTIPLIER,
                                 'minXangle': const.NOSEBRIDGECENTRAL_WRINKLE_MIN_X_ANGLE, 'maxYangle': const.NOSEBRIDGECENTRAL_WRINKLE_MAX_Y_ANGLE}


config['Wrinkle.NosebridgeWrinkle'] = {'cannyparam1': const.NOSEBRIDGE_WRINKLE_CANNYPARAM_1, 'cannyparam2': const.NOSEBRIDGE_WRINKLE_CANNYPARAM_2,
                                 'minlenmultiplier': const.NOSEBRIDGE_WRINKLE_MIN_LEN_MULTIPLIER, 'maxlenmultiplier': const.NOSEBRIDGE_WRINKLE_MAX_LEN_MULTIPLIER,
                                 'minXangle': const.NOSEBRIDGE_WRINKLE_MIN_X_ANGLE, 'maxYangle': const.NOSEBRIDGE_WRINKLE_MAX_Y_ANGLE}

with open('recognition.ini', 'w') as configfile:
    config.write(configfile)