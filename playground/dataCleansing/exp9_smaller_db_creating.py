import json 
import pandas as pd 

with open('./database_try1/exp4_cleansed_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(data)
print(type(data))
print(len(data))

data = data[:100]
print(len(data))

with open('./database_try1/exp9_smaller_db.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

df = pd.DataFrame(data)
print(df.head())
df.to_csv('./database_try1/exp9_smaller_db.csv', index=False, encoding='utf-8')