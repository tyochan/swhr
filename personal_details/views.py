# Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Models
from .models import Employee

# Form classes
from . import forms

# Response
from django.urls import reverse_lazy

# Utils


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'employees'
    paginate_by = 15

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'last_name')
        return Employee.objects.all().order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', 'last_name')
        return context


class EmployeeCreateView(CreateView):
    form_class = forms.EmployeeForm
    model = Employee
    template_name = 'form_employee.html'


class EmployeeUpdateView(UpdateView):
    form_class = forms.EmployeeUpdateForm
    model = Employee
    template_name = 'form_employee.html'
