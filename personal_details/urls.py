from django.urls import path
from . import views

app_name = 'personal_details'

urlpatterns = [
    # /personal_details/
    path('', views.IndexView.as_view(), name='index'),

    # /personal_details/string/
    path('create', views.UserCreateView.as_view(), name='create_user'),
    path('update/<slug>', views.UserUpdateView.as_view(),
         name='update_user'),
    # path('change_salary', views.ChangeSalaryView.as_view(), name='change_salary'),
    # path('change_title', views.ChangeTitleView.as_view(), name='change_title'),
    # path('change_academic_record/<slug>',
    #      views.AcademicRecordChangeView.as_view(), name='change_academic_record'),

    path('ajax/annual_leave_calculation', views.annual_leave_calculation)
]
