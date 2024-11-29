import json 
from openai import OpenAI

client = OpenAI()

with open('./database_try1/exp9_smaller_db.json', 'r') as f:
    dataset = json.load(f)
print(len(dataset))

dataset = [item for item in dataset if item['service_description'] != '']
print(len(dataset))

with open('./database_try1/exp12_db_without_none.json', 'w', encoding='utf-8') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=4)


with open('./database_try1/exp12_db_without_none.json', 'r') as f:
    dataset = json.load(f)

print(len(dataset))

with open('./database_try1/exp11_clusters.json', 'r') as f:
    clusters = json.load(f)

clusters_string = json.dumps(clusters, ensure_ascii=False, indent=4)
print(clusters_string)

SYSTEM_PROMPT_TO_MAP_CATEGORIES_TO_CLUSTERS = """
You are tasked with mapping the categories provided to the cluster topics of: 

{clusters_string}

Think step by step to analyze in which cluster each category belongs to the best possible way. Your response has to be in JSON format and should follow the following format:
{{
    'service_id': [provided service_id],
    'service_description': [provided service_description],
    'service_title': [provided service_title],
    'cluster_id': [id of the cluster that the service belongs to],
    'cluster_topic': [topic of the cluster that the service belongs to]
}}
You should never leave the cluster_id and cluster_topic empty.
"""

USER_PROMPT_TO_MAP_CATEGORIES_TO_CLUSTERS = """
Description of the service you have to map to the clusters is [{data}].
"""

mapped_dataset = []
for idx, data in enumerate(dataset):
    data = {
        'service_id': data['id'],
        'service_description': data['service_description'],
        'service_title': data['service_title']
    }
    mapped_data = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_TO_MAP_CATEGORIES_TO_CLUSTERS.format(clusters_string=clusters_string)}, 
            {"role": "user", "content": USER_PROMPT_TO_MAP_CATEGORIES_TO_CLUSTERS.format(data=data)}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    mapped_dataset.append(json.loads(mapped_data.choices[0].message.content))
    print(f'{idx} / {len(dataset)}')

with open('./database_try1/exp12_mapped_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(mapped_dataset, f, ensure_ascii=False, indent=4)

with open('./database_try1/exp12_mapped_dataset.json', 'r') as f:
    mapped_dataset = json.load(f)

number_of_cluster_1 = 0
number_of_cluster_2 = 0
number_of_cluster_3 = 0
number_of_cluster_4 = 0
number_of_cluster_5 = 0
number_of_cluster_6 = 0
number_of_cluster_7 = 0
number_of_cluster_8 = 0
number_of_cluster_9 = 0
number_of_cluster_10 = 0
for dataset in mapped_dataset:
    if dataset['cluster_id'] == 1:
        number_of_cluster_1 += 1
    elif dataset['cluster_id'] == 2:
        number_of_cluster_2 += 1
    elif dataset['cluster_id'] == 3:
        number_of_cluster_3 += 1
    elif dataset['cluster_id'] == 4:
        number_of_cluster_4 += 1
    elif dataset['cluster_id'] == 5:
        number_of_cluster_5 += 1
    elif dataset['cluster_id'] == 6:
        number_of_cluster_6 += 1
    elif dataset['cluster_id'] == 7:
        number_of_cluster_7 += 1
    elif dataset['cluster_id'] == 8:
        number_of_cluster_8 += 1
    elif dataset['cluster_id'] == 9:
        number_of_cluster_9 += 1
    elif dataset['cluster_id'] == 10:
        number_of_cluster_10 += 1
print(number_of_cluster_1, number_of_cluster_2, number_of_cluster_3, number_of_cluster_4, number_of_cluster_5, number_of_cluster_6, number_of_cluster_7, number_of_cluster_8, number_of_cluster_9, number_of_cluster_10)