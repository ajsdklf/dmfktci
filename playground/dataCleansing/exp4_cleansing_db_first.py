import json
import re

with open('./database_try1/exp3_pre_processed_data.json', 'r', encoding='utf-8') as f:
    datasets = json.load(f)

cleansed_datasets = []
for dataset in datasets:
    cleaned_dataset = {}
    for key, value in dataset.items():
        if isinstance(value, str):
            # Remove multiple spaces while preserving single spaces
            value = re.sub(r'\s+', ' ', value)
            # Strip leading/trailing whitespace
            value = value.strip()
        elif isinstance(value, list):
            # Handle lists of strings
            value = [re.sub(r'\s+', ' ', v).strip() if isinstance(v, str) else v for v in value]
        cleaned_dataset[key] = value
    cleansed_datasets.append(cleaned_dataset)

with open('./database_try1/exp4_cleansed_data.json', 'w', encoding='utf-8') as f:
    json.dump(cleansed_datasets, f, ensure_ascii=False, indent=4)
