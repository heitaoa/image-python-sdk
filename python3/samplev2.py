#!/usr/bin/env python3

import time
import tencentyun

appid = "10000002"
secret_id = "AKIDL5iZVplWMenB5Zrx47X78mnCM3F5xDbC"
secret_key = "Lraz7n2vNcyW3tiP646xYdfr5KBV4YAv"

bucket = "test1"
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

