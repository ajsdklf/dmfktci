from openai import OpenAI 
import json 

client = OpenAI()
with open('./database_try1/exp13_db_compiling.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

print(db)

target_informations = []

for data in db:
    print(data['target_content'])
    print("---"*33)
    
    extracted_target_information = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are an assistant that extracts eligibility information from given content. The output should only contain eligibility criteria and no other information. Follow these guidelines when extracting information:

1. Enter 'None' if the information is not provided.
2. Information should be clear and non-redundant.
3. Extract restrictions for these four categories:
- Age restrictions (e.g., '18세 이상', '14-34세', '65세 이상')
- Income restrictions (e.g., '중위소득 120% 이하', '기초생활수급자', '월소득 50만원 이상') 
- Location restrictions (e.g., '광주광역시 주민등록', '대구시 거주 1년 이상')
- Other restrictions (Any qualifications, status, situations, or other relevant restrictions)

4. Output in the following JSON format:
{
    "age_restriction": ["List of age restrictions"],
    "income_restriction": ["List of income restrictions"], 
    "location_restriction": ["List of location restrictions"],
    "other_restrictions": ["List of other restrictions"]
}

Be precise and comprehensive in extracting all relevant eligibility criteria while maintaining clarity and avoiding redundancy. Your response has to be **IN KOREAN**."""},
            {"role": "user", "content": data['target_content']}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    print(extracted_target_information.choices[0].message.content)
    target_informations.append(
        {
            "service_id": data['service_id'],
            "target_informations": json.loads(extracted_target_information.choices[0].message.content),
            "service_description": data['service_description']
        }
    )
    print(target_informations)
    print("---"*33)

with open('./database_try1/exp15_target_informations.json', 'w', encoding='utf-8') as f:
    json.dump(target_informations, f, ensure_ascii=False, indent=4)

