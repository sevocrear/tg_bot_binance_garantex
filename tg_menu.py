from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import Updater
from config.telegram_bot.token import token

from include.garantex_api import garantex_API
from include.binance_api import binance_API
from include.comparator import compare_higher_cup, compare_lower_cup
import time
import threading 

garantex_api = garantex_API()
binance_api = binance_API()

############################### Bot ############################################
class bot_api():
    def __init__(self) -> None:
        self.updater = Updater(token, use_context=True)
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.main_menu, pattern='main'))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.usdt_rub_menu, pattern='m2_0'))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.usdt_rub_menu, pattern='m1_1'))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.main_menu, pattern='m1_2'))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.usdt_rub_menu, pattern='m2_1'))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.usdt_rub_menu, pattern='m2_2'))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.usdt_rub_menu, pattern='m2_3'))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.usdt_rub_menu, pattern='m2_4'))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.usdt_rub_menu, pattern='m2_5'))
        self.updater.start_polling()

        # GETTING INFO FROM STOCK MARKETS
        calculations_thread = threading.Thread(target = self.calculations)
        calculations_thread.start()
        calculations_thread.join()
    
    def calculations(self,):
        while True:
            # GARANTEX
            garantex_api.get_ticker_price(ticker_id="USDT_RUB") # both bid and ask
            print()
            # # BINANCE
            binance_api.get_ticker_price(asset = "USDT", fiat = "RUB", min_amount = 50000,  min_finish_rate = 93, logic_to_choose = "less", tradeType = "BUY", payType = 'Tinkoff', pages = 5)
            binance_api.get_ticker_price(asset = "USDT", fiat = "RUB", min_amount = 50000,  min_finish_rate = 93, logic_to_choose = "more", tradeType = "SELL", payType = 'Any', pages = 5)

            time.sleep(10)

    def start(self, update, context):
        update.message.reply_text(self.main_menu_message(),
                                reply_markup=self.main_menu_keyboard())


    def main_menu(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text=self.main_menu_message(),
            reply_markup=self.main_menu_keyboard())


    def usdt_rub_menu(self, update, context):
        try: 
            query = update.callback_query
            query.answer()
            query.edit_message_text(
            text=self.usdt_rub_menu_message(),
            reply_markup=self.usdt_rub_menu_keyboard())
        except BadRequest:
            pass
    ############################ Keyboards #########################################
    def main_menu_keyboard(self,):
        keyboard = [[InlineKeyboardButton('USDT-RUB', callback_data='m1_1')],
                    [InlineKeyboardButton('Чего-то не хватает?', callback_data='m1_2')],
                    ]
        return InlineKeyboardMarkup(keyboard)

    def usdt_rub_menu_keyboard(self, ):
        # # CALCULATIONS 
        lower_diff = compare_lower_cup(garantex_api.gar_costs['нижний'], binance_api.bin_costs['нижний']['price'])
        higher_diff = compare_higher_cup(garantex_api.gar_costs['верхний'], binance_api.bin_costs['нижний']['price'])

        keyboard = [
                    [InlineKeyboardButton(f"GAR: НИЗ {garantex_api.gar_costs['нижний']} | ВЕРХ {garantex_api.gar_costs['верхний']}", callback_data='m2_0')],
                    [InlineKeyboardButton(f'Спред[верх]: {higher_diff}', callback_data='m2_1')],
                    [InlineKeyboardButton(
                        f'Спред[низ]:  {lower_diff}', callback_data='m2_2')],
                    [InlineKeyboardButton(
                        f"Покупка: {binance_api.bin_costs['нижний']['price']}", callback_data='m2_3')],
                    [InlineKeyboardButton(
                        f"Владелец: {binance_api.bin_costs['нижний']['nickname']}", callback_data='m2_4')],
                    [InlineKeyboardButton(
                        text='link', url=binance_api.bin_costs['нижний']['link'])],
                    [InlineKeyboardButton('Назад', callback_data='main')]]
        return InlineKeyboardMarkup(keyboard)

    ############################# Messages #########################################


    def main_menu_message(self, ):
        return 'Давай посмотрим ценники:'


    def usdt_rub_menu_message(self, ):
        return 'USDT бинанс-гарантекс'

bot = bot_api()