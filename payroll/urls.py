from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    # /payroll/
    path('', views.IndexView.as_view(), name='index'),

    # /payroll/string/
    path('create', views.PaymentCreateView.as_view(), name='create_payment'),
    path('detail/<int:pk>', views.PaymentDetailView.as_view(), name='detail_payment'),

    # Method
    path('ajax/getSalary', views.calculateSalary, name='calculate_salary'),
    path('generatePDF/<int:pk>', views.PaymentPDFView.as_view(), name='generate_pdf'),
]
