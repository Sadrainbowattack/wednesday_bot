from celery import Celery
from celery.schedules import crontab

from jobs import delete_frog
from utils import save_pic_red

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def pic_red():
    save_pic_red()

@celery_app.task
def delete_pic():
    delete_frog()

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='0', hour='15', day_of_week='2'), delete_pic.s())
    sender.add_periodic_task(crontab(minute='0', hour='12', day_of_week='3'), pic_red.s())