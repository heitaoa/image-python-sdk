# tencentyun-image-python
Python 2/3 SDK for [腾讯云万象图片服务](http://app.qcloud.com/image.html)

## 安装

### 使用pip
Python 2:

pip install tencentyun

Python 3:

pip3 install tencentyun

### 下载源码
从github下载源码装入到您的程序中，并加载tencentyun包

## 修改配置
修改tencentyun/conf.py内的appid等信息为您的配置

## V2版本空间和自定义文件名的上传，查询和删除示例
```python
# -*- coding: utf-8 -*-

import time
import tencentyun

appid = '10000002'
secret_id = 'AKIDL5iZVplWMenB5Zrx47X78mnCM3F5xDbC'
secret_key = 'Lraz7n2vNcyW3tiP646xYdfr5KBV4YAv'

bucket = 'test1'
fileid = 'sample'+str(int(time.time()))

# 图片上传
image = tencentyun.ImageV2(appid,secret_id,secret_key)
obj = image.upload('/tmp/amazon.jpg', bucket, fileid);
print obj

if obj['code'] == 0 :
    fileid = obj['data']['fileid']
    statRet = image.stat(bucket, fileid)

    fileid = obj['data']['fileid']
    copyRet = image.copy(bucket, fileid)
    download_url = copyRet['data']['download_url']
    print copyRet

    # 生成私密下载url
    auth = tencentyun.Auth(secret_id,secret_key)
    sign = auth.app_sign_v2(download_url)
    print download_url + '?sign=' + sign

    # 生成上传签名
    expired = int(time.time()) + 999
    sign = auth.app_sign_v2('http://test1-10000002.image.myqcloud.com/test1-10000002/0/sample1436341553/', expired)
    print sign

    print image.delete(bucket, fileid)

# 上传指定进行优图识别  fuzzy（模糊识别），food(美食识别）
# 如果要支持模糊识别，url?analyze=fuzzy
# 如果要同时支持模糊识别和美食识别，url?analyze=fuzzy.food
# 返回数据中
# "is_fuzzy" 1 模糊 0 清晰
# "is_food" 1 美食 0 不是
userid = 0
magic_context = ''
gets = {'analyze':'fuzzy.food'}
obj = image.upload('/tmp/amazon.jpg', bucket, fileid, userid, magic_context, {'get':gets});
print obj
```

## 万象优图上传识别示例
```python
# 上传指定进行优图识别  fuzzy（模糊识别），food(美食识别）
# 如果要支持模糊识别，url?analyze=fuzzy
# 如果要同时支持模糊识别和美食识别，url?analyze=fuzzy.food
# 返回数据中
# "is_fuzzy" 1 模糊 0 清晰
# "is_food" 1 美食 0 不是
userid = 0
magic_context = ''
gets = {'analyze':'fuzzy.food'}
obj = image.upload('/tmp/20150624100808134034653.jpg',userid,magic_context,{'get':gets});
print obj
```

## 图片上传、查询、删除程序示例
```python
# -*- coding: utf-8 -*-

import time
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
obj = video.upload('test.mp4','0','test_title','test_desc','test_magic_context')
#obj = video.upload_slice('test.mp4','0','test_title','test_desc','test_magic_context')		#分片上传，适用于较大文件
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
    print video.delete(fileid)

	
```
