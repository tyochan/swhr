from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Employee
from . import forms


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return Employee.objects.all()  # .order_by('last_name')


class EmployeeCreateView(CreateView):
    form_class = forms.EmployeeForm
    model = Employee
    template_name = 'form_employee.html'


class EmployeeUpdateView(UpdateView):
    form_class = forms.EmployeeUpdateForm
    model = Employee
    template_name = 'form_employee.html'


class EmployeeDeleteView(DeleteView):
    # form_class = forms.EmployeeDeleteForm
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('personal_details:index')
