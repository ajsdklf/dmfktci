import json

with open('./database_try1/exp13_db_compiling.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

print(db)

with open('./database_try1/exp16_target_informations_updated.json', 'r', encoding='utf-8') as f:
    target_informations = json.load(f)

age_restrictions = []
for target_information in target_informations:
    age_restrictions.append(target_information['target_informations']['age_restriction'])

print(age_restrictions)
print(len(age_restrictions))

new_db = []
for idx, age_restriction in enumerate(age_restrictions):
    new_db.append({
        **db[idx],
        "age_restriction": age_restriction
    })

print(new_db)

with open('./database_try1/exp17_db_compiling_with_age_restriction.json', 'w', encoding='utf-8') as f:
    json.dump(new_db, f, ensure_ascii=False, indent=4)