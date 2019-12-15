# -*- coding:utf-8 -*-
from django.shortcuts import render
from toolkit.pre_load import pre_load_thu
from toolkit.pre_load import neo_con
import random
import re

thu_lac = pre_load_thu
db = neo_con
pattern = [[r"相关关系?",r"所在律师事务所?"],]
def question_answering(request):  # index页面需要一开始就加载的内容写在这里
	context = {'ctx':''}
	if(request.GET):
		question = request.GET['question']
		cut_statement = thu_lac.cut(question,text=False)
		address_name = []
		weather_name = []
		question_name = ""
		ret_dict = {}
		ret_dict_2 = {}
		pos = -1
		q_type = -1
		# for i in range(len(pattern)):
		# 	for x in pattern[i]:
		# 		index = re.search(x, question)
		if (question[4:]=="相关关系?"):
			cut = cut_statement[0][0]+cut_statement[1][0]
			shoudu = db.findRelationByEntity(cut)
			# pos = index.span()[0]
			# q_type = i
			# break
		if (str(question[4:])=="所在律师事务所？"):
			cut = cut_statement[0][0]+cut_statement[1][0]
			shoudu = db.findOtherEntities(cut, "所在律师事务所")
			if shoudu != []:
				ret_dict["list"] = []
				ret_dict_2["list"] = []
				ret_dict_2["answer"] = []
				for i in shoudu:
					ret_dict['list'].append(
						{'entity1': i["n1"], 'rel': i["rel"], 'entity2': i["n2"]})
				for i in ret_dict["list"]:
					ret_dict_2["list"].append(
						{"entity1":i["entity1"]["name"], "rel":i["rel"]["type"], "entity2":i["entity2"]["name"],
						 "entity1_type":"地点", "entity2_type":"气候"})
				for j in ret_dict["list"]:
					ret_dict_2["answer"].append(j["entity2"]["name"])
					# for j in i["n2"]:
						# ret_dict["answer"].append(j["name"])
					# ret_dict['list'] = [{'entity1': cut, 'rel': '所在律师事务所', 'entity2': shoudu}]
		if(len(ret_dict)!=0  and ret_dict!=0):
			# print(ret_dict)
			return render(request,'question_answering.html',{'ret':ret_dict_2})
		# print(context)
		return render(request, 'question_answering.html', {'ctx':'暂未找到答案'})
	return render(request, 'question_answering.html', context)



















