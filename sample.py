# -*- coding: utf-8 -*-

import time
import tencentyun

appid = '200679'
secret_id = 'AKIDoleG4e6U0j6EVQcjWXxzSO2Vv7Hqlgp2'
secret_key = 'ROlw3XYdNXNnII18ATs6zd7m5mivnApa'

# 图片上传
image = tencentyun.Image(appid,secret_id,secret_key)
obj = image.upload('./test.jpg');
print obj

if obj['code'] == 0 :
    fileid = obj['data']['fileid']
    statRet = image.stat(fileid)

    fileid = obj['data']['fileid']
    copyRet = image.copy(fileid)
    download_url = copyRet['data']['download_url']
    print copyRet

    # 生成私密下载url
    auth = tencentyun.Auth(secret_id,secret_key)
    sign = auth.app_sign(download_url)
    print download_url + '?sign=' + sign

    # 生成上传签名
    expired = int(time.time()) + 999
    sign = auth.app_sign('http://web.image.myqcloud.com/photos/v1/200679/0/', expired)
    print sign

    print image.delete(fileid)

# 视频上传
video = tencentyun.Video(appid,secret_id,secret_key)
obj = video.upload('./test.mp4',0,'title_test','desc_test','magic_test');
print obj

if obj['code'] == 0 :
    fileid = obj['data']['fileid']
    # 查询视频状态
    statRet = video.stat(fileid)
    print statRet
    
    # 生成上传签名
    auth = tencentyun.Auth(secret_id,secret_key)
    expired = int(time.time()) + 999
    sign = auth.app_sign('http://web.video.myqcloud.com/videos/v1/200679/0/', expired)
    print sign

    # 删除视频
    #print video.delete(fileid)
