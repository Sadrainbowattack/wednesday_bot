from glob import glob
import os

from random import choice
from telegram.ext import MessageHandler, Filters
from utils import main_keyboard

def greet_user(update,context):
    print('Вызван /start')
    update.message.reply_text(
        f"Здарова, бандиты!", reply_markup=main_keyboard())

def send_random_frog(update, context):
    frog_pic_list = glob('old_frogs/*.jp*g')
    frog_pic_name = choice(frog_pic_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(frog_pic_name, 'rb'), reply_markup=main_keyboard())

def check_user_photo(update, context):
    update.message.reply_text("Loading")
    os.makedirs('old_frogs', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('old_frogs', f'{photo_file.file_id}.jpg')
    photo_file.download(filename)
    update.message.reply_text("Frog saved")

