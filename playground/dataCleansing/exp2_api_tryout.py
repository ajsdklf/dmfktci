import requests
import xml.etree.ElementTree as ET

url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
params ={'serviceKey' : 'd+Ldwk5vbWYHLw8eG/hq6sjDnl0sX2BKyq0JVPOaZE4mKBZGx+NQQ/N1kKR7QRV4Bn1/cxjjvIuGDFYgikOyJg==', 'pageNo' : '1', 'numOfRows' : '3', 'entpName' : '', 'itemName' : '', 'itemSeq' : '', 'efcyQesitm' : '', 'useMethodQesitm' : '', 'atpnWarnQesitm' : '', 'atpnQesitm' : '', 'intrcQesitm' : '', 'seQesitm' : '', 'depositMethodQesitm' : '', 'openDe' : '', 'updateDe' : '', 'type' : 'xml' }

response = requests.get(url, params=params)
print(response.content)
print(type(response.content))
# xml_content = ET.fromstring(response.content)
# print(xml_content)

# print(xml_content.items())