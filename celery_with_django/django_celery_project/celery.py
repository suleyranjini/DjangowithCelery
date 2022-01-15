from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings

from celery.schedules import crontab

#Set default Django settings for celery program
os.environ.setdefault('DJANGO_SETTINGS_MODULE','django_celery_project.settings')

#Initializing Celery instance
app = Celery('django_celery_project')

app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')

#Load any configurations variables that need to be set for Celery will be done via Settings.py. Pass as string to avoid serialization
#namespace CELERY means in settings.py, all CELERY related config keys should start with CELERY_
app.config_from_object('django.conf:settings',namespace = 'CELERY')

#Celery Beat settings
app.conf.beat_schedule = {
    'insert-fruits':{
        'task':'mainapp.tasks.fruit_task',
        'schedule': crontab(hour = 22, minute = 52)
        
    }
}

#THis is to load task modules from all registered Django app configs
app.autodiscover_tasks()

#We r telling celery to register and remember, this prints the request that came to the task in order to debug celery
@app.task(bind = True)
def debug_task(self):
    print(f'Request : {self.request!r}')