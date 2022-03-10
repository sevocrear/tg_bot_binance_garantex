from telegram.ext import Updater,CommandHandler 
from telegram.ext import MessageHandler,Filters,InlineQueryHandler
import logging
import telegram
from config.telegram_bot.token import token

from include.garantex_api import garantex_API
from include.binance_api import binance_API

garantex_api = garantex_API()
binance_api = binance_API()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

bot = telegram.Bot(token=token)

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                     text="Hello , Thanks for choosing us!!")

    context.job_queue.run_repeating(callback_minute, interval=5, first=30,
                                    context=update.message.chat_id)

def callback_minute(context):
    chat_id=context.job.context

    text = f"GAR\tBIN\n{garantex_api.get_ticker_price(ticker_id='USDT_RUB', type_price = 'ask')}\t{binance_api.get_ticker_price(ticker_id='USDTRUB', type_price = 'askPrice')}"
    context.bot.send_message(chat_id=chat_id, 
                             text=text)

def main():
    updater = Updater(token,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start, pass_job_queue=True))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()