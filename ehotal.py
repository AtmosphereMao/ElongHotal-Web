import os
import urllib.request, urllib.parse, urllib.error
import http.cookiejar
import time
import json
import js2py
import re
import math
import random
from Crypto.Cipher import AES
import base64
from binascii import a2b_hex

regionId = '179900'
filterName = ''
GET_URL = 'http://ihotel.elong.com/region_%s/?keyword=%s&filterName=%s'
GET_HOTALS_URL = 'http://ihotel.elong.com/list/GetHotelListFromhotel?searchFeatures=%%5B%%5D&regionId=%s&keyword=%s&sort=%i&traceToken=&pageNo=%i&code=%s&groupId=' # regionId | 查询内容 | 排序0,1 | 页数 | code
GET_SCRIPTCODE_URL = 'http://ihotel.elong.com/list/scriptCode?regionId=%s&_=%i'

# 请求头
HEADER = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'Host': 'ihotel.elong.com',
    'Referer': 'http://ihotel.elong.com/region_179900/'

}
HEADER_GETINFO = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36',
}

HEADER_SCRIPTCODE = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    # 'Host': 'ihotel.elong.com',
    # 'Referer': 'http://ihotel.elong.com/region_179900/',
    'X-Requested-With': 'XMLHttpRequest',
}
# cookiejar
cookie = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

# AESCrypt
iv = ''

# 禁止302重定向处理
class NoRedirHandle(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return fp
    http_error_301 = http_error_302

class PrpCrypt(object):
    def __init__(self, key, iv):
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC
        self.iv = iv.encode('utf-8')
        self.block_size = 16
        # self.padding = lambda data: data + (self.block_size - len(data) % self.block_size) * chr(self.block_size - len(data) % self.block_size)
        # 此处为一坑,需要现将data转换为byte再来做填充，否则中文特殊字符等会报错

        # 填充函数
        self.padding = lambda data: data + (self.block_size - len(data.encode('utf-8')) % self.block_size) * chr(self.block_size - len(data.encode('utf-8')) % self.block_size)

        self.unpadding = lambda data: data[:-ord(data[-1])]

    def __unpad(self, text):
        pad = ord(text[-1])
        return text[:-pad]

    def encrypt(self, text):
        text = text.encode('utf-8')
        cryptor = AES.new(self.key, self.mode, self.iv)
        # 这里密钥key 长度必须为16（AES-128）,
        # 24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            # \0 backspace
            # text = text + ('\0' * add)
            text = text + ('\01' * add).encode('utf-8')
        elif count > length:
            add = (length - (count % length))
            # text = text + ('\0' * add)
            text = text + ('\01' * add).encode('utf-8')
        a=cryptor.encrypt(text)
        self.ciphertext = self.iv+a
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为base64
        return str(base64.b64encode(self.ciphertext), 'utf-8')

    def decrypt(self, text):
        encry_text = a2b_hex(text)  # 转换为16进制
        cryptor = AES.new(self.key, self.mode, self.iv)

        plain_text = cryptor.decrypt(encry_text)    # 解密
        # print(plain_text.decode('utf-8'))
        return self.__unpad(plain_text.decode('utf-8')) # 向上转型为UTF-8格式



def getHotels(page=1, sort=0, keyword=""):
    # 访问首页
    request = urllib.request.Request(url=GET_URL % (regionId, keyword, filterName),
                                     method='GET')
    response = opener.open(request)
    # 获取需解密的内容
    html = response.read().decode('utf-8')
    keyData = re.search('<input type="hidden" style="display: none;" id="tsd" autocomplete="off" value="(.*?)">', html, re.S).group(1)
    # print(keyData)
    # 进行解密
    crypt = AesCrypt(keyData)
    code = crypt.c(regionId)
    print("code:", code)

    # 爬取酒店列表  # regionId | 查询内容 | 排序0,1 | 页数 | code
    request = urllib.request.Request(url=GET_HOTALS_URL % (regionId, keyword, sort, page, code),
                                     method='GET')
    response = opener.open(request)
    # 获取需解密的内容
    html = response.read().decode('utf-8')
    hotels = json.loads(html)

    return hotels


class AesCrypt:
    def __init__(self, keyData):
        self.keyData = keyData

    def c(self, regionId):
        try:
            d = self.keyData
            if d is None and d == '' and not d:
                return False
            a = self.d(regionId)
            script = js2py.eval_js(self.h(a))   # js加密混淆 获取key
            return script
        except:
            return self.g()

    def h(self, script):
        if script is None and script == '' and not script:
            return script
        else:
            strinfo = re.compile('/\)\^-1/gm')  # js 信息处理
            script = strinfo.sub(')&-1', script)
            return script

    def d(self, regionId):
        # 获取iv
        for i in cookie:
            if i.name == 'iv':
                iv = i.value
        decipher = PrpCrypt(self.k(regionId), iv)
        decrypted = decipher.decrypt(self.keyData)  # AES解密
        return decrypted



    def g(self):
        return math.ceil(1e7 * random.random())

    def k(self, regionId):
        m = ""
        for v in range(0, 16-len(regionId+'a')):
            m += 'a'
        return regionId + "a" + m

def main():
    hotels = getHotels()
    if hotels['errno'] != 0:
        print("获取酒店发生错误")
    else:
        print(hotels['data'])

if __name__ == '__main__':
    main()
