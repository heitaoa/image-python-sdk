#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import tencentyun

appid = "200899"
secret_id = "AKIDXZE8z7kUBlltXgfjb8NgrgChrpTiiVNo"
secret_key = "8W0dbC201JgEl8XPYTBFu0ulUxiNnuYv"

sample_image_path = "test_image.jpg"
sample_video_path = "test_video.mp4"


image = tencentyun.Image(appid,secret_id,secret_key)

# upload an image from local file
#obj = image.upload(sample_image_path);
# or from in-memory binary data
# both upload and upload_binary is ok in Python 3
image_data = open(sample_image_path, "rb").read()
#obj = image.upload(image_data)
obj = image.upload_binary(image_data)
print("Update return info: ")
print(obj)

if obj["code"] == 0:
    fileid = obj["data"]["fileid"]
    statRet = image.stat(fileid)
    print("Status enquiry returns info: ")
    print(statRet)

    fileid = obj["data"]["fileid"]
    copyRet = image.copy(fileid)
    download_url = copyRet["data"]["download_url"]
    print("Copy returns info: ")
    print(copyRet)

    # generate private download url
    auth = tencentyun.Auth(secret_id,secret_key)
    sign = auth.app_sign(download_url)
    print("Private download URL: ")
    print(download_url + "?sign=" + sign)

    # generate upload signature
    expired = int(time.time()) + 999
    sign = auth.app_sign("http://web.image.myqcloud.com/photos/v1/200679/0/", expired)
    print("Upload signature: ")
    print(sign)

    print("Delete returns info: ")
    print(image.delete(fileid))



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
# u can use both local filename or image binary data
obj = image.upload(sample_image_path, userid,magic_context, {"get": gets});
print(obj)

if obj["code"] == 0:
    image.delete(obj["data"]["fileid"])
