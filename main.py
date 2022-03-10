from include.garantex_api import garantex_API
from include.binance_api import binance_API
from include.comparator import compare_higher_cup, compare_lower_cup
import time 
garantex_api = garantex_API()
binance_api = binance_API()
print('GAR\tBIN')
while True:
      bin_costs = binance_api.get_ticker_price(ticker_id="USDTRUB")
      gar_costs = garantex_api.get_ticker_price(ticker_id="USDT_RUB")
      print(binance_api.get_ticker_price(ticker_id="USDTRUB"))
      print(garantex_api.get_ticker_price(ticker_id="USDT_RUB"))
      print(f"lower diff:{compare_lower_cup()}")
      time.sleep(5)