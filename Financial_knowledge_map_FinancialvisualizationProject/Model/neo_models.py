from py2neo import Graph

class Neo4j():
	graph = None
	def __init__(self):
		print("create neo4j class ...")
	def connectDB(self):
		self.graph = Graph("http://localhost:7474", username="Graph_n", password="123456")

	# 根据entity的名称返回关系
	def getEntityRelationbyEntity(self, value):
		answer = self.graph.run("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.name = \"" + str(
			value) + "\" RETURN entity1, rel, entity2").data()
		"MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.name='平安银行' RETURN entity1, rel, entity2"
		return answer