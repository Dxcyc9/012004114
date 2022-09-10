import xlwt
import re
from openpyxl import load_workbook
from openpyxl.styles import Alignment
import sqlExcute

def writeToExcel():
    # 创建新的workbook（其实就是创建新的excel）
    workbook = xlwt.Workbook(encoding='ascii')

    dateList = sqlExcute.selectFromDateInfo()
    i = 4
    for date in dateList:
        worksheet = workbook.add_sheet(date)# 创建新的sheet表

        # 合并 第0行到第2行 的 第0列到第3列
        worksheet.write_merge(0, 2, 0, 4, date + "疫情通报表")
        worksheet.write_merge(0, 0, 5, 7, '当日新增本地确诊')
        worksheet.write_merge(2, 2, 5, 7, '当日新增本地无症状感染者')

        # 往表格写入内容
        worksheet.write(3, 0, "省份")
        worksheet.write(3, 1, "本土新增")
        worksheet.write(3, 2, "本土新增无症状感染者")

        newAdd = sqlExcute.selectNewAdd(date)
        worksheet.write(0,8,newAdd)

        newAsymptomatic = sqlExcute.selectNewAsymptomatic(date)
        worksheet.write(2,8,newAsymptomatic)

        #写入省份信息
        i = 4
        provinceList = sqlExcute.selectProvince()
        for province in provinceList:
            worksheet.write(i, 0, province)#省份写入
            provinceNewAdd = sqlExcute.selectProvinceNewAdd(date,re.findall('\'(.*)\',',str(province))[0])
            provinceNewAsymptomatic = sqlExcute.selectProvinceAsymptomatic(date,re.findall('\'(.*)\',',str(province))[0])
            print(re.findall('\'(.*)\',',str(province))[0])
            worksheet.write(i,1,provinceNewAdd)
            worksheet.write(i,2,provinceNewAsymptomatic)
            i += 1










    # # 设置样式
    # style = xlwt.XFStyle()
    # al = xlwt.Alignment()
    # # VERT_TOP = 0x00       上端对齐
    # # VERT_CENTER = 0x01    居中对齐（垂直方向上）
    # # VERT_BOTTOM = 0x02    低端对齐
    # # HORZ_LEFT = 0x01      左端对齐
    # # HORZ_CENTER = 0x02    居中对齐（水平方向上）
    # # HORZ_RIGHT = 0x03     右端对齐
    # al.horz = 0x02  # 设置水平居中
    # al.vert = 0x01  # 设置垂直居中
    # style.alignment = al
    #
    # newAddStyle = sqlExcute.selectNewAdd()



    # 保存
    workbook.save("新saaddssdas.xls")

writeToExcel()