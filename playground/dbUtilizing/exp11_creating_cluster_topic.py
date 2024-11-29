# there will be 10 clusters 

import json
from openai import OpenAI

client = OpenAI()

with open('./database_try1/exp9_smaller_db.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(data)

categories = []
for data_ in data:
    categories.append(data_['service_description'])

print(len(categories))

print(categories)
categories = [category for category in categories if category != '']

print(categories)
print(len(categories))

categories_string = json.dumps(categories)

clusters = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": """You are a helpful assistant that is tasked to create clusters from the given categories. You need to come up with cluster topics that best represent the categories. Number of clusters you are creating can differ by your judgement. Clusters you are creating have to follow the follwing rules:
            ---
            1. Each cluster has to be representative.
            2. Each cluster has to be diverse.
            3. Each cluster has to be mutually exclusive.
            4. Each cluster has to be exhaustive.
            5. Examples of good clusters: 
                - 청년 지원 서비스 
                - 장애인 지원 서비스 
                - 주택 지원 서비스
                - 출산 지원 서비스
            ---
            Your output has to be in Korean and should follow the JSON format of: 
            [
                {'cluster_topic': 'topic_1', 'cluster_id': 1},
                {'cluster_topic': 'topic_2', 'cluster_id': 2},
                ...
            ]
            Think step by step to come up with the most appropriate cluster topics.
            """}, {"role": "user", "content": categories_string}],
    temperature=0,
    response_format={"type": "json_object"}
).choices[0].message.content

print(clusters)

clusters = json.loads(clusters)

with open('./database_try1/exp11_clusters.json', 'w', encoding='utf-8') as f:
    json.dump(clusters, f, ensure_ascii=False, indent=4)