from .celery import app as celery_app

#This is to ensure app is always imported when Django starts so that shared_task will use this app.
#Celery is initialized whenever Django starts up
__all__ = ('celery_app')