import os
import csv
url_name = {}   # 预加载实体到标注的映射字典
filePath = os.getcwd()
import pandas as pd
with open(filePath+'/data/stock.csv','r',encoding="utf-8") as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		# row = pandas.DataFrame(row, columns=["index:ID","name","code","status",":LABEL","业绩变动","预计净利润(元)","业绩变动幅度","业绩变动原因","预告类型","上年同期净利润(元)","公告日期"])
		# if len(row[2]) == 1:
		# 	row[2].zfill(6)
		# elif len(row[2]) == 2:
		# 	row[2].zfill(6)
		# elif len(row[2]) == 3:
		# 	row[2].zfill(6)
		# elif len(row[2]) == 4:
		# 	row[2].zfill(6)
		# elif len(row[2]) == 5:
		row[2] = row[2].zfill(6)
		url_name[str(row[1]).strip()] = row[2] #{key:value} {'平安银行': "0000001"}

print('url_name load over!')#predicted labels load over!

import thulac
pre_load_thu = thulac.thulac()  #默认模式
print('thulac open!')

from Model.neo_models import Neo4j
neo_con = Neo4j()   #预加载neo4j
neo_con.connectDB()
print('neo4j connected!')