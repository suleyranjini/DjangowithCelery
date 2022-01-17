from django.shortcuts import render,HttpResponse,redirect
from django.views import View

from rest_framework.decorators import api_view
from rest_framework import status,viewsets,permissions
from rest_framework.response import Response

from mainapp.serializers import calculateSerializer

from .models import Calculation

# Create your views here.
from .tasks import test_func,calculation_task


def test(request):
    test_func.delay()
    return HttpResponse("Done")

# class CalculationView(View):
#     def get(self,request):
#         return render(request,"mainapp/calculate.html")

#     def post(self, request):
#         num1 = request.POST['n1']
#         num2 = request.POST['n2']
#         oper = request.POST['op']
#         print(num1, num2,oper)
#         calculation = Calculation.objects.create(
#             oper = oper,
#             input1 = int(num1),
#             input2 = int(num2),
#             status = 'PENDING',
#         )

#         calculation_task.delay(calculation.id)
#         return redirect('list')
    
# class ListView(View):
#     def get(self,request):
#         context = {'calculations':Calculation.objects.all()}
#         return render(request,"mainapp/list.html",context)



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

@api_view(['GET'])
def detail_view(request,id):
    if request.method == 'GET':
        try:
            calculationrecord = Calculation.objects.get(pk=id)
            print(calculationrecord)
            serializer = calculateSerializer(calculationrecord)
            return Response(serializer.data)
        except calculationrecord.DoesNOTExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
    
        