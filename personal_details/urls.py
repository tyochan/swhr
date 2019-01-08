from django.urls import path
from . import views

app_name = 'personal_details'

urlpatterns = [
    # /personal_details/
    path('', views.IndexView.as_view(), name='index'),

    # /personal_details/string/
    path('create', views.UserCreateView.as_view(), name='create_user'),
    path('super_update/<slug>', views.UserUpdateView.as_view(),
         name='super_update_user'),

    # normal user
    path('update/<slug>', views.NormalUserUpdateView.as_view(),
         name='update_user'),

    path('ajax/annual_leave_calculation', views.annual_leave_calculation)
]
