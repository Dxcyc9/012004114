import time

import crawlerEpidemic
import sqlExcute
import writeToExcel

#将日期以str形式存入dateList以便后续操作
dateList = []
#爬取第一页的所有链接并访问
urList = crawlerEpidemic.getUrls('http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml')
for url in urList:
    #日期存入dateList
    dateList.append(crawlerEpidemic.getDayData(url))
    time.sleep(3)
#获取2-20页主页链接列表
i = 2
while i < 20:
    homePageUrl = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_{}.shtml'.format(i)
    urList = crawlerEpidemic.getUrls(homePageUrl)
    for url in urList:
        dateList.append(crawlerEpidemic.getDayData(url))
        print(dateList)
        time.sleep(3)
    i+=1

#将爬到的数据写入excel
writeToExcel.writeToExcel(dateList)