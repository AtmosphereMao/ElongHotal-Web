import os
import urllib.request, urllib.parse, urllib.error
import http.cookiejar

regionId = '179900'
keyword = ''
filterName = ''
GET_URL = 'http://ihotel.elong.com/region_%s/?keyword=%s&filterName=%s' % (regionId, keyword, filterName)
GET_HOTALS_URL = 'http://ihotel.elong.com/list/GetHotelListFromhotel?searchFeatures=%5B%5D&regionId=179900&keyword=%E6%8B%89%E6%96%AF%E4%B8%BD&sort=1&traceToken=&pageNo=1&code=6900321&groupId='

# 请求头
HEADER = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Host': 'ehall.szpt.edu.cn',

}
HEADER_GETINFO = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36',
}
# cookiejar
cookie = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

def getHotals():
    request = urllib.request.Request(url=GET_URL,
                                     method='GET')
    response = opener.open(request)
    html = response.read().decode('utf-8')
    print(html)
    return True

def main():
    if getHotals():
        pass
    else:
        print("登录失败")


if __name__ == '__main__':
    main()
