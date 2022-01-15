
from django.urls import path
from .views import CalculationView, test,ListView

urlpatterns = [
    
    path('test/',test,name='test'),
    path('list',ListView.as_view(),name='list'),
    path('calculate',CalculationView.as_view(),name='calculate'),
]