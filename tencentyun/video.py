# -*- coding: utf-8 -*-

import os.path
import time
import sys
import hashlib
import requests
from tencentyun import conf
from .auth import Auth

class Video(object):

    def __init__(self, appid, secret_id, secret_key):
        self.VIDEO_FILE_NOT_EXISTS = -1
        self.VIDEO_NETWORK_ERROR = -2
        self.VIDEO_PARAMS_ERROR = -3

        self.EXPIRED_SECONDS = 2592000
        self._secret_id,self._secret_key = secret_id,secret_key
        conf.set_app_info(appid, secret_id, secret_key)


    def upload(self, filepath, userid=0,title='',desc='',magic_context=''):
        filepath = os.path.abspath(filepath);
        if os.path.exists(filepath):
            expired = int(time.time()) + self.EXPIRED_SECONDS
            url = self.generate_res_url(userid)
            auth = Auth(self._secret_id, self._secret_key)
            sign = auth.app_sign(url, expired)
            size = os.path.getsize(filepath)
            sha1 = hashlib.sha1();
            fp = open(filepath, 'rb')
            sha1.update(fp.read())

            '''data = {}
            data['Sha'] = sha1.hexdigest()
            if title:
                data['Title'] = title
                
            if desc:
                data['Desc'] = desc
                
            if magic_context:
                data['MagicContext'] = magic_context'''

            headers = {
                'Authorization':sign,
                'User-Agent':conf.get_ua(),
            }

            files = {'FileContent': open(filepath, 'rb'),'Sha':sha1.hexdigest(),'Title':title,'Desc':title,'MagicContext':magic_context}

            r = {}
            try:
                r = requests.post(url, headers=headers, files=files)
                ret = r.json()

            except Exception as e:
                if r:
                    return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}
                else:
                    return {'httpcode':0, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}
			
            if 'code' in ret:
                if 0 == ret['code']:
                    return {
                        'httpcode':r.status_code, 
                        'code':ret['code'], 
                        'message':ret['message'], 
                        'data':{
                            'url':ret['data']['url'],
                            'download_url':ret['data']['download_url'],
                            'fileid':ret['data']['fileid'],
                            'cover_url':ret['data'].has_key('cover_url') and ret['data']['cover_url'] or '',
                        }
                    }
                else:
                    return {
                        'httpcode':r.status_code, 
                        'code':ret['code'], 
                        'message':ret['message'], 
                        'data':{}
                    }
            else:
                return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(r.raw), 'data':{}}

        else:
            return {'httpcode':0, 'code':self.VIDEO_FILE_NOT_EXISTS, 'message':'file not exists', 'data':{}}

    def stat(self, fileid, userid=0):
        if not fileid:
            return {'httpcode':0, 'code':self.VIDEO_PARAMS_ERROR, 'message':'params error', 'data':{}}

        expired = int(time.time()) + self.EXPIRED_SECONDS
        url = self.generate_res_url(userid, fileid)
        auth = Auth(self._secret_id, self._secret_key)
        sign = auth.app_sign(url, expired)

        headers = {
            'Authorization':'QCloud '+sign,
            'User-Agent':conf.get_ua(),
        }

        r = {}
        try:
            r = requests.get(url, headers=headers)
            ret = r.json()
        except Exception as e:
            if r:
                return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}
            else:
                return {'httpcode':0, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}

        if 'code' in ret:
            if 0 == ret['code']:
                return {
                    'httpcode':r.status_code, 
                    'code':ret['code'], 
                    'message':ret['message'], 
                    'data':{
                        'download_url':ret['data']['file_url'],
                        'fileid':ret['data'].has_key('file_fileid') and ret['data']['file_fileid'] or '',
                        'upload_time':ret['data']['file_upload_time'],
                        'size':ret['data']['file_size'],
                        'sha':ret['data']['file_sha'],
                        'video_status':ret['data']['video_status'],
                        'video_status_msg':ret['data']['video_status_msg'],
                        'video_play_time':ret['data'].has_key('video_play_time') and ret['data']['video_play_time'] or 0,
                        'video_title':ret['data'].has_key('video_title') and ret['data']['video_title'] or '',
                        'video_desc':ret['data'].has_key('video_desc') and ret['data']['video_desc'] or '',
                        'video_cover_url':ret['data'].has_key('video_cover_url') and ret['data']['video_cover_url'] or '',
                        },
                    }
            else:
                return {
                    'httpcode':r.status_code, 
                    'code':ret['code'], 
                    'message':ret['message'], 
                    'data':{}
                }
        else:
            return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(r.raw), 'data':{}}

    def delete(self, fileid, userid=0):
        if not fileid:
            return {'httpcode':0, 'code':self.VIDEO_PARAMS_ERROR, 'message':'params error', 'data':{}}

        expired = int(time.time()) + self.EXPIRED_SECONDS
        url = self.generate_res_url(userid, fileid, 'del')
        auth = Auth(self._secret_id, self._secret_key)
        sign = auth.app_sign(url, expired)

        headers = {
            'Authorization':'QCloud '+sign,
            'User-Agent':conf.get_ua(),
        }

        r = {}
        try:
            r = requests.post(url, headers=headers)
            ret = r.json()
        except Exception as e:
            if r:
                return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}
            else:
                return {'httpcode':0, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}

        if 'code' in ret:
            if 0 == ret['code']:
                return {
                    'httpcode':r.status_code, 
                    'code':ret['code'], 
                    'message':ret['message'], 
                    'data':{},
                }
            else:
                return {
                    'httpcode':r.status_code, 
                    'code':ret['code'], 
                    'message':ret['message'], 
                    'data':{},
                }
        else:
            return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(r.raw), 'data':{}}


    def generate_res_url(self, userid=0, fileid='', oper=''):
        app_info = conf.get_app_info('video')
        if fileid:
            if oper:
                return app_info['end_point'] + str(app_info['appid']) + '/' + str(userid) + '/' + str(fileid) + '/' + oper
            else:
                return app_info['end_point'] + str(app_info['appid']) + '/' + str(userid) + '/' + str(fileid)
        else:
            return app_info['end_point'] + str(app_info['appid']) + '/' + str(userid)

