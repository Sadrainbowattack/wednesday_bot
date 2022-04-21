import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import greet_user, send_random_frog, check_user_photo


logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot=Updater(settings.API_KEY,use_context=True)
    dp=mybot.dispatcher

    def save_frog(update, context):
        update.message.reply_text('Give me frog pic')
        dp.add_handler(MessageHandler(Filters.photo, check_user_photo))

    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Random frog)$'), send_random_frog))
    dp.add_handler(CommandHandler('random_frog', send_random_frog))
    dp.add_handler(MessageHandler(Filters.regex('^(Save my frog)$'), save_frog))
    dp.add_handler(CommandHandler('save_frog', save_frog))
    logging.info("Bot started")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()