import logging
import settings
from datetime import time
from telegram.bot import Bot
from telegram.ext import messagequeue as mq
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.utils.request import Request
import pytz

from handlers import greet_user, send_random_frog, check_user_photo, save_frog_plan, subscribe, unsubscribe
from jobs import repeating_frog_pic


logging.basicConfig(filename='bot.log', level=logging.INFO)

class MQBot(Bot):
    def __init__(self, *args, is_queued_def=True, msg_queue=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = msg_queue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_photo(self, *args, **kwargs):
        return super().send_photo(*args, **kwargs)

def main():
    request = Request(con_pool_size=8)
    bot = MQBot(settings.API_KEY, request=request)
    mybot=Updater(bot=bot,use_context=True)

    dp = mybot.dispatcher

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