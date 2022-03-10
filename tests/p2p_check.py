import requests

tradeType = "SELL"
data = {
  "asset": "USDT",
  "fiat": "RUB",
  "merchantCheck": False,
  "page": 2,
  "payTypes": [],
  "publisherType": None,
  "rows": 10,
  "tradeType": tradeType
}

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "123",
    "content-type": "application/json",
    "Host": "p2p.binance.com",
    "Origin": "https://p2p.binance.com",
    "Pragma": "no-cache",
    "TE": "Trailers",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
}

r = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', headers=headers, json=data)
import json
d = json.loads(r.text)
data = d['data']
for advertisement in data: 
    nickname = advertisement['advertiser']['nickName']
    monthFinishRate = advertisement['advertiser']['monthFinishRate']*100
    minSingleTransAmount = advertisement['adv']['minSingleTransAmount']
    maxSingleTransAmount = advertisement['adv']['maxSingleTransAmount']
    price = advertisement['adv']['price']
    payTypes = list(map(lambda x: x['payType'], advertisement['adv']['tradeMethods']))

    print(nickname)
    print(monthFinishRate)
    print(minSingleTransAmount)
    print(maxSingleTransAmount)
    print(price)
    print(payTypes)
    print("####")
