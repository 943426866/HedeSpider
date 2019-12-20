import requests

keyword = ''
taskid = '1'
userid = 'test'
data = {'keyword': keyword, 'taskid': taskid, 'userid': userid}

requests.get('http://localhost:5000/start_crawl?keyword=餐饮 饮食')
