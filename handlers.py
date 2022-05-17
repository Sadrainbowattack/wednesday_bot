from glob import glob
import os
from random import choice

from db import db, get_or_create_user, subscribe_user, unsubscribe_user
from utils import main_keyboard

def greet_user(update,context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    print('Вызван /start')
    update.message.reply_text(
        f"Здарова, бандиты!", reply_markup=main_keyboard())

def send_random_frog(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    frog_pic_list = glob('old_frogs/*.jp*g')
    frog_pic_name = choice(frog_pic_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(frog_pic_name, 'rb'), reply_markup=main_keyboard())

def check_user_photo(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text("Loading")
    os.makedirs('old_frogs', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('old_frogs', f'{photo_file.file_id}.jpg')
    photo_file.download(filename)
    update.message.reply_text("Frog saved")

def save_frog_plan(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    os.makedirs('planned_frogs', exist_ok=True)
    os.makedirs('old_frogs', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('planned_frogs', f'{photo_file.file_id}.jpg')
    filename2 = os.path.join('old_frogs', f'{photo_file.file_id}.jpg')
    photo_file.download(filename)
    photo_file.download(filename2)
    update.message.reply_text("Frog saved for Wednesday")

def subscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    subscribe_user(db, user)
    update.message.reply_text("Subscription complete", reply_markup=main_keyboard())

def unsubscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    unsubscribe_user(db, user)
    update.message.reply_text("Unsubscription complete", reply_markup=main_keyboard())

