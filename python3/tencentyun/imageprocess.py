# -*- coding: utf-8 -*-

import os.path
import time
import urllib
import json
import requests
from tencentyun import conf
from .auth import Auth

class ImageProcess(object):

    def __init__(self, appid, secret_id, secret_key, bucket):
        self._secret_id,self._secret_key = secret_id,secret_key
        conf.set_app_info(appid, secret_id, secret_key, bucket)

    def porn_detect(self, porn_detect_url):
        auth = Auth(self._secret_id, self._secret_key)
        sign = auth.get_porn_detect_sign(porn_detect_url)
        app_info = conf.get_app_info()

        if False == sign:
            return {
                'code':9,
                'message':'Secret id or key is empty.',
                'data':{},
            }

        url = app_info['end_point_porndetect']
        payload = {
            'bucket':app_info['bucket'],
            'appid':int(app_info['appid']),
            'url':(porn_detect_url),
        }
        header = {
            'Authorization':sign,
            'Content-Type':'application/json',
        }
        r = {}
        r = requests.post(url, data=json.dumps(payload), headers=header)
        ret = r.json()

        return ret