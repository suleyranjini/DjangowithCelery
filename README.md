# DjangowithCelery
1. Create a folder celery_with_django

2. Open terminal on this location and run
$pipenv shell to create a VE

3. Install django
$pipenv install django

4. Create django project
$django-admin startproject django_celery_project

5. Rename the outside project folder to celery_with_django and go inside this folder

6. Install Celery
$pipenv install celery

7. Create Django app
$django-admin startapp mainapp

8. Install Redis server from https://github.com/tporadowski/redis/releases, download .msi file and install

9. From C:\Program Files\Redis, run redis-cli.exe to start Redis server
type ping and you will get the response PONG which means server is running


10. To use Django Rest Api, first install it
$pipenv install djangorestframework
$pipenv install markdown
$pipenv install django-filter

10. In settings.py of Django project, put in the following

#CELERY_SETTINGS

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'#6379 is default port for Redis server
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_RESULT_BACKEND = 'django-db'

Register the following under INSTALLED_APPS section
'mainapp',
'django_celery_results',
'rest_framework'

11. Under django_celery_project folder create a file celery.py and put in following code

from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings

from celery.schedules import crontab

#Set default Django settings for celery program
os.environ.setdefault('DJANGO_SETTINGS_MODULE','django_celery_project.settings')

#Initializing Celery instance
app = Celery('django_celery_project')

#To update default timezone set by celery
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')

#Load any configurations variables that need to be set for Celery will be done via Settings.py. Pass as string to avoid serialization
#namespace CELERY means in settings.py, all CELERY related config keys should start with CELERY_
app.config_from_object('django.conf:settings',namespace = 'CELERY')

#THis is to load task modules from all registered Django app configs
app.autodiscover_tasks()

#We r telling celery to register and remember, this prints the request that came to the task in order to debug celery
@app.task(bind = True)
def debug_task(self):
    print(f'Request : {self.request!r}')


12. In models.py, give the following

from django.db import models


class Calculation(models.Model):
       
    oper = models.CharField(max_length=5)
    input1 = models.IntegerField()
    input2 = models.IntegerField()
    output = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=8,null=True)
    message = models.CharField(max_length=110, blank=True)

    def __str__(self):
        return self.message
    
    class Meta:
        db_table = "Calculation"


class Fruit(models.Model):
    name = models.CharField(max_length = 100)
    colour = models.CharField(max_length = 100)

    class Meta:
        db_table = "Fruit"

    def __str__(self):
        return self.name +" - "+ self.colour



13. Run makemigrations and migrate

14. Inside mainapp Django App folder, create a file tasks.py

from celery import shared_task
from .models import Calculation, Fruit
from django_celery_project.celery import app

from celery.schedules import crontab

def calc(num1, num2, oper):
    print("Inside Function******")
    if oper == "SUM":
        result = num1 + num2
    elif oper == "DIFF":
        result = num1 - num2
    elif  oper == "MULT":
        result = num1 * num2
    elif oper == "DIV" and num2 != 0:
        result = num1 / num2
    else:
        result = 0           
    final_result = float(result)
    
    return final_result

@app.task(bind=True)
def calculation_task(self,calculation_id):
    calculation = Calculation.objects.get(id=calculation_id)
    
    num1 = calculation.input1
    num2 = calculation.input2
    oper = calculation.oper
    print(num1,num2,oper)
    
    try:
        calculation.output = calc(num1,num2,oper)
       
        calculation.status = 'SUCCESS'
    except Exception as e:
        calculation.status = 'ERROR'
        calculation.message = str(e)
    
    calculation.save()

15. Inside mainapp create a file called serializers.py and give the following

from rest_framework import serializers
from .models import Calculation

class calculateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Calculation
        fields = '__all__'

16. Inside Views.py under mainapp, give the following
from django.shortcuts import render,HttpResponse,redirect
from django.views import View

from rest_framework.decorators import api_view
from rest_framework import status,viewsets,permissions
from rest_framework.response import Response

from mainapp.serializers import calculateSerializer

from .models import Calculation

# Create your views here.
from .tasks import calculation_task

@api_view(['GET'])#can give list of requests as well
def list_view(request):

    try:
        # calculaterecord = Calculation.objects.get(pk=id)
        calculaterecord = Calculation.objects.all()
        print(calculaterecord)
    except calculaterecord.DoesNOTExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = calculateSerializer(calculaterecord,many=True)
        return Response(serializer.data)#sends this response to html with JSON data(converted from QuerySet)

@api_view(['POST'])
def calculate_view(request):
    if request.method == 'POST':
        # print(request.POST['input1'])
        serializer = calculateSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            print(serializer.data['id'])
            calculation_task.delay(serializer.data['id'])
            return Response(serializer.data, status = status.HTTP_201_CREATED)#For POST success this is the HTTP code
        return Response(serializer.error, status = status.HTTP_404_NOT_FOUND)#or any other appropriate reponse code

17. In django_celery_project folder, inside urls.py, give the following

from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mainapp/',include('mainapp.urls')),
    
]

18. Inside mainapp folder, create a file urls.py and give the following

from django.urls import path
# from .views import CalculationView, test,ListView,list_view,calculate_view
from .views import list_view,calculate_view

# from .views import calculatemodelViewset

urlpatterns = [
    
    # path('test/',test,name='test'),
    # path('list/<int:id>',list_view,name='list'),
    path('list/',list_view,name='list'),
    path('calculate',calculate_view,name='calculate'),
]

To run the application do the following:
----------------------------------------

1. Start Django server
$python manage.py runserver

2. To run celery worker
celery -A django_celery_project.celery worker --pool=solo -l info

In Postman, configure a GET request with the following URL
http://127.0.0.1:8000/mainapp/list

Result - All the data from Calculation Table in database

To insert data into the table using POST, configure a POST request with following URL and JSON format
http://127.0.0.1:8000/mainapp/calculate
{
    "input1":6,
    "input2":6,
    "oper":"DIFF",
    "status":"PENDING"
}

To run periodic tasks or schedule tasks in Celery
-------------------------------------------------
1. In Django terminal install celery  beat
$pipenv install django-celery-beat

2. In settings.py, register celery beat under INSTALLED_APPS
'django_celery_beat'

3. Run makemigrations and migrate

4. Create task in tasks.py for running on scheduler
@app.task(bind=True)
def fruit_task(self):
    fruit_dict = {'apple':'red','banana':'yellow','kiwi':'green'}

    for key,value in fruit_dict.items():
        fruits = Fruit.objects.create(name=key,colour=value)
        fruits.save()
    return "Fruits Saved"

4. In celery.py can do the following

from celery.schedules import crontab

#Celery Beat settings
app.conf.beat_schedule = {
	 'insert-fruits':{
         'task':'mainapp.tasks.fruit_task',
         'schedule': crontab(hour = 22, minute = 52)
        
     }
 }

---
OR
---

Inside tasks.py, put the following

from celery.schedules import crontab

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Call at 12:07pm.
    sender.add_periodic_task(
        crontab(hour = 12, minute = 7),
        fruit_task
    )

5. Start another terminal for running celery beat
$celery -A django_celery_project beat -l info

