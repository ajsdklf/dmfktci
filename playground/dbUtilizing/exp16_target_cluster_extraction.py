import json 
from openai import OpenAI

client = OpenAI()

with open('./database_try1/exp16_target_informations_updated.json', 'r', encoding='utf-8') as f:
    target_informations = json.load(f)

age_restrictions = []
location_restrictions = []
income_restrictions = []
other_restrictions = []

for target_information in target_informations:
    age_restrictions.append(target_information['target_informations']['age_restriction'])
    location_restrictions.append(target_information['target_informations']['location_restriction'])
    income_restrictions.append(target_information['target_informations']['income_restriction'])
    other_restrictions.append(target_information['target_informations']['other_restrictions'])

# print(age_restrictions)
# print(len(age_restrictions))
# print("---"*33)
# print(location_restrictions)
# print(len(location_restrictions))
# print("---"*33)
# print(income_restrictions)
# print(len(income_restrictions))
# print("---"*33)
# print(other_restrictions)
# print(len(other_restrictions))
# print("---"*33)

# age_restrictions = [item for item in age_restrictions if item != ['None']]
# print(len(age_restrictions))
# print("---"*33)
# location_restrictions = [item for item in location_restrictions if item != ['None']]
# print(len(location_restrictions))
# print("---"*33)
# income_restrictions = [item for item in income_restrictions if item != ['None']]
# print(len(income_restrictions))
# print("---"*33)
# other_restrictions = [item for item in other_restrictions if item != ['None']]
# print(len(other_restrictions))
# print("---"*33)

updated_age_restrictions = []
for age_restriction in age_restrictions:
    cleaned_age_restriction = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts and cleans up age restrictions from a given text. Follow the following instructions: 1. When restrictions indicate that only those above a certain age are eligible, return '18세 이상'. (18 is just an example number) 2. When the restrictions indicate that only those below a certain age are eligible, return '18세 미만'. 3. When the input is empty, return 'None'. 4. When the restriction indicates that those between two ages are eligible, return '18세~25세' (18 and 25 are just example numbers). Your output has to be a json object with a single array of strings as the value of 'age_restriction' key."},
            {"role": "user", "content": f"Please clean up the following age restrictions: {json.dumps(age_restriction, ensure_ascii=False)}."}
        ],
        response_format={"type": "json_object"}
    )
    # print(cleaned_age_restriction.choices[0].message.content)
    try:
        if cleaned_age_restriction.choices[0].message.content is not None:
            cleaned_age_restriction = json.loads(cleaned_age_restriction.choices[0].message.content)
        updated_age_restrictions.append(
            {
                "service_id": target_information['service_id'],
                "age_restriction": cleaned_age_restriction['age_restriction'],
                "location_restriction": target_information['target_informations']['location_restriction'],
                "income_restriction": target_information['target_informations']['income_restriction'],
                "other_restrictions": target_information['target_informations']['other_restrictions'],
                "service_description": target_information['service_description'],
                "service_title": target_information['service_title']
            }
        )
    except json.JSONDecodeError:
        print(f"Failed to parse JSON: {cleaned_age_restriction.choices[0].message.content}")

print(updated_age_restrictions)
with open('./database_try1/exp16_target_informations_updated.json', 'w', encoding='utf-8') as f:
    json.dump(updated_age_restrictions, f, ensure_ascii=False)