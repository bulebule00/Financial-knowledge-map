from py2neo import Graph

class Neo4j():
	graph = None
	def __init__(self):
		print("create neo4j class ...")
	def connectDB(self):
		self.graph = Graph("http://localhost:7474", username="Graph_J", password="123456")
	# 根据entity的名称返回关系 --->实体查询
	def getEntityRelationbyEntity(self, value):
		answer = self.graph.run("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.name = \"" + str(
			value) + "\" RETURN entity1, rel, entity2").data()
		"MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.name='平安银行' RETURN entity1, rel, entity2"
		return answer

	# 根据title值返回互动百科item --->实体识别
	def matchHudongItembyTitle(self,value):
		# sql = "MATCH (n:企业 { name: '" + str(value) + "' }) return n;"
		try:
			answer = self.graph.run("MATCH (n:N_Company_Boss { name: '" + str(value) + "' }) return n").data()
			if answer is None:
				answer = self.graph.run("MATCH (n:Company_Boss { name: '" + str(value) + "' }) return n").data()
		except:
			pass
		return answer

	#查找entity1及其对应的关系（与getEntityRelationbyEntity的差别就是返回值不一样） entity1="苹果" 无关系
	def findRelationByEntity(self,entity1):
		answer = self.graph.run("MATCH (n1 {name:\""+str(entity1)+"\"})- [rel] -> (n2) RETURN n1,rel,n2").data()
		# if(answer is None):
		# 	answer = self.graph.run("MATCH (n1:NewNode {title:\""+entity1+"\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
		return answer

	#查找entity2及其对应的关系 #entity2="香蕉" 无关系
	def findRelationByEntity2(self,entity1):
		answer = self.graph.run("MATCH (n1)- [rel] -> (n2 {name:\""+str(entity1)+"\"}) RETURN n1,rel,n2").data()
		# if(answer is None):
		# 	answer = self.graph.run("MATCH (n1)- [rel] -> (n2:NewNode {title:\""+entity1+"\"}) RETURN n1,rel,n2" ).data()
		return answer

	# 根据两个实体查询它们之间的最短路径
	def findRelationByEntities(self, entity1, entity2):
		try:
			answer = self.graph.run(
				"MATCH (p1:N_Company_Boss {name:\"" + str(entity1) + "\"}),(p2:N_Company_Boss{name:\"" + str(
					entity2) + "\"}),p=shortestpath((p1)-[*..10]-(p2)) RETURN  p").evaluate()
			#MATCH (p1:Company_Boss {name:"超声电子"}),(p2:Company_Boss{name:"猛狮科技"}),p=shortestpath((p1)-[*..10]-(p2)) RETURN p
	#MATCH (p1:`企业` {name:"超声电子"}), (p2:`企业` {name:"猛狮科技"}), p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN rel
		# https://www.jianshu.com/p/b7dcdb4d4799
		# answer = self.graph.run("MATCH (p1:HudongItem {title:\"" + entity1 + "\"})-[rel:RELATION]-(p2:HudongItem{title:\""+entity2+"\"}) RETURN p1,p2").data()
		except:
			answer = None
		else:
			if answer is None:
				try:
					answer = self.graph.run(
						"MATCH (p1:Company_Boss {name:\"" + str(entity1) + "\"}),(p2:Company_Boss{name:\"" + str(
							entity2) + "\"}),p=shortestpath((p1)-[*..10]-(p2)) RETURN  p").evaluate()
				except:
					pass
			if answer is None:
				answer = self.graph.run(
					"MATCH (p1:N_Company_Boss {name:\"" + str(entity1) + "\"}),(p2:Company_Boss{name:\"" + str(
						entity2) + "\"}),p=shortestpath((p1)-[*..10]-(p2)) RETURN  p").evaluate()
			if answer is None:

				answer = self.graph.run(
					"MATCH (p1:Company_Boss {name:\"" + str(entity1) + "\"}),(p2:N_Company_Boss{name:\"" + str(
						entity2) + "\"}),p=shortestpath((p1)-[*..10]-(p2)) RETURN  p").evaluate()
		# 我们有不同的实体, 进行不同文件的查询,
		# NewNode 和 HudongItem中都有苹果和一系列对应的关系。
		# answer = self.graph.data("MATCH (n1:HudongItem {title:\"" + entity1 + "\"})- [rel] -> (n2:HudongItem{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
		# if(answer is None):
		#	answer = self.graph.data("MATCH (n1:HudongItem {title:\"" + entity1 + "\"})- [rel] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
		# if(answer is None):
		#	answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel] -> (n2:HudongItem{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
		# if(answer is None):
		#	answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
		relationDict = []
		if (answer is not None):
			for x in answer:
				tmp = {}
				start_node = x.start_node
				end_node = x.end_node
				tmp['n1'] = start_node
				tmp['n2'] = end_node
				tmp['rel'] = x
				relationDict.append(tmp)
		return relationDict

	#查询数据库中是否有对应的实体-关系匹配  entity1="苹果"  无关系  entity2="香蕉"
#match (b:Company_Boss{name:"平安银行"})-[*0..3]-(h)return distinct b, h
	#MATCH (n1:N_Company_Boss {name:"平安银行"})- [rel:RELATION {type:"业务方向"}] -> (n2:N_Company_Boss{name:"深科技"}) RETURN n1,rel,n2
	def findEntityRelation(self,entity1,relation,entity2):
		answer = self.graph.run("MATCH (n1:N_Company_Boss {name:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:N_Company_Boss{name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
		if(answer is None):#relation
			answer = self.graph.run("MATCH (n1:N_Company_Boss {name:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:Company_Boss{name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
		if(answer is None):
			answer = self.graph.run("MATCH (n1:Company_Boss {name:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:N_Company_Boss{name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
		if(answer is None):
			answer = self.graph.run("MATCH (n1:Company_Boss {name:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:Company_Boss{name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
		return answer

	#根据entity1和关系查找enitty2
	def findOtherEntities(self,entity,relation):
		answer = self.graph.run("MATCH (n1 {name:\"" + str(entity) + "\"})- [rel {type:\""+str(relation)+"\"}] -> (n2) RETURN n1,rel,n2" ).data()
		#if(answer is None):
		#	answer = self.graph.run("MATCH (n1:NewNode {title:\"" + entity + "\"})- [rel:RELATION {type:\""+relation+"\"}] -> (n2) RETURN n1,rel,n2" ).data()

		return answer

	#根据entity2和关系查找enitty1
	def findOtherEntities2(self,entity,relation):
		answer = self.graph.run("MATCH (n1)- [rel {type:\""+str(relation)+"\"}] -> (n2 {name:\"" + str(entity) + "\"}) RETURN n1,rel,n2" ).data()
		#if(answer is None):
		#	answer = self.graph.run("MATCH (n1)- [rel:RELATION {type:\""+relation+"\"}] -> (n2:NewNode {title:\"" + entity + "\"}) RETURN n1,rel,n2" ).data()

		return answer



