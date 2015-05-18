# tencentyun-image-php
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
import tencentyun

image = tencentyun.Image('200679','AKIDoleG4e6U0j6EVQcjWXxzSO2Vv7Hqlgp2','ROlw3XYdNXNnII18ATs6zd7m5mivnApa')
obj = image.upload('/tmp/amazon.jpg');
print obj

fileid = obj['data']['fileid']
print image.stat(fileid)

print image.delete(fileid)
```