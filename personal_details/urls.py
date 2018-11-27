from django.urls import path
from . import views

app_name = 'personal_details'

urlpatterns = [
    #/personal_details/
    path('', views.index, name = 'index'),

    #/personal_details/string/
    path('<int:staff_no>', views.detail, name = 'detail'),
    path('new_staff', views.new_staff, name = 'new_staff'),
    path('edit_staff', views.edit_staff, name = 'edit_staff'),
]
