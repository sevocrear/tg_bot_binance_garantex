from include.garantex_api import garantex_API
from include.binance_api import binance_API
from include.comparator import compare_higher_cup, compare_lower_cup
import time 
garantex_api = garantex_API()
binance_api = binance_API()
price, nickname, link, page = binance_api.get_ticker_price(asset = "USDT", fiat = "RUB", min_amount = 50000,  min_finish_rate = 93, logic_to_choose = "less", tradeType = "BUY", payType = 'Tinkoff', pages = 5)

print(price, nickname, link, page)
# while True:
#       bin_costs = binance_api.get_ticker_price(ticker_id="USDTRUB")
#       gar_costs = garantex_api.get_ticker_price(ticker_id="USDT_RUB")
#       print(bin_costs)
#       print(gar_costs)
#       print(f"lower diff:{compare_lower_cup(gar_costs['нижний'], bin_costs['нижний'])} %")
#       print(f"higher diff:{compare_higher_cup(gar_costs['верхний'], bin_costs['верхний'])} %")
#       time.sleep(5)