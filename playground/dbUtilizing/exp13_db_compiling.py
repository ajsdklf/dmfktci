import json 

with open('./database_try1/exp12_mapped_dataset.json', 'r', encoding='utf-8') as f:
    mapped_dataset = json.load(f)

print(mapped_dataset)

with open('./database_try1/exp9_smaller_db.json', 'r', encoding='utf-8') as f:
    original_dataset = json.load(f)

print(original_dataset)

updated_dataset = []
for idx, data in enumerate(mapped_dataset):
    index = data['service_id']
    orginal_data = original_dataset[index]
    updated_data = {
        **orginal_data,
        **data
    }
    updated_dataset.append(updated_data)

with open('./database_try1/exp13_db_compiling.json', 'w', encoding='utf-8') as f:
    json.dump(updated_dataset, f, ensure_ascii=False, indent=4)