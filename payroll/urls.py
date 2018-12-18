from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    # /payroll/
    path('', views.IndexView.as_view(), name='index'),

    # /payroll/string/
    path('create', views.PaymentCreateView.as_view(), name='create_payment'),
    # path('update/<int:pk>', views.LeaveUpdateView.as_view(), name='update_leave'),
    path('detail/<int:pk>', views.PaymentDetailView.as_view(), name='detail_payment'),

    # AJAX
    path('ajax/getSalary', views.calculateSalary, name='calculate_salary'),

    # Method
    path('generatePDF', views.generatePDF, name='generate_pdf'),
]
