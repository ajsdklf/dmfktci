import json 

with open('./database_try1/exp3_pre_processed_data_sample.json', 'r', encoding='utf-8') as f:
    datasets = json.load(f)

for dataset in datasets:
    for key, value in dataset.items():
        print(key)
        print(value)
    break