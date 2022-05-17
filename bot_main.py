import logging
import settings
from datetime import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import greet_user, send_random_frog, check_user_photo, save_frog_plan, subscribe, unsubscribe
from jobs import repeating_frog_pic
import pytz

logging.basicConfig(filename='bot.log', level=logging.INFO)

def main():
    mybot=Updater(settings.API_KEY,use_context=True)
    dp=mybot.dispatcher

    def save_frog(update, context):
        update.message.reply_text('Give me frog pic')
        dp.add_handler(MessageHandler(Filters.photo, check_user_photo))
    
    def save_wednesday_frog(update, context):
        update.message.reply_text('Give me frog pic')
        dp.add_handler(MessageHandler(Filters.photo, save_frog_plan))

    jq = mybot.job_queue
    target_time = time(12, 00, tzinfo=pytz.timezone('Europe/Moscow'))
    target_day = [2]
    jq.run_daily(repeating_frog_pic, target_time, target_day)

    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Random frog)$'), send_random_frog))
    dp.add_handler(CommandHandler('random_frog', send_random_frog))
    dp.add_handler(MessageHandler(Filters.regex('^(Save my frog)$'), save_frog))
    dp.add_handler(CommandHandler('save_frog', save_frog))
    dp.add_handler(CommandHandler('plan_frog', save_wednesday_frog))
    dp.add_handler(MessageHandler(Filters.regex('^(Subscribe)$'), subscribe))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(MessageHandler(Filters.regex('^(Unsubscribe)$'), unsubscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    logging.info("Bot started")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()