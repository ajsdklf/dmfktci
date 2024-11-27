from datetime import datetime
import pandas as pd 
import json 

with open('./database_try1/exp4_cleansed_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
current_time = datetime.now()
df = pd.DataFrame(data)
finished_time = datetime.now()
taken_time = finished_time - current_time
print(f"Time taken: {taken_time}")
print(df.head())
df.to_csv(f'./database_try1/exp5_csv_from_json.csv', index=False, encoding='utf-8')