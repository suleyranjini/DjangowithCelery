from django.shortcuts import render,HttpResponse,redirect
from django.views import View

from .models import Calculation

# Create your views here.
from .tasks import test_func,calculation_task


def test(request):
    test_func.delay()
    return HttpResponse("Done")

class CalculationView(View):
    def get(self,request):
        return render(request,"mainapp/calculate.html")

    def post(self, request):
        num1 = request.POST['n1']
        num2 = request.POST['n2']
        oper = request.POST['op']
        print(num1, num2,oper)
        calculation = Calculation.objects.create(
            oper = oper,
            input1 = int(num1),
            input2 = int(num2),
            status = 'PENDING',
        )

        calculation_task.delay(calculation.id)
        return redirect('list')
    
class ListView(View):
    def get(self,request):
        context = {'calculations':Calculation.objects.all()}
        return render(request,"mainapp/list.html",context)

    