from django.urls import path
from . import views

app_name = 'leave_records'

urlpatterns = [
    # /leave_records/
    path('', views.IndexView.as_view(), name='index'),

    # /leave_records/string/
    path('create', views.LeaveCreateView.as_view(), name='create_leave'),
    path('update/<int:pk>', views.LeaveUpdateView.as_view(), name='update_leave'),
    path('detail/<int:pk>', views.LeaveDetailView.as_view(), name='detail_leave'),
]
