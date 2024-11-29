import json 
import pandas as pd

with open('./database_try1/exp13_db_compiling.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

print(db)

df = pd.DataFrame(db)
df.to_csv('./database_try1/exp14_csv_building_ver2.csv', index=False, encoding='utf-8')