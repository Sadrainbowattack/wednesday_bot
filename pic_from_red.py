import requests
from bs4 import BeautifulSoup
import urllib.request
import os

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
    filepath = os.path.join('/home/weinder/projects/wednesday_bot/planned_frogs/', f'{filename}.jpg')
    urllib.request.urlretrieve(stack, filepath)

if __name__ == "__main__":
    save_pic_red()