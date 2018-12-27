# Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Models
from .models import Employee
from django.db.models import Q

# Form classes
from . import forms

# Response
from django.urls import reverse_lazy

# Utils


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'employees'
    paginate_by = 13

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'last_name')

        # Filtering
        staff_no = self.request.GET.get('staff_no', '')
        name = self.request.GET.get('name', '')
        join_date = self.request.GET.get('join_date', '')
        print('Staff Filtering: %s %s %s' %
              (staff_no, name, join_date))

        return Employee.objects.order_by(order_by).filter(Q(staff_no__contains=staff_no), Q(last_name__contains=name) | Q(first_name__contains=name),
                                                          Q(join_date__contains=join_date))

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', 'last_name')

        # Filtering
        context['staff_no'] = self.request.GET.get('staff_no', '')
        context['name'] = self.request.GET.get('name', '')
        context['join_date'] = self.request.GET.get('join_date', '')

        return context


class EmployeeCreateView(CreateView):
    form_class = forms.EmployeeForm
    model = Employee
    template_name = 'form_employee.html'


class EmployeeUpdateView(UpdateView):
    form_class = forms.EmployeeUpdateForm
    model = Employee
    template_name = 'form_employee.html'
