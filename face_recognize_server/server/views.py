# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
import recognizer.recognize
import base64
import numpy as np
import zlib

@require_http_methods(["POST"])
@csrf_exempt
def Recognizing(request):

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
        json_data = json.loads(request.body)
        
        facet_image = base64.b64decode(json_data['facet']['data'])
        #facet_hash = json_data['facet']['hash']

        #if check_summ(facet_hash, facet_image) != True:
        #    result = {'result': 'error',
        #              'description': 'bad facet image check sum'}
        #    return JsonResponse(result)

        profile_image = base64.b64decode(json_data['profile']['data'])
        #profile_hash = json_data['profile']['hash']

        #if check_summ(profile_hash, profile_image) != True:
        #    result = {'result': 'error',
        #              'description': 'bad profile image check sum'}
        #    return JsonResponse(result)

        result = recognizer.recognize.recognize_precessor.recognize(facet_image, profile_image)
    except Exception:
        e = sys.exc_info()[1]
        result = {'result': 'error',
                    'description': 'bad request',
                    'errorText': e.args[0]}

    return JsonResponse(result)