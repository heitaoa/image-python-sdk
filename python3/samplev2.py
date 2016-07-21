#!/usr/bin/env python3

import time
import tencentyun

appid = "111"
secret_id = "secret_id"
secret_key = "secret_key"

bucket = "bucket"

#porn detect
imageprocess = tencentyun.ImageProcess(appid,secret_id,secret_key,bucket)

pornUrl = 'http://b.hiphotos.baidu.com/image/pic/item/8ad4b31c8701a18b1efd50a89a2f07082938fec7.jpg'
pornRet = imageprocess.porn_detect(pornUrl)
print('pornRet:', pornRet)

pornUrl = [
        'http://b.hiphotos.baidu.com/image/pic/item/8ad4b31c8701a18b1efd50a89a2f07082938fec7.jpg',
        'http://c.hiphotos.baidu.com/image/h%3D200/sign=7b991b465eee3d6d3dc680cb73176d41/96dda144ad3459829813ed730bf431adcaef84b1.jpg',
    ]
pornRet = imageprocess.porn_detect_url(pornUrl)
print ('pornRet:', pornRet)

pornFile = [
        'D:/porn/test1.jpg',
        'D:/porn/test2.jpg',
        '../../../../../porn/test3.png',
    ]
pornRet = imageprocess.porn_detect_file(pornFile)
print ('pornRet:', pornRet)
# 注意：如果您要鉴黄的图片文件或路径中包含中文，请修改requests包的packages/urlib3中的fields.py文件
#       将format_header_param方法中的倒数第二行
#           value = '%s*=%s' % (name, value)
#       修改为
#           value = '%s="%s"' % (name, value)

fileid = "sample" + str(int(time.time()))

sample_image_path = "test_image.jpg"


image = tencentyun.ImageV2(appid,secret_id, secret_key)



# upload an image from local file
obj = image.upload(sample_image_path, bucket, fileid);
# or from in-memory binary data
# both upload and upload_binary is ok in Python 3
#image_data = open(sample_image_path, "rb").read()
#obj = image.upload(image_data, bucket, fileid)
#obj = image.upload_binary(image_data, bucket, fileid)
print("Update return info: ")
print(obj)


if obj["code"] == 0:
    fileid = obj["data"]["fileid"]
    statRet = image.stat(bucket, fileid)
    print("Status enquiry returns info: ")
    print(statRet)

    fileid = obj["data"]["fileid"]
    copyRet = image.copy(bucket, fileid)
    download_url = copyRet["data"]["download_url"]
    print("Copy returns info: ")
    print(copyRet)

    # generate private download URL
    auth = tencentyun.Auth(secret_id,secret_key)
    expired = 0
    sign = auth.get_app_sign_v2(bucket, fileid, expired)
    print("Private download URL: ")
    print(download_url + "?sign=" + sign)

    # generate upload signature
    copy_fileid = 'sample' + str(int(time.time()))
    expired = int(time.time()) + 999
    sign = auth.get_app_sign_v2(bucket, copy_fileid, expired)
    print("Upload signature: ")
    print(copy_fileid)
    print(sign)


    print("Delete returns info: ")
    print(image.delete(bucket, fileid))


# Youtu recognition after upload this image, 
# fuzzy recognition and food recognition are supported
# to enable fuzzy recognition: url?analyze=fuzzy
# to enable both: url?analyze=fuzzy.food
# in return value: is_fuzzy == 1 if this image is fuzzy, 0 otherwise
#                  is_food == 1 if this is an image of food, 0 otherwise
print("Youtu recognition after uploading: ")
userid = 0
magic_context = ""
gets = {"analyze": "fuzzy.food"}
obj = image.upload(sample_image_path, bucket, fileid, userid, magic_context, {"get": gets});
print(obj)

if obj["code"] == 0:
    image.delete(bucket, fileid)

