from Model.neo_models import Neo4j

neo_con = Neo4j()   #预加载neo4j
neo_con.connectDB()
print('neo4j connected!')