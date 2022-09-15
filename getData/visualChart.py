#利用Map模块绘制地图
#Map模块的使用方法和Geo类似，数据展现在地图上，首先导入相关库：
from pyecharts.faker import Collector, Faker
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
from pyecharts.charts import Map
from getData import sqlExcute
import re
from getData import writeToExcel
#处理香、台湾、澳门的数据
def handleData(date):
    #当天的数据
    data = sqlExcute.seleceProvinceDataByDate(date)
    i = 0
    dateYes = ''
    #获取前一天日期
    while i < len(writeToExcel.dateList):
        if date == writeToExcel.dateList[i]:
            dateYes = writeToExcel.dateList[i+1]
            break
        i += 1
    #昨天的数据
    dataYes = sqlExcute.seleceProvinceDataByDate(dateYes)
    listTo = []
    listYes = []
    #格式转化
    for d in data:
        tmp = re.findall('\'([0-9]+)\'', str(d))[0]
        num = int(tmp)
        listTo.append(num)
    for d in dataYes:
        tmp = re.findall('\'([0-9]+)\'', str(d))[0]
        num = int(tmp)
        listYes.append(num)
    #港澳台数据处理
    listTo[-1] = listTo[-1] - listYes[-1]
    listTo[-2] = listTo[-2] - listYes[-2]
    listTo[-3] = listTo[-3] - listYes[-3]
    return listTo

date = input("请输入日期：")
c = (
    Map()
    .add("新增确诊", [list(z) for z in zip([ '广东', '福建', '浙江', '北京', '上海', '江苏', '河北', '河南', '湖北', '湖南',
                '广西', '云南', '贵州', '四川', '新疆', '西藏', '宁夏', '重庆', '天津', '甘肃',
                '吉林', '黑龙江', '内蒙古', '陕西', '安徽', '江西', '山东', '山西', '辽宁', '海南',
                '青海', '兵团', '香港', '澳门', '台湾'], handleData(date))], "china")
    .set_global_opts(title_opts=opts.TitleOpts(title=date+"疫情图"),
    visualmap_opts=opts.VisualMapOpts(max_=200))

    .add("新增无症状", [list(z) for z in zip(['广东', '福建', '浙江', '北京', '上海', '江苏', '河北', '河南', '湖北', '湖南',
                                        '广西', '云南', '贵州', '四川', '新疆', '西藏', '宁夏', '重庆', '天津', '甘肃',
                                        '吉林', '黑龙江', '内蒙古', '陕西', '安徽', '江西', '山东', '山西', '辽宁', '海南',
                                        '青海', '兵团', '香港', '澳门', '台湾'], sqlExcute.seleceProvinceDataByDateAsy(date))], "china")
    .set_global_opts(title_opts=opts.TitleOpts(title=date+"疫情图"),
                     visualmap_opts=opts.VisualMapOpts(max_=200))

)

#存到指定目录
savepath =  "F:\\pythoncode\\charts\\"
c.render(savepath + date + ".html")
c.render_notebook()

