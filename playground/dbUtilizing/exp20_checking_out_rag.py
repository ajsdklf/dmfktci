import json
from openai import OpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os 
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

embeddings = OpenAIEmbeddings(model='text-embedding-3-large', api_key=os.getenv('OPENAI_API_KEY'))

db_service_description = Chroma(persist_directory='./database_try1/exp19_vector_db_service_description', embedding_function=embeddings)
db_target_summary = Chroma(persist_directory='./database_try1/exp19_vector_db_target_summary', embedding_function=embeddings)

query = input("찾고 있는 서비스 관련 정보 혹은 본인 관련 정보를 자유롭게 입력해주세요!")

if query:
    QUERY_MAPPER_SYSTEM_PROMPT = """
    You are tasked with mapping the user's query to either the [SERVICE_DESCRIPTION] or [TARGET_SUMMARY] vector database.
    If the user's query is related to the service description, return "SERVICE_DESCRIPTION".
    If the user's query is related to the target summary, return "TARGET_SUMMARY".
    If the user's query is not related to either, just return "SERVICE_DESCRIPTION".
    """
    
    query_category = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": QUERY_MAPPER_SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )
    query_category = query_category.choices[0].message.content

    if query_category == "SERVICE_DESCRIPTION":
        docs = db_service_description.similarity_search(query, k=40)
    elif query_category == "TARGET_SUMMARY":
        docs = db_target_summary.similarity_search(query, k=40)

    for doc in docs:
        metadata = json.loads(doc.metadata['original_data'])
        if metadata['cluster_id'] == 10:
            print(doc.page_content)
            print("-"*100)