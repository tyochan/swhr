from django.urls import path
from . import views

app_name = 'leave_records'

urlpatterns = [
    # /leave_records/
    path('', views.IndexView.as_view(), name='index'),

    # /leave_records/string/
    path('super_create', views.LeaveCreateView.as_view(),
         name='super_create_leave'),
    path('update/<pk>', views.LeaveUpdateView.as_view(), name='update_leave'),
    path('detail/<pk>', views.LeaveDetailView.as_view(), name='detail_leave'),

    path('create', views.NormalLeaveCreateView.as_view(), name='create_leave'),

    # Method
    path('ajax/leave_calculation', views.leave_calculation),
]
