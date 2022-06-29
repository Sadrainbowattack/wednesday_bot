import os
import requests
from bs4 import BeautifulSoup
import urllib.request
from telegram import ReplyKeyboardMarkup
from glob import glob
import logging

def main_keyboard():
    return ReplyKeyboardMarkup([['Random frog', 'Save my frog'], ['Subscribe', 'Unsubscribe']], True, True)

#Get pics from reddit

def get_html():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
    }
    url = "https://www.reddit.com/r/wednesdaymemes/new/"
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return False

def get_pic_url():        
    html = get_html()
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
    filepath = os.path.join('planned_frogs/', f'{filename}.jpg')
    urllib.request.urlretrieve(stack, filepath)
    print('saved')

def delete_frog():
    try:
        frog_pic_list = glob('planned_frogs/*.jp*g')
        frog_pic_name = frog_pic_list[0]
        os.replace(frog_pic_name, os.path.join('old_frogs', frog_pic_name[-7:]))
    except IndexError:
        logging.info("Have no frogs")