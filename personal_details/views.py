# Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Models
from .models import User
from django.db.models import Q

# Form classes
from . import forms

# Response
from django.urls import reverse_lazy

# Utils
from django_ajax.decorators import ajax
import datetime
import calendar


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'users'
    paginate_by = 13

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'last_name')

        # Filtering
        staff_id = self.request.GET.get('staff_id', '')
        name = self.request.GET.get('name', '')
        date_joined = self.request.GET.get('date_joined', '')

        if bool(staff_id + name + date_joined):
            print('Staff Filtering: %s %s %s' %
                  (staff_id, name, date_joined))

            return User.objects.order_by(order_by).filter(Q(staff_id__contains=staff_id),
                                                          Q(last_name__contains=name) |
                                                          Q(first_name__contains=name),
                                                          Q(date_joined__contains=date_joined),
                                                          Q(is_staff=False),)
        else:
            return User.objects.order_by(order_by).filter(Q(is_staff=False),)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', 'last_name')

        # Filtering
        context['staff_id'] = self.request.GET.get('staff_id', '')
        context['name'] = self.request.GET.get('name', '')
        context['date_joined'] = self.request.GET.get('date_joined', '')
        context['filter'] = 'staff_id=%s&name=%s&date_joined=%s' % (
            context['staff_id'], context['name'], context['date_joined'])

        return context


class UserCreateView(CreateView):
    form_class = forms.UserCreateForm
    model = User
    template_name = 'form_employee.html'


class UserUpdateView(UpdateView):
    form_class = forms.UserUpdateForm
    model = User
    slug = 'staff_id'
    template_name = 'form_employee.html'


@ajax
def calculateAnnualLeave(request):
    date_joined = [int(x) for x in request.GET['date_joined'].split("-")]
    date_joined = datetime.date(date_joined[0], date_joined[1], date_joined[2])
    end_date = datetime.date(date_joined.year, 12, 31)
    workdays = (end_date - date_joined).days + 1
    days_of_year = 0
    if calendar.isleap(date_joined.year):
        days_of_year = 366
    else:
        days_of_year = 365
    annual_leave = round_to_neareast_half(workdays / days_of_year * 15)
    return {'annual_leave': annual_leave}


def round_to_neareast_half(number):
    return round(number * 2) / 2
