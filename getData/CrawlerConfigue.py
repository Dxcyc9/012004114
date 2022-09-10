import asyncio

import pyppeteer as pyp
import requests
from pyppeteer import launcher

# 在导入 launch 之前 把 --enable-automation 禁用 防止监测webdriver
launcher.DEFAULT_ARGS.remove("--enable-automation")

# import nest_asyncio
# nest_asyncio.apply()

def sessionGetHtml(session, url):  # 发送带session的网页请求
    fakeHeaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77'
    }  # 伪装浏览器用的请求头
    try:
        result = session.get(url, headers=fakeHeaders)
        result.encoding = result.apparent_encoding
        return result.text
    except Exception as e:
        print(e)
        return ""


async def makeSession(page):
    # 返回一个session,将其内部cookies修改成pypeteer浏览器页面对象中的cookies
    cookies = await page.cookies()  # cookies是一个列表，每个元素都是一个字典
    cookies1 = {}
    for cookie in cookies:  # requests中的cookies只要 "name"属性
        cookies1[cookie['name']] = cookie['value']
    session = requests.Session()
    session.cookies.update(cookies1)
    return session


async def antiAntiCrawler(page):
    # 为page添加反反爬虫手段
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0')
    await page.evaluateOnNewDocument(
        '() =>{ Object.defineProperties(navigator,'
        '{ webdriver:{ get: () => false } }) }')


# 爬取网页主题信息
async def getOjSourceCode(url):
    width, height = 1, 1  # 网页宽高
    browser = await pyp.launch(headless=False,
                               userdataDir="c:/tmp",
                               args=[f'--window-size={width},{height}'])
    page = await browser.newPage()
    await antiAntiCrawler(page)  # 反爬虫函数
    await page.setViewport({'width': width, 'height': height})
    await page.goto(url)
    await page.waitForXPath('/html/body/div[3]/div[2]')
    session = await makeSession(page)  # 调用函数获取session
    html = sessionGetHtml(session, url)
    await browser.close()

    return html


def get(url):
    #print(asyncio.get_event_loop().run_until_complete(getOjSourceCode(url)))
    return asyncio.get_event_loop().run_until_complete(getOjSourceCode(url))

#get('http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_2.shtml')