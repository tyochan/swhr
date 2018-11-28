from django.urls import path
from . import views

app_name = 'personal_details'

urlpatterns = [
    #/personal_details/
    path('', views.IndexView.as_view(), name = 'index'),

    #/personal_details/string/
    path('<int:pk>', views.DetailView.as_view(), name = 'detail'),
    path('add', views.AddStaffView.as_view(), name = 'add_staff'),
]
