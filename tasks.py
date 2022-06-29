from celery import Celery
from celery.schedules import crontab

from utils import save_pic_red, delete_frog

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def pic_red():
    save_pic_red()

@celery_app.task
def delete_pic():
    delete_frog()

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour='16',day_of_week='3'), delete_pic.s())
    sender.add_periodic_task(crontab(hour='14',day_of_week='4'), pic_red.s())