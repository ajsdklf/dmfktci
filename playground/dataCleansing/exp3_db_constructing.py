from bs4 import BeautifulSoup
import json 

with open('./database_try1/xml_sample_data.json', 'r', encoding='utf-8') as f:
    datasets = json.load(f)

processed_data = []
for i, data in enumerate(datasets):
    # Process service title and description
    service_title = data['service_title']
    service_description = data['service_description']
    
    # Process main content
    main_contents = []
    soup = BeautifulSoup(data['main_content'], 'html.parser')
    content_list = soup.find_all('li')
    for content in content_list:
        content = content.text.strip()
        main_contents.append(content)
        
    # Process target content
    soup = BeautifulSoup(data['target_content'], 'html.parser')
    target_description = soup.find('div', {'class': 'service-detail-inner'})
    target_text = target_description.text.strip() if target_description else ""
    
    # Process support content
    soup = BeautifulSoup(data['support_content'], 'html.parser')
    support_description = soup.find('div', {'class': 'service-detail-inner'})
    support_text = support_description.text.strip() if support_description else ""
    
    soup = BeautifulSoup(data['apply_content'], 'html.parser')
    apply_description = soup.find('div', {'class': 'service-detail-inner'})
    apply_text = apply_description.text.strip() if apply_description else ""
    
    # Process contact content
    soup = BeautifulSoup(data['contact_content'], 'html.parser')
    contact_description = soup.find('div', {'class': 'service-detail-inner'})
    contact_text = contact_description.text.strip() if contact_description else ""
    
    processed_data.append({
        'service_title': service_title,
        'service_description': service_description,
        'main_contents': main_contents,
        'target_content': target_text,
        'support_content': support_text,
        'apply_content': apply_text,
        'contact_content': contact_text
    })
    
    print(f"currently {i} / {len(datasets)}")

with open('./database_try1/exp3_pre-processed_data.json', 'w', encoding='utf-8') as f:
    json.dump(processed_data, f, ensure_ascii=False, indent=4)