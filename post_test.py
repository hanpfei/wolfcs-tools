import json
import requests

# url = 'http://localhost:18312/api/v1/log.do'
url = 'http://localhost:18312/mob/api/v1/log'
# d = {'data': 'ddd', 'meta': 'adagsfgdh', 'product' : 'ykt'}
s = {'data': 'ddd', 'meta': 'adagsfgdh', 'product' : 'ykt'}

print(s)
r = requests.post(url, json=s)
print(r.text)