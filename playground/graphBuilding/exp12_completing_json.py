import json 

# with open('./database_try1/exp10_categories.json', 'r') as f:
#     dataset = json.load(f)
# print(len(dataset))

# dataset = [item for item in dataset if item['service_category'] != 'None']

# print(len(dataset))

# with open('./database_try1/exp12_categories_without_none.json', 'w', encoding='utf-8') as f:
#     json.dump(dataset, f, ensure_ascii=False, indent=4)


with open('./database_try1/exp12_categories_without_none.json', 'r') as f:
    dataset = json.load(f)

print(len(dataset))

with open('./database_try1/exp11_clusters.json', 'r') as f:
    clusters = json.load(f)

print(len(clusters))