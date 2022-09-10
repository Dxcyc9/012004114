import re
import sqlExcute
from datetime import datetime, timedelta
import CrawlerConfigue
#首页url
homePageUrl = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"

headers = {
    "User-Agent":'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MI NOTE LTE Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/8.8.7',
    #'Connection': 'close'
}
def getHtmlMainInfo(url):
    t = ''
    temp = CrawlerConfigue.get(url)
    # 获取日期信息
    pattern = '20[0-9]+-[0-9]+-[0-9]+'
    infoTmp = re.findall(pattern, temp)
    s = infoTmp[2]
    cur_time = (datetime.strptime(s, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')

    # 获取主体
    pattern = '>.*?<'
    tempInfo = re.findall(pattern, temp)
    for i in tempInfo:
        str_t = i[1:-1]
        t += str_t
    t += cur_time
    return t[t.index('页'):]

#爬取主页链接
def getUrls(url):
    #爬取主页信息
    resp = CrawlerConfigue.get(url)
  #  print(resp)
    #获取主页到每一天的链接
    urlList = re.findall('\/xcs\/yqtb.*\.shtml',resp)
    len(urlList)
    print(len(urlList))
    i = 0
    while i < len(urlList):
        urlList[i] = 'http://www.nhc.gov.cn' + urlList[i]
        i += 1
    return urlList

#爬取各个日期页面信息
def getDayData(url):
    data = {
        'date' : '',
        'newAdd' :'',
        'newAsymptomatic':'',
        'area':[{
            'province':'',
            'newAdd':'',
            'newAsymptomatic':''
        }]
    }
    areaNewAdd = {'广东':'0','福建':'0','浙江':'0','北京':'0','上海':'0','江苏':'0','河北':'0','河南':'0','湖北':'0','湖南':'0',
                  '广西':'0','云南':'0','贵州':'0','四川':'0','新疆':'0','西藏':'0','宁夏':'0','重庆':'0','天津':'0','甘肃':'0',
                  '吉林':'0','黑龙江':'0','内蒙古':'0','陕西':'0','安徽':'0','江西':'0','山东':'0','山西':'0','辽宁':'0','海南':'0',
                  '青海':'0','兵团':'0','香港':'0','澳门':'0','台湾':'0'}
    areaNewAsymptomatic = {'广东': '0', '福建': '0', '浙江': '0', '北京': '0', '上海': '0', '江苏': '0', '河北': '0', '河南': '0', '湖北': '0', '湖南': '0',
                  '广西': '0', '云南': '0', '贵州': '0', '四川': '0', '新疆': '0', '西藏': '0', '宁夏': '0', '重庆': '0', '天津': '0', '甘肃': '0',
                  '吉林': '0', '黑龙江': '0', '内蒙古': '0', '陕西': '0', '安徽': '0', '江西': '0', '山东': '0', '山西': '0', '辽宁': '0', '海南': '0',
                  '青海': '0', '兵团': '0','香港':'0','澳门':'0','台湾':'0'}
    area = ['广东', '福建', '浙江', '北京', '上海', '江苏', '河北', '河南', '湖北', '湖南',
                  '广西', '云南', '贵州', '四川', '新疆', '西藏', '宁夏', '重庆', '天津', '甘肃',
                  '吉林', '黑龙江', '内蒙古', '陕西', '安徽', '江西', '山东', '山西', '辽宁', '海南',
                  '青海', '兵团', '香港', '澳门', '台湾']
    resp = getHtmlMainInfo(url)
    text = resp
    print(text)
    data['date'] = text[-10:]
    try:
        data['newAdd'] = re.findall('本土病例(.*?)例', text)[0]
    except:
        data['newAdd'] = '0'
    try:
        data['newAsymptomatic'] = re.findall('本土(.*?)例', text)[2]
    except:
        data['newAsymptomatic'] = '0'

    proAdds = re.findall('本土病例[0-9]+例（(.*?)）', text, re.DOTALL)[0]
    proAddKey = re.findall('([\u4E00-\u9FA5]*)[0-9]*例', proAdds)
    proAddValue = re.findall('[\u4E00-\u9FA5]*([0-9]*)例', proAdds)

    i = 0
    while i < len(proAddKey):
        areaNewAdd[proAddKey[i]]=proAddValue[i]
        i += 1

    proAsymptomatic = re.findall('本土[0-9]+例（(.*?)）', text, re.DOTALL)[0]
    proAsymptomaticKey = re.findall('([\u4E00-\u9FA5]+?)[0-9]*?例',proAsymptomatic)
    proAsymptomaticValue = re.findall('[\u4E00-\u9FA5]+?([0-9]*?)例',proAsymptomatic)
    i = 0
    while i < len(proAsymptomaticKey):
        areaNewAsymptomatic[proAsymptomaticKey[i]] = proAsymptomaticValue[i]
        i += 1


    #港澳台新增爬取
        areaNewAdd['香港'] = re.findall('香港特别行政区([0-9]+)例', text)[0]
        areaNewAdd['澳门'] = re.findall('澳门特别行政区([0-9]+)例', text)[0]
        areaNewAdd['台湾'] = re.findall('台湾地区([0-9]+)例', text)[0]


    sqlExcute.insertToDateInfo(data['date'],data['newAdd'],data['newAsymptomatic'])

    i = 0
    while i < 35:
        sqlExcute.insertToAreaInfo(area[i],areaNewAdd[area[i]],areaNewAsymptomatic[area[i]],data['date'])
        i += 1





