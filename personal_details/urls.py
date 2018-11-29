from django.urls import path
from . import views

app_name = 'personal_details'

urlpatterns = [
    # /personal_details/
    path('', views.IndexView.as_view(), name='index'),

    # /personal_details/string/
    path('create', views.EmployeeCreateView.as_view(), name='create_staff'),
    path('update/<int:pk>', views.EmployeeUpdateView.as_view(), name='update_staff'),
    path('delete/<int:pk>', views.EmployeeDeleteView.as_view(), name='delete_staff'),
]
