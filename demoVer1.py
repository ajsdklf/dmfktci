from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import json
import streamlit as st 
from openai import OpenAI 
import os 
from dotenv import load_dotenv
from neo4j import GraphDatabase
from prompts_for_demo1 import *
load_dotenv()

# Set page config
st.set_page_config(
    page_title="서비스 추천 시스템",
    page_icon="🎯",
    layout="wide"
)

# Apply custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

with st.spinner('시스템을 초기화하는 중...'):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    URI = os.getenv("NEO4J_URI")
    AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()

st.markdown('<p class="big-font">서비스 추천 시스템 🎯</p>', unsafe_allow_html=True)
st.markdown("---")

embeddings = OpenAIEmbeddings(model='text-embedding-3-large', api_key=os.getenv('OPENAI_API_KEY'))

db_service_description = Chroma(persist_directory='./database/exp19_vector_db_service_description', embedding_function=embeddings)
db_target_summary = Chroma(persist_directory='./database/exp19_vector_db_target_summary', embedding_function=embeddings)

# Load data with progress bar
with st.spinner('데이터를 불러오는 중...'):
    with open('./database/exp17_db_compiling_with_age_restriction.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

    with open('./database/exp11_clusters.json', 'r', encoding='utf-8') as f:
        clusters = json.load(f)

# Initialize session states
if "neo4j_data" not in st.session_state:
    st.session_state["neo4j_data"] = []
if "clusters" not in st.session_state:
    st.session_state["clusters"] = clusters
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "db" not in st.session_state:
    st.session_state["db"] = db
if "filtered_db" not in st.session_state:
    st.session_state["filtered_db"] = []
if "mapped_cluster" not in st.session_state:
    st.session_state["mapped_cluster"] = None
if 'step' not in st.session_state:
    st.session_state['step'] = 1
if 'age' not in st.session_state:
    st.session_state['age'] = None

# Create two columns for expanders
col1, col2 = st.columns(2)
with col1:
    with st.expander("서비스 클러스터 정보 📊"):
        st.json(st.session_state["clusters"])
with col2:
    with st.expander("데이터베이스 정보 💾"):
        st.json(st.session_state["db"])

# Display chat history in a container
with st.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])

# Display Neo4j data in a clean format
if st.session_state['neo4j_data']:
    with st.expander("Neo4j 데이터 🔍"):
        st.json(st.session_state['neo4j_data'])

# Step 1: Service Query
if st.session_state['step'] == 1:
    st.info("👋 원하시는 서비스에 대해 설명해주세요!")
    user_query = st.chat_input("찾고자 하는 서비스에 대해 설명해주세요. [ex. 주택 지원 서비스, 건강 지원 서비스, 소득 지원 서비스 등]")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_query)
        
        with st.spinner('서비스를 분석하는 중...'):
            mapped_cluster = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT_TO_MAP_QUERY_TO_CLUSTER.format(clusters=st.session_state["clusters"])},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            st.session_state.mapped_cluster = json.loads(mapped_cluster.choices[0].message.content)
            
        with st.chat_message("assistant", avatar="🤖"):
            st.success("서비스 매핑 완료!")
            st.json(st.session_state.mapped_cluster)
            
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.mapped_cluster})
        
        with st.spinner('데이터베이스 검색 중...'):
            cluster_id = st.session_state.mapped_cluster['cluster_id']
            filtered_db = [service for service in st.session_state["db"] if service["cluster_id"] == cluster_id]
            
            with driver.session() as session:
                query = """
                MATCH (e: Event)-[:BELONGS_TO]->(c: Cluster {cluster_id: $cluster_id})
                return e as event
                """
                result = session.run(query, cluster_id=cluster_id)
                for record in result:
                    with st.expander("관련 이벤트 정보"):
                        st.json(record.get('event'))
                    st.session_state['neo4j_data'].append(record.get('event'))
                    
        st.session_state['db'] = filtered_db
        st.session_state['step'] += 1
        st.rerun()

# Step 2: Age Input
if st.session_state['step'] == 2:
    st.success(f"🎯 검색된 서비스 수: {len(st.session_state['db'])}")
    st.info("👤 나이 정보를 입력해주세요!")
    user_query = st.chat_input('본인의 나이를 입력해주세요. (예: 만 20세라면 20 입력)')
    
    if user_query:
        try:
            st.session_state.messages.append({"role": "user", "content": user_query})
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(user_query)
                
            st.session_state['age'] = int(user_query)
            
            VALIDATOR_PROMPT_TO_FILTER_SERVICES_BY_AGE_RESTRICTION = """
            You are a helpful assistant that can help users find the services they need. As an input, you will be provided (1) User's current age, (2) Age restriction of the service. Your task is to check if the user's age satisfies the age restriction of the service. If it does, you should return "VALID". Otherwise, you should return "INVALID". Answer only with "VALID" or "INVALID".
            """.strip()
            
            progress_text = '나이 제한 확인 중...'
            with st.spinner(progress_text):
                for service in st.session_state['db']:
                    age_restriction = json.dumps(service['age_restriction'])
                    validator = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "system", "content": VALIDATOR_PROMPT_TO_FILTER_SERVICES_BY_AGE_RESTRICTION}, {"role": "user", "content": f"User's current age: {st.session_state['age']}, Age restriction of the service: {age_restriction}"}],
                        temperature=0.0,
                    )
                    if validator.choices[0].message.content == "VALID":
                        st.session_state['filtered_db'].append(service)
                        
            st.session_state['db'] = st.session_state['filtered_db']
            st.session_state['step'] += 1
            st.rerun()
            
        except ValueError:
            st.error("⚠️ 올바른 나이를 숫자로 입력해주세요!")

# Step 3: Display Results
if st.session_state['step'] == 3:
    st.success(f"✨ 조건에 맞는 서비스 수: {len(st.session_state['db'])}")
    
    user_query = st.chat_input("서비스에 대해 궁금한 점을 자유롭게 물어보세요!")
    
    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_query)
            
        with st.spinner('답변 생성 중...'):
            # Determine which vector DB to use based on query
            query_category = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are tasked with mapping the user's query to either the [SERVICE_DESCRIPTION] or [TARGET_SUMMARY] vector database. If the user's query is related to the service description, return 'SERVICE_DESCRIPTION'. If the user's query is related to the target summary, return 'TARGET_SUMMARY'. If the user's query is not related to either, just return 'SERVICE_DESCRIPTION'."},
                    {"role": "user", "content": user_query}
                ]
            )
            query_category = query_category.choices[0].message.content
            if query_category == "SERVICE_DESCRIPTION":
                db = db_service_description
                docs = db.similarity_search(user_query, k=20)
            elif query_category == "TARGET_SUMMARY":
                db = db_target_summary
                docs = db.similarity_search(user_query, k=20)
            final_docs = []
            for doc in docs:
                metadata = json.loads(doc.metadata['original_data'])
                if metadata['cluster_id'] == st.session_state['mapped_cluster']['cluster_id']:
                    final_docs.append(doc)
                    with st.expander(f"📌 {metadata['service_title']}"):
                        st.markdown("### 서비스 설명")
                        st.write(metadata['service_description'])
                        
                        st.markdown("### 지원 대상")
                        st.write(metadata['summarized_target_content'])
                        
                        st.markdown("### 지원 내용")
                        st.write(metadata['support_content'])
                        
                        st.markdown("### 신청 방법")
                        st.write(metadata['apply_content'])
                        
                        st.markdown("### 문의처")
                        st.write(metadata['contact_content'])
            st.write(f"당신께 딱 맞는 서비스를 {len(final_docs)}개 찾았습니다.")