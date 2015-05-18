# -*- coding: utf-8 -*-

import tencentyun

image = tencentyun.Image('200679','AKIDoleG4e6U0j6EVQcjWXxzSO2Vv7Hqlgp2','ROlw3XYdNXNnII18ATs6zd7m5mivnApa')
obj = image.upload('/tmp/amazon.jpg');
print obj

fileid = obj['data']['fileid']
print image.stat(fileid)

print image.delete(fileid)