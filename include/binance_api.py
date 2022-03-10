import requests
# https://github.com/binance/binance-connector-python

class binance_API():
    def __init__(self, binance_private_key = 'binance_private.key', binance_UID = 'binance_UID') -> None:

        self.host = 'api.binance.com' # для тестового сервера используйте stage.binance.biz


    def get_ticker_price(self, ticker_id = 'USDTRUB'):
        '''
        Функция, которая показывает текущий прайс тикера

        ticker_id - айди тикера (напр., 'USDTRUB', 'BTCRUB')
        type_price - ['bidPrice', 'askPrice', 'lastPrice']
        
        ask - верхний(продажа)
        bid - нижний (покупка)
        '''
        ret = requests.get('https://' + self.host + '/api/v3/ticker/24hr')

        response = ret.json()
        for ticker in response:
            if ticker['symbol'] == ticker_id:
                return {'верхний':round(float(ticker['askPrice']),2), 'нижний':round(float(ticker['bidPrice']),2)}