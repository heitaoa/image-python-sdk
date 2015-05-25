# -*- coding: utf-8 -*-

import tencentyun

appid = '200679'
secret_id = 'AKIDoleG4e6U0j6EVQcjWXxzSO2Vv7Hqlgp2'
secret_key = 'ROlw3XYdNXNnII18ATs6zd7m5mivnApa'

image = tencentyun.Image(appid,secret_id,secret_key)
obj = image.upload('/tmp/amazon.jpg');
print obj

if obj['code'] == 0 :
    fileid = obj['data']['fileid']
    statRet = image.stat(fileid)

    fileid = obj['data']['fileid']
    copyRet = image.copy(fileid)
    download_url = copyRet['data']['download_url']
    print copyRet

    auth = tencentyun.Auth(secret_id,secret_key)
    sign = auth.app_sign(download_url)
    print download_url + '?sign=' + sign

    print image.delete(fileid)