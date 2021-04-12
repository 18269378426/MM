# 停止爬虫
import requests
url = 'http://localhost:6800/cancel.json'
data = {
    'project': "MM",
    'job': "MM",
}
resp = requests.post(url, data=data)