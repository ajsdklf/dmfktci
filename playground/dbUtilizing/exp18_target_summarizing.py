import json 
from openai import OpenAI 

client = OpenAI()

with open('./database_try1/exp17_db_compiling_with_age_restriction.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

print(db)
new_db = []
for data in db:
    print(data['target_content'])
    summarzied_content = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': """
            You are an expert in summarizing provided input to a concise and informative summary. Be sure to include all important informations from the original content while making summary more concise and straight forward. Your answer should be in Korean and be in a format of sequence of sentences.
            """.strip()},
            {'role': 'user', 'content': data['target_content']}
        ],
    )
    print(summarzied_content.choices[0].message.content)
    data['summarized_target_content'] = summarzied_content.choices[0].message.content
    new_db.append(data)

with open('./database_try1/exp18_target_summarizing.json', 'w', encoding='utf-8') as f:
    json.dump(new_db, f, ensure_ascii=False, indent=4)
