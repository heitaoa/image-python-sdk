# tencentyun-image-python
python sdk for [腾讯云万象图片服务](http://app.qcloud.com/image.html)

## 安装

### 使用pip
pip install tencentyun

### 下载源码
从github下载源码装入到您的程序中，并加载tencentyun包

## 修改配置
修改tencentyun/conf.py内的appid等信息为您的配置

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
```