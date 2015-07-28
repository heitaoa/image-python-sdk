# -*- coding: utf-8 -*-

import time
import tencentyun

# V2版本 带有空间和自定义文件名的示例
# 上传图片

# 项目ID，在http://console.qcloud.com/image/bucket查看
appid = '10000002'
secret_id = 'AKIDL5iZVplWMenB5Zrx47X78mnCM3F5xDbC'
secret_key = 'Lraz7n2vNcyW3tiP646xYdfr5KBV4YAv'

# 自定义空间名称，在http://console.qcloud.com/image/bucket创建
bucket = 'test1'
# 自定义文件名
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