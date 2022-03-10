from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from config.telegram_bot.token import token

from include.garantex_api import garantex_API
from include.binance_api import binance_API
import time

garantex_api = garantex_API()
binance_api = binance_API()

############################### Bot ############################################
class bot_api():
    def __init__(self) -> None:
        self.updater = Updater(token, use_context=True)
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.main_menu, pattern='main'))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.usdt_rub_menu, pattern='m1_1'))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.main_menu, pattern='m1_2'))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.usdt_rub_menu, pattern='m2_1'))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.usdt_rub_menu, pattern='m2_2'))
        self.updater.start_polling()

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
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text=self.usdt_rub_menu_message(),
            reply_markup=self.usdt_rub_menu_keyboard())


    ############################ Keyboards #########################################
    def main_menu_keyboard(self,):
        keyboard = [[InlineKeyboardButton('USDT-RUB', callback_data='m1_1')],
                    [InlineKeyboardButton('Чего-то не хватает?', callback_data='m1_2')],
                    ]
        return InlineKeyboardMarkup(keyboard)


    def usdt_rub_menu_keyboard(self, ):
        # st = time.time()
        text_gar_ask = garantex_api.get_ticker_price(
            ticker_id='USDT_RUB', type_price='ask')
        text_gar_bid = garantex_api.get_ticker_price(
            ticker_id='USDT_RUB', type_price='bid')
        text_bin_ask = binance_api.get_ticker_price(
            ticker_id='USDTRUB', type_price='askPrice')
        text_bin_bid = binance_api.get_ticker_price(
            ticker_id='USDTRUB', type_price='bidPrice')
        # print((time.time()-st)/1000)
        keyboard = [[InlineKeyboardButton(f'Binance : {text_bin_ask} | {text_bin_bid}', callback_data='m2_1')],
                    [InlineKeyboardButton(
                        f'Garantex : {text_gar_ask} | {text_gar_bid}', callback_data='m2_2')],
                    [InlineKeyboardButton('Назад', callback_data='main')]]
        return InlineKeyboardMarkup(keyboard)

    ############################# Messages #########################################


    def main_menu_message(self, ):
        return 'Давай посмотрим ценники:'


    def usdt_rub_menu_message(self, ):
        return 'Курсы USDT-RUB: ASK | BID'

bot = bot_api()