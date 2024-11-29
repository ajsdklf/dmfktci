import json 
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

embeddings = OpenAIEmbeddings(model='text-embedding-3-large', api_key=OPENAI_API_KEY)

with open('./database_try1/exp18_target_summarizing.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# documents_for_service_description = []
# for data in db:
#     documents_for_service_description.append(Document(page_content=data['service_description'], metadata={'original_data': json.dumps(data)}))

# db = Chroma.from_documents(documents=documents_for_service_description, embedding=embeddings, persist_directory='./database_try1/exp19_vector_db_service_description')

documents_for_target_summary = []
for data in db:
    documents_for_target_summary.append(Document(page_content=data['summarized_target_content'], metadata={'original_data': json.dumps(data)}))

db = Chroma.from_documents(documents=documents_for_target_summary, embedding=embeddings, persist_directory='./database_try1/exp19_vector_db_target_summary')