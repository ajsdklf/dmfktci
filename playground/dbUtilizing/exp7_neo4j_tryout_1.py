# from langchain_openai import ChatOpenAI
# import os 
# from dotenv import load_dotenv
# import json
# from langchain.prompts import PromptTemplate

# load_dotenv()

# prompt = PromptTemplate(template="""
# You are a helpful assistant that can answer questions about the world.
# For the {question}, provide the answer that is helpful and relevant to the question. Your answer should be in the json format with the following keys:
# - question: the question that you are answering
# - answer: the answer to the question
# - source: the source of the answer, which should be the name of the person who provided the answer
# """, input_variables=["question"])

# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

# response = llm.invoke(prompt.format(question="What is the capital of France?"))
# print(f"Pure LLM response: {response}")
# print("--------------------------------")

# from langchain.output_parsers.json import SimpleJsonOutputParser

# json_parser = SimpleJsonOutputParser()

# chain = prompt | llm | json_parser 

# response = chain.invoke({"question": "What is the capital of France?"})
# print(f"Chain response: {response}")
# print("--------------------------------")

# response = llm.invoke(
#     input=prompt.format(question="What is the capital of France?"),
#     response_format={'type': 'json_object'}
# ).content
# print(f"Pure LLM response: {json.loads(response)}")
# print("--------------------------------")



# # chat model 
# from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# chat_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

# instruction = SystemMessage(content="You are a helpful assistant that can answer questions about the world.")
# question = HumanMessage(content="What is the capital of France?")

# response = chat_llm.invoke(
#     input=[instruction, question]
# )
# print(f"Chat response: {response.content}")
# print("--------------------------------")


# from langchain.schema import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are a helpful assistant that can answer questions about the world."),
#         ("human", "{question}")
#     ]
# )

# chat_chain = prompt | chat_llm | StrOutputParser()

# response = chat_chain.invoke({"question": "What is the capital of France?"})
# print(f"Chat Chain response: {response}")
# print("--------------------------------")

from neo4j import GraphDatabase
import os 
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_USER = "neo4j"

with GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
) as driver:
    driver.verify_connectivity()
    events = driver.session().run("MATCH (e:Event) RETURN e.service_title AS service_title")
    for event in events:
        print(event["service_title"])