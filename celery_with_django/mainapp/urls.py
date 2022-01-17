
from django.urls import path
# from .views import CalculationView, test,ListView,list_view,calculate_view
from .views import test,list_view,calculate_view,detail_view

# from .views import calculatemodelViewset

urlpatterns = [
    
    path('test/',test,name='test'),
    # path('list/<int:id>',list_view,name='list'),
    path('list/',list_view,name='list'),
    path('calculate/',calculate_view,name='calculate'),
    path('detail/<int:id>',detail_view,name='detail'),
]


# urlpatterns = [
    
#     path('test/',test,name='test'),
#     path('list',ListView.as_view(),name='list'),
#     path('calculate',CalculationView.as_view(),name='calculate'),
# ]