# author: Curry
import pandas as pd
import json
from matplotlib import pyplot as plt 
import csv
import codecs
import requests
import time
import os
resp = requests.get("http://sa.sogou.com/new-weball/api/sgs/epidemic/all-chart/data")
jsData = json.loads(resp.text)
csvFile = open("./data/{}.csv".format(time.strftime("%m-%d")), "w", newline='', encoding='gbk')
csvObj = csv.writer(csvFile)
header = []
rows = []

jsData.pop("code") # 这一项先删除免得影响后面程序
header.append("自1月20的天数")
header.append("日期")

# 数据装填

# 表头
chart2Header = ["全国累计趋势对比", "湖北内外新增确诊数对比", "湖北内外治愈率对比", "湖北内外病死率对比"]
index = 0
flag = False
for i in jsData:
    for j in jsData[i]:
        if j == "series":
            for seriesNo in range(0, len(jsData[i][j])):
                if i.find("Hubei") == -1 :
                    flag = False
                    header.append(jsData[i][j][seriesNo]["name"])
                else :
                    flag = True
                    header.append("{}-{}".format(chart2Header[index],jsData[i][j][seriesNo]["name"]))
            if flag :
                index+=1

# 日期列
dataSet = set()
for i in jsData:
    for j in jsData[i]:
        if j == "x":
            for k in jsData[i][j]:
                dataSet.add(k["value"])
dataSet = sorted(dataSet)

# 所有数据列
columns = []
for i in jsData:
    for j in jsData[i]:
        if j == "series":
            for seriesNo in range(0, len(jsData[i][j])):
                column = [] # 新建一列
                for k in jsData[i][j][seriesNo]["data"]:
                    if type(k) is dict :
                        column.append(k["value"])
                    else :
                        column.append(k)
                columns.append(column) # 把当前列装进所有列
    
# 按行构建
for i in range(0, len(dataSet)) : # 所有数据有日期那么多行 所以取日期集合长度
    row = []
    row.append(i+1)
    row.append(dataSet[i])
    for j in range(0, len(columns)):
        row.append(columns[j][i])
    rows.append(row) # 把当前行装进所有行
    
csvObj.writerow(header)
csvObj.writerows(rows)

print("{}已经保存成功".format(csvFile.name))

csvFile.close()