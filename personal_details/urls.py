from django.urls import path
from . import views

urlpatterns = [
    #/personal_details/
    path('', views.index, name = 'index'),

    #/personal_details/
    path('<int:employee_id>', views.details, name = 'details')
]
