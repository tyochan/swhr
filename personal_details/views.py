from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Employee

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return Employee.objects.all()

class DetailView(UpdateView):
    model = Employee
    fields = ['staff_no', 'first_name', 'last_name', 'start_date', 'start_date', 'salary', 'address', 'phone_no', 'annual_leave', 'email', 'bank_acc', 'department']
    template_name = 'detail.html'

class AddStaffView(CreateView):
    model = Employee
    fields = ['first_name', 'last_name', 'start_date', 'start_date', 'salary', 'address', 'phone_no', 'annual_leave', 'email', 'bank_acc', 'department']
    template_name = 'employee_form.html'
