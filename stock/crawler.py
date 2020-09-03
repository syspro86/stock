import os
import pymongo
import requests
from bs4 import BeautifulSoup
from datetime import datetime

client = None
db = None

def run():
    global client, db

    print('start cralwer')

    if db is None:
        mongo_url = None
        try:
            from stock import config
            mongo_url = config.MONGO_URL
        except:
            mongo_url = os.environ['MONGO_URL']

        client = pymongo.MongoClient(mongo_url)
        db = client.stocks

    today = datetime.now()
    today = f'{today.year}-{today.month:02}-{today.day:02}'

    s = requests.Session()
    s.get('https://finance.naver.com/sise/field_submit.nhn?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn&fieldIds=quant&fieldIds=open_val&fieldIds=high_val&fieldIds=low_val')
    res = s.get('https://finance.naver.com/sise/sise_market_sum.nhn')
    bs = BeautifulSoup(res.text, 'html.parser')
    for tr in bs.select('table.type_2 tr'):
        data = list(map(lambda td: td.text.strip(), tr.select('td')))
        if len(data) > 1:
            print(data)

            db.notes.insert_one({
                '_id': f'{today}_{data[1]}',
                'date': today,
                '종목명': data[1],
                '현재가': data[2],
                '전일비': data[3],
                '등락률': data[4],
                '액면가': data[5],
                '거래량': data[6],
                '시가': data[7],
                '고가': data[8],
                '저가': data[9],
            })
