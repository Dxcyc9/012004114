import re
import sqlExcute
from datetime import datetime, timedelta
import CrawlerConfigue

#获取页面信息，并进行初步筛选
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
    #每日信息
    data = {
        'date' : '',#日期
        'newAdd' :'',#每日新增
        'newAsymptomatic':''#每日无症状感染者新增
    }
    #省份新增
    areaNewAdd = {'广东':'0','福建':'0','浙江':'0','北京':'0','上海':'0','江苏':'0','河北':'0','河南':'0','湖北':'0','湖南':'0',
                  '广西':'0','云南':'0','贵州':'0','四川':'0','新疆':'0','西藏':'0','宁夏':'0','重庆':'0','天津':'0','甘肃':'0',
                  '吉林':'0','黑龙江':'0','内蒙古':'0','陕西':'0','安徽':'0','江西':'0','山东':'0','山西':'0','辽宁':'0','海南':'0',
                  '青海':'0','兵团':'0','香港':'0','澳门':'0','台湾':'0'}
    #省份每日新增无症状
    areaNewAsymptomatic = {'广东': '0', '福建': '0', '浙江': '0', '北京': '0', '上海': '0', '江苏': '0', '河北': '0', '河南': '0', '湖北': '0', '湖南': '0',
                  '广西': '0', '云南': '0', '贵州': '0', '四川': '0', '新疆': '0', '西藏': '0', '宁夏': '0', '重庆': '0', '天津': '0', '甘肃': '0',
                  '吉林': '0', '黑龙江': '0', '内蒙古': '0', '陕西': '0', '安徽': '0', '江西': '0', '山东': '0', '山西': '0', '辽宁': '0', '海南': '0',
                  '青海': '0', '兵团': '0','香港':'0','澳门':'0','台湾':'0'}
    #省份
    area = ['广东', '福建', '浙江', '北京', '上海', '江苏', '河北', '河南', '湖北', '湖南',
                  '广西', '云南', '贵州', '四川', '新疆', '西藏', '宁夏', '重庆', '天津', '甘肃',
                  '吉林', '黑龙江', '内蒙古', '陕西', '安徽', '江西', '山东', '山西', '辽宁', '海南',
                  '青海', '兵团', '香港', '澳门', '台湾']
    resp = getHtmlMainInfo(url)
    text = resp
    print(text)
    data['date'] = text[-10:]
    #获取新增
    try:
        data['newAdd'] = re.findall('本土病例(.*?)例', text)[0]
    except:
        data['newAdd'] = '0'
    #获取无症状感染
    try:
        data['newAsymptomatic'] = re.findall('本土([0-9]+)例', text)[0]
        print(data['newAsymptomatic'])
    except:
        data['newAsymptomatic'] = '0'
    #各个省份新增确诊信息
    proAdds = re.findall('本土病例[0-9]+例（(.*?)）', text, re.DOTALL)[0]
    proAddKey = re.findall('([\u4E00-\u9FA5]*)[0-9]*例', proAdds)
    proAddValue = re.findall('[\u4E00-\u9FA5]*([0-9]*)例', proAdds)
    #存入areaNewAdd字典中
    i = 0
    while i < len(proAddKey):
        areaNewAdd[proAddKey[i]]=proAddValue[i]
        i += 1
    #各个省份新增无症状感染者信息
    proAsymptomatic = re.findall('本土[0-9]+例（(.*?)）', text, re.DOTALL)[0]
    proAsymptomaticKey = re.findall('([\u4E00-\u9FA5]+?)[0-9]*?例',proAsymptomatic)
    proAsymptomaticValue = re.findall('[\u4E00-\u9FA5]+?([0-9]*?)例',proAsymptomatic)
    #存入areaNewAsymptomatic字典中
    i = 0
    while i < len(proAsymptomaticKey):
        areaNewAsymptomatic[proAsymptomaticKey[i]] = proAsymptomaticValue[i]
        i += 1
    #港澳台新增爬取，港澳台的累计确诊存入新增确诊中
        areaNewAdd['香港'] = re.findall('香港特别行政区([0-9]+)例', text)[0]
        areaNewAdd['澳门'] = re.findall('澳门特别行政区([0-9]+)例', text)[0]
        areaNewAdd['台湾'] = re.findall('台湾地区([0-9]+)例', text)[0]
    # 插入每日基本信息数据库
    sqlExcute.insertToDateInfo(data['date'],data['newAdd'],data['newAsymptomatic'])
    #插入各个省份信息
    i = 0
    while i < 35:
        sqlExcute.insertToAreaInfo(area[i],areaNewAdd[area[i]],areaNewAsymptomatic[area[i]],data['date'])
        i += 1
    return data['date']


