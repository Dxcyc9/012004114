import time

import crawlerEpidemic
import sqlExcute

#获取主页链接列表
i = 2
while i < 6:
    homePageUrl = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_{}.shtml'.format(i)
    print(homePageUrl)
    urList = crawlerEpidemic.getUrls(homePageUrl)
    print(urList)
    for url in urList:
        crawlerEpidemic.getDayData(url)
        time.sleep(5)
    i+=1

# urList = crawlerEpidemic.getUrls('http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml')
# print(urList)
# for url in urList:
#     crawlerEpidemic.getDayData(url)
#     time.sleep(3)
