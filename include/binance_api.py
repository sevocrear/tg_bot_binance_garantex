import requests
# https://github.com/binance/binance-connector-python
import json
import threading 

class binance_API():
    def __init__(self, ) -> None:

        self.headers = {
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

    def get_ticker_price(self, asset = "USDT", fiat = "RUB", min_amount = 50000,  min_finish_rate = 93, logic_to_choose = "more", tradeType = "SELL", payType = 'Tinkoff', pages = 1):
        advertisements = []
        def request_page(page):
            # REQUEST
            data = {
            "asset": asset,
            "fiat": fiat,
            "merchantCheck": False,
            "page": page,
            "payTypes": [],
            "publisherType": None,
            "rows": 10,
            "tradeType": tradeType
            }

            r = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', headers=self.headers, json=data)
            d = json.loads(r.text)
            for id in range(len(d['data'])):
                d['data'][id]['page'] = page
            advertisements.extend(d['data'])
        threads = [] 
        for page in range(1,pages+1):
            threads.append(                                                         
            threading.Thread(target=request_page, args=(page,)))         
            threads[-1].start() # start the thread we just created            
        # wait for all threads to finish                                            
        for t in threads:                                                           
            t.join()      
        # min and max init values for finding optimal advertisement
        min_price = 1_000_000_000_000
        max_price = 0

        idx = 0 # iterating index
        advert_id = None # index of desired advertisement
        for advertisement in advertisements: 
            monthFinishRate = advertisement['advertiser']['monthFinishRate']*100
            minSingleTransAmount = float(advertisement['adv']['minSingleTransAmount'])
            price = float(advertisement['adv']['price'])
            payTypes = list(map(lambda x: x['payType'], advertisement['adv']['tradeMethods']))

            # Our condition to choose
            if minSingleTransAmount >= min_amount and monthFinishRate >= min_finish_rate and payType in payTypes:
                if logic_to_choose == "less":
                    if min_price > price:
                        advert_id = idx
                        min_price = price
                else:
                    if max_price < price:
                        advert_id = idx
                        max_price = price
            idx += 1
        # Finalize!
        if advert_id != None:
            adv = advertisements[advert_id]
            nickname = adv['advertiser']['nickName']
            price = float(adv['adv']['price'])
            page = adv['page']
            link = f"https://p2p.binance.com/en/advertiserDetail?advertiserNo={adv['advertiser']['userNo']}"
            return price, nickname, link,  page
        else:
            return -1, None, None, None
