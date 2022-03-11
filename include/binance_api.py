import requests
# https://github.com/binance/binance-connector-python
import json
import threading 
import numpy as np
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

        # TODO: Currently API supports only one pair (coin-fiat)
        
        # BINANCE P2P COSTS 
        nickname = "None"
        price = -1
        link = "https://www.binance.com/ru/404"
        page = 0
        self.bin_costs = {}
        self.bin_costs['верхний']={'price':price, 'link':link, 'nickname': nickname, 'page':page}
        self.bin_costs['нижний']={'price':price, 'link':link, 'nickname': nickname, 'page':page}

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

        idx = 0 # iterating index
        advert_id = None # index of desired advertisement
        advert_indexes = []
        for idx, advertisement in enumerate(advertisements): 
            monthFinishRate = advertisement['advertiser']['monthFinishRate']*100
            minSingleTransAmount = float(advertisement['adv']['minSingleTransAmount'])
            maxSingleTransAmount = float(advertisement['adv']['dynamicMaxSingleTransAmount'])
            price = float(advertisement['adv']['price'])
            payTypes = list(map(lambda x: x['payType'], advertisement['adv']['tradeMethods']))+["Any"]

            # Our condition to choose
            if (min_amount >= minSingleTransAmount and min_amount <= maxSingleTransAmount) and monthFinishRate >= min_finish_rate and payType in payTypes:
                advert_indexes.append([idx, price])
                
        if len(advert_indexes) > 0:
            adv_array = np.array(advert_indexes)
            if logic_to_choose == "less":
                advert_id = np.argmin(adv_array[:,1])
                advert_id = int(adv_array[advert_id][0])

            else:
                advert_id = np.argmax(adv_array[:,1])
                advert_id = int(adv_array[advert_id][0])


        nickname = "None"
        price = -1
        link = "https://www.binance.com/ru/404"
        page = 0
        # Finalize!
        if advert_id != None:
            adv = advertisements[advert_id]
            nickname = adv['advertiser']['nickName']
            price = float(adv['adv']['price'])
            page = adv['page']
            link = f"https://p2p.binance.com/en/advertiserDetail?advertiserNo={adv['advertiser']['userNo']}"

        if tradeType == "SELL":
            self.bin_costs['верхний']={'price':price, 'link':link, 'nickname': nickname, 'page':page}
        else:
            self.bin_costs['нижний']={'price':price, 'link':link, 'nickname': nickname, 'page':page}
