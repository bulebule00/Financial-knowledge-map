from py2neo import Graph

class Neo4j():
	graph = None
	def __init__(self):
		print("create neo4j class ...")
	def connectDB(self):
		self.graph = Graph("http://localhost:7474", username="Graph", password="123456")

