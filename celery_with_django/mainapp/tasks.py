from celery import shared_task
from .models import Calculation, Fruit
from django_celery_project.celery import app

from celery.schedules import crontab

@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        print(i)
    return "Done"


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

@app.task(bind=True)
def fruit_task(self):
    fruit_dict = {'apple':'red','banana':'yellow','kiwi':'green'}

    for key,value in fruit_dict.items():
        fruits = Fruit.objects.create(name=key,colour=value)
        fruits.save()
    return "Fruits Saved"

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Call at 12:05pm.
    sender.add_periodic_task(
        crontab(hour = 12, minute = 7),
        fruit_task
    )
