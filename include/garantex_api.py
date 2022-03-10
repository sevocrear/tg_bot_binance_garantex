
# https://garantexio.github.io/?python#overview
import requests
import jwt

class garantex_API():
    def __init__(self, garantex_private_key = 'garantex_private.key', garantex_UID = 'garantex_UID') -> None:

        self.host = 'garantex.io' # для тестового сервера используйте stage.garantex.biz


    def get_ticker_price(self, ticker_id = 'USDT_RUB', type_price='ask'):
        '''
        Функция, которая показывает текущий прайс тикера

        ticker_id - айди тикера (напр., 'USDT_RUB', 'BTC_RUB')
        type_price - ['bid', 'ask', 'last]
        '''
        ret = requests.get('https://' + self.host + '/api/v2/coingecko/tickers')

        response = ret.json()
        for ticker in response:
            if ticker['ticker_id'] == ticker_id:
                return round(float(ticker[type_price]),2)