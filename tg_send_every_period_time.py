from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest, Unauthorized, TimedOut
from telegram.ext import Updater
from config.telegram_bot.token import token

from include.garantex_api import garantex_API
from include.binance_api import binance_API
from include.comparator import compare_higher_cup, compare_lower_cup
import time
import threading 
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

garantex_api = garantex_API()
binance_api = binance_API()

# NEWS
def news():
    while True:
        callback_for_users(bot)
        time.sleep(30)
############################### Bot ############################################
class bot_api():
    def __init__(self) -> None:
        self.updater = Updater(token, use_context=True)
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))

        self.updater.start_polling()
        # data = np.asarray([])
        # np.save('config/telegram_bot/users_id.npy', data)
        self.users_id = np.load('config/telegram_bot/users_id.npy')
        print(self.users_id, type(self.users_id))

        # self.updater.idle()
        self.error_flag = 0
        self.error = ""
    def calculations(self,):
        while True:
            try:
                # GARANTEX
                garantex_api.get_ticker_price(ticker_id="USDT_RUB") # both bid and ask
                # # BINANCE
                binance_api.get_ticker_price(asset = "USDT", fiat = "RUB", min_amount = 50000,  min_finish_rate = 93, logic_to_choose = "less", tradeType = "BUY", payType = 'Tinkoff', pages = 20)
                binance_api.get_ticker_price(asset = "USDT", fiat = "RUB", min_amount = 50000,  min_finish_rate = 93, logic_to_choose = "more", tradeType = "SELL", payType = 'Tinkoff', pages = 20)
                time.sleep(5)
                self.error_flag = 0
            except Exception as e: 
                self.error = e
                self.error_flag = 1
                pass

    def start(self, update, context):
        chat_id = update.message.chat_id
        if chat_id not in self.users_id:
            self.users_id = np.append(chat_id, self.users_id)
        np.save('config/telegram_bot/users_id.npy', self.users_id)
        context.bot.send_message(chat_id=chat_id, text="Давай посмотрим ценники.")
        context.bot.send_message(chat_id=chat_id, text="Подписали Вас на обновления...")



def callback_for_users(bot):
    # # CALCULATIONS
    lower_diff = compare_lower_cup(garantex_api.gar_costs['нижний'], binance_api.bin_costs['нижний']['price'])
    higher_diff = compare_higher_cup(garantex_api.gar_costs['верхний'], binance_api.bin_costs['нижний']['price'])
    # if lower_diff != None and higher_diff != None:
    processes = []

    # error message
    error =""
    if bot.error_flag:
        error = "Ошибка:" + str(bot.error)
    # time

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    text_to_send = f"""GAR: НИЗ {garantex_api.gar_costs['нижний']} | ВЕРХ {garantex_api.gar_costs['верхний']}\nСпред[верх]: {higher_diff}\nСпред[низ]:  {lower_diff}\nПокупка: {binance_api.bin_costs['нижний']['price']}\nВладелец: {binance_api.bin_costs['нижний']['nickname']}\n{error}\nВремя: {current_time}"""
    with ThreadPoolExecutor(max_workers=10) as executor:
        for chat_id in bot.users_id:
    ############################# Messages #########################################
            try:
                processes.append(executor.submit(bot.updater.bot.send_message(chat_id=chat_id, 
                            text=text_to_send, timeout = 15)))
            except Unauthorized: 
            # for task in as_completed(processes):
              user_blocked_by_id = np.where(bot.users_id == chat_id)[0][0]
              bot.users_id = np.delete(bot.users_id, user_blocked_by_id)
              np.save('config/telegram_bot/users_id.npy', bot.users_id)
            except TimedOut:
                pass

bot = bot_api()

# GETTING INFO FROM STOCK MARKETS
calculations_thread = threading.Thread(target = bot.calculations)
calculations_thread.start()

# NEWS
news_thread = threading.Thread(target = news)
news_thread.start()

news_thread.join()
calculations_thread.join()

print("NEWS")
