import time
from neo4j import GraphDatabase
import os 
from dotenv import load_dotenv 

load_dotenv()
NEO4J_URI = os.getenv("NEO4J_URI")
print(NEO4J_URI)
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
print(NEO4J_PASSWORD)

uri = NEO4J_URI
username = "neo4j"
password = NEO4J_PASSWORD

start_time = time.time()
driver = GraphDatabase.driver(uri, auth=(username, password))
end_time = time.time()
print(f"Time taken to connect to Neo4j: {end_time - start_time} seconds")

print(driver.session())

driver.close()