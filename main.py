import pymongo
import requests
from bs4 import BeautifulSoup
#import config

#client = pymongo.MongoClient(config.MONGO_URL)
#db = client.stocks
#
#db.notes.insert_one({
#    '_id': 'hello',
#    'value': 'world'
#})

s = requests.Session()
s.get('https://finance.naver.com/sise/field_submit.nhn?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn&fieldIds=quant&fieldIds=open_val&fieldIds=high_val&fieldIds=low_val')
res = s.get('https://finance.naver.com/sise/sise_market_sum.nhn')
bs = BeautifulSoup(res.text, 'html.parser')
for tr in bs.select('table.type_2 tr'):
    data = list(map(lambda td: td.text.strip(), tr.select('td')))
    if len(data) > 1:
        print(data)
