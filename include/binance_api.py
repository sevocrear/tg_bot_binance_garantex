import requests


class binance_API():
    def __init__(self, binance_private_key = 'binance_private.key', binance_UID = 'binance_UID') -> None:

        self.host = 'api.binance.com' # для тестового сервера используйте stage.binance.biz


    def get_ticker_price(self, ticker_id = 'USDTRUB', type_price='ask'):
        '''
        Функция, которая показывает текущий прайс тикера

        ticker_id - айди тикера (напр., 'USDTRUB', 'BTCRUB')
        type_price - ['bidPrice', 'askPrice', 'lastPrice']
        '''
        ret = requests.get('https://' + self.host + '/api/v3/ticker/24hr')

        response = ret.json()
        for ticker in response:
            if ticker['symbol'] == ticker_id:
                return round(float(ticker[type_price]),2)