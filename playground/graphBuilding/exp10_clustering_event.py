import json
from openai import OpenAI

client = OpenAI()

with open('./database_try1/exp9_smaller_db.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(data)

categories = []

for idx, data_ in enumerate(data):
    print(data_['service_description'])
    print('-'*100)
    service_category = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful assistant that is tasked to classify the service category of the given service description. Given the service_description, you need to classify the service into one word category. Think step by step to come up with the most appropriate category. Your output has to be one or two word answer. If there is no appropriate category, you can put 'None'."}, {"role": "user", "content": data_['service_description']}],
        temperature=0,
    ).choices[0].message.content
    print(service_category)
    categories.append(
        {
            "service_title": data_['service_title'],
            "service_category": service_category,
            "service_id": data_['id']
        }
    )
    print(f'{idx} / {len(data)}')

print(categories)
with open('./database_try1/exp10_categories.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, ensure_ascii=False, indent=4)