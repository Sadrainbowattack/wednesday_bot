import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import greet_user
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

def main():
    mybot=Updater(settings.API_KEY,use_context=True)
    dp=mybot.dispatcher
    dp.add_handler(CommandHandler('start',greet_user))
    logging.info("Bot started")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()