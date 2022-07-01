from glob import glob
import logging
from telegram.error import BadRequest
from db import db, get_subscription


def repeating_frog_pic(context):
    frog_pic_list = glob('planned_frogs/*.jp*g')
    frog_pic_name = frog_pic_list[0]
    for user in get_subscription(db):
        try:
            context.bot.send_photo(chat_id=user['chat_id'], photo=open(frog_pic_name, 'rb'))
        except OSError:
            logging.info("Have no frogs")
        except BadRequest:
            logging.info(f"Chat {user['chat_id']} not found")
