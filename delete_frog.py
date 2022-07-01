from glob import glob
import logging
import os

#Remove pic to old_frogs

def delete_frog():
    try:
        frog_pic_list = glob('/home/weinder/projects/wednesday_bot/planned_frogs/*.jp*g')
        frog_pic_name = frog_pic_list[0]
        os.replace(frog_pic_name, os.path.join('/home/weinder/projects/wednesday_bot/old_frogs/', frog_pic_name[-7:]))
    except IndexError:
        logging.info("Have no frogs")

if __name__ == "__main__":
    delete_frog()