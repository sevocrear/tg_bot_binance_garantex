from include.garantex_api import garantex_API
from include.binance_api import binance_API
import time 
garantex_api = garantex_API()
binance_api = binance_API()
print('GAR\tBIN')
while True:
      print(binance_api.get_ticker_price(ticker_id="USDTRUB", type_price = 'askPrice'))
      time.sleep(5)