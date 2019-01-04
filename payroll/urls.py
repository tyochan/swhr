from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    # /payroll/
    path('', views.IndexView.as_view(), name='index'),

    # /payroll/string/
    path('create', views.PaymentCreateView.as_view(), name='create_payment'),
    path('detail/<int:pk>', views.PaymentDetailView.as_view(), name='detail_payment'),
    path('update/<int:pk>', views.PaymentUpdateView.as_view(), name='update_payment'),
    path('last/create', views.LastPaymentCreateView.as_view(),
         name='create_last_payment'),
    path('last/update/<int:pk>', views.LastPaymentUpdateView.as_view(),
         name='update_last_payment'),
    path('last/detail/<int:pk>', views.LastPaymentDetailView.as_view(),
         name='detail_last_payment'),

    # Method
    path('ajax/payment_calculation', views.payment_calculation),
    path('last/ajax/payment_calculation', views.payment_calculation),
    path('payslipPDF/<int:pk>', views.PaymentPDFView.as_view(), name='payslip_pdf'),
    path('last/payslipPDF/<int:pk>',
         views.LastPaymentPDFView.as_view(), name='last_payslip_pdf'),
]
