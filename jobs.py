from glob import glob
from utils import main_keyboard
import os
import logging
from telegram.error import BadRequest
from db import db, get_subscription
import requests
from bs4 import BeautifulSoup
import urllib.request

def repeating_frog_pic(context):
    frog_pic_list = glob('planned_frogs/*.jp*g')
    frog_pic_name = frog_pic_list[0]
    for user in get_subscription(db):
        try:
            context.bot.send_photo(chat_id=user['chat_id'], photo=open(frog_pic_name, 'rb'), reply_markup=main_keyboard())
        except OSError:
            print('Have no frogs')
            logging.info("Have no frogs")
        except BadRequest:
            logging.info(f"Chat {user['chat_id']} not found")

def delete_frog(context):
    frog_pic_list = glob('planned_frogs/*.jp*g')
    frog_pic_name = frog_pic_list[0]
    os.remove(frog_pic_name)

url = "https://www.reddit.com/r/wednesdaymemes/new/"

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
    }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return False

def get_pic_url():        
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    all_img = soup.find_all('img', class_="_2_tDEnGMLxpM6uOa2kaDB3 ImageBox-image media-element _1XWObl-3b9tPy64oaG6fax")
    for one in all_img:
        try:
            first = str(one).split(' ')[7]
            second = first[4:].replace('"', ' ')
            final = second.replace('amp;', '')
            return final
        except(AttributeError, ValueError, TypeError):
            return False

def save_pic_red():
    stack = get_pic_url()
    filename = stack[-10:-5]
    filepath = os.path.join('planned_frogs', f'{filename}.jpg')
    urllib.request.urlretrieve(stack, filepath)
