
import json
import requests

url = 'http://localhost:5000/?name=zhengys&age=26'
req = requests.get(url=url)
print req.status_code
print req.content

url = 'http://localhost:5000/'
data = {'username':'zhengyh', 'password':'123456'}
# req = requests.post(url=url, data=json.dumps(data), timeout=5)
req = requests.post(url=url, json=data, timeout=5)
print req.status_code
print req.content
