#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import tencentyun

# V2版本 带有空间和自定义文件名的示例
# 上传图片

# 项目ID，在http://console.qcloud.com/image/bucket查看
appid = '111'
secret_id = 'secret_id'
secret_key = 'secret_key'

# 自定义空间名称，在http://console.qcloud.com/image/bucket创建
bucket = 'bucket'

imageprocess = tencentyun.ImageProcess(appid,secret_id,secret_key,bucket)

#智能鉴黄，单个图片Url
pornUrl = 'http://b.hiphotos.baidu.com/image/pic/item/8ad4b31c8701a18b1efd50a89a2f07082938fec7.jpg'
pornRet = imageprocess.porn_detect(pornUrl)
print 'pornRet:', pornRet

#智能鉴黄，单个或多个图片Url
pornUrl = [
        'http://b.hiphotos.baidu.com/image/pic/item/8ad4b31c8701a18b1efd50a89a2f07082938fec7.jpg',
        'http://c.hiphotos.baidu.com/image/h%3D200/sign=7b991b465eee3d6d3dc680cb73176d41/96dda144ad3459829813ed730bf431adcaef84b1.jpg',
    ]
pornRet = imageprocess.porn_detect_url(pornUrl)
print 'pornRet:', pornRet

#智能鉴黄，单个或多个图片File
pornFile = [
        'D:/porn/test1.jpg',
        'D:/porn/test2.jpg',
        '../../../../../porn/test3.png',
    ]
pornRet = imageprocess.porn_detect_file(pornFile)
print 'pornRet:', pornRet
# 注意：如果您要鉴黄的图片文件或路径中包含中文，请修改requests包的packages/urlib3中的fields.py文件
#       将format_header_param方法中的倒数第二行
#           value = '%s*=%s' % (name, value)
#       修改为
#           value = '%s="%s"' % (name, value)

# 自定义文件名
fileid = 'sample'+str(int(time.time()))

image_path = '/tmp/amazon.jpg'

# 图片上传
image = tencentyun.ImageV2(appid,secret_id,secret_key)

# upload by filename
obj = image.upload(image_path, bucket, fileid);
# or in-memory data
#binary_image = open(image_path).read()
#obj = image.upload_binary(binary_image, bucket, fileid)
print 'upload:', obj

if obj['code'] == 0 :
    fileid = obj['data']['fileid']
    statRet = image.stat(bucket, fileid)
    print 'stat:', statRet

    # 生成私密下载url
    auth = tencentyun.Auth(secret_id,secret_key)
    expired = int(time.time()) + 999
    sign = auth.get_app_sign_v2(bucket, fileid, expired)
    download_url = statRet['data']['download_url']
    print 'download_url:', download_url + '?sign=' + sign

    # 生成上传签名
    fileid = 'sample'+str(int(time.time()))
    expired = int(time.time()) + 999
    sign = auth.get_app_sign_v2(bucket, fileid, expired)
    print fileid, sign

    fileid = obj['data']['fileid']
    copyRet = image.copy(bucket, fileid)
    print 'copy:', copyRet

    #print image.delete(bucket, fileid)


# 上传指定进行优图识别  fuzzy（模糊识别），food(美食识别）
# 如果要支持模糊识别，url?analyze=fuzzy
# 如果要同时支持模糊识别和美食识别，url?analyze=fuzzy.food
# 返回数据中
# "is_fuzzy" 1 模糊 0 清晰
# "is_food" 1 美食 0 不是
userid = 0
magic_context = ''
gets = {'analyze':'fuzzy.food'}
fileid = 'sample'+str(int(time.time()))+'new'
obj = image.upload(image_path, bucket, fileid, userid, magic_context, {'get':gets});
print obj
