import os 
from neo4j import GraphDatabase
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
driver = GraphDatabase.driver(URI, auth=AUTH)
driver.verify_connectivity()

with driver.session() as session:
    query = """
    MATCH (e: Event {service_id: 1})-[:BELONGS_TO]->(c: Cluster)
    return e, c
    """
    result = session.run(query)
    for record in result:
        print(record.get('e'))
        print(record.get('c'))


with driver.session() as session:
    query = """
    WITH genai.vector.encode(
        "안녕하세요. 저는 중소득층입니다.",
        "OpenAI",
        {token: $token}
    ) AS embedding
    RETURN embedding
    """
    result = session.run(query, token=OPENAI_API_KEY)
    for record in result:
        print(record.get('embedding'))