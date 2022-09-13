
from Database import Database
import re

# 设置连接数据库的参数
config = {
    "host": "localhost",
    "port": 3306,
    "database": "homework1",
    "charset": "utf8",
    "user": "root",
    "password": "123456"

}

# 实例化时就直接传参数
db = Database(**config)
#
# dateInfo新增一条数据
def insertToDateInfo(date,newAdd,newAsymptomatic):
    db.insertToDateInfo("dateInfo",date,newAdd,newAsymptomatic)

# areaInfo新增数据
def insertToAreaInfo(area,newAdd,newAsymptomatic,date):
    db.insertToAreaInfo("areaInfo",area,newAdd,newAsymptomatic,date)

#dateInfo查询日期数据返回日期list
def selectFromDateInfo():
     list = db.select_all('dateInfo','','date')
     return list
    # return re.findall('[0-9]+月[0-9]+日',str(list))

#通过日期查询全国新增
def selectNewAdd(date):
    newAdd = db.select_one('dateInfo','date = "'+ date+'"' ,'newAdd')
    # return newAdd
    return re.findall('([0-9]+)',str(newAdd))#[0]

#通过日期查询全国新增无症状
def selectNewAsymptomatic(date):
    newAsymptomatic = db.select_one('dateInfo','date = "'+ date+'"' ,'newAsymptomatic')
    return re.findall('([0-9]+)',str(newAsymptomatic))

#查询省份
def selectProvince():
    provinces = db.select_all('areaInfo','date = "2022-08-02"','area')
    return provinces

#查询省份新增
def selectProvinceNewAdd(date,province):
    newAdd = db.select_one('areaInfo','date = "' + date +'"AND area ="' + str(province) + '"','newAdd')
    return newAdd

#查询省份无症状
def selectProvinceAsymptomatic(date,province):
    newAsymptomatic = db.select_one('areaInfo','date = "' + date +'"AND area ="' + str(province) + '"','newAsymptomatic')
    return newAsymptomatic
