# Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

# Models
from .models import User
from django.db.models import Q

# Form classes
from . import forms

# Response
from django.urls import reverse_lazy

# Utils
from django.contrib.auth.decorators import login_required
from django_ajax.decorators import ajax
import datetime
from swhr import utils


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'personal_details.html'
    context_object_name = 'users'
    paginate_by = 13

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'last_name')
        if self.request.user.is_superuser:
            # Filtering
            staff_id = self.request.GET.get('staff_id', '')
            name = self.request.GET.get('name', '')
            # date_joined = self.request.GET.get('date_joined', '')
            is_active = bool(self.request.GET.get('is_active', 'True'))

            if bool(staff_id + name):  # + date_joined
                print('Staff Filtering: %s %s %s %s' %
                      (staff_id, name, date_joined, is_active))

                return User.objects.order_by(order_by).filter(Q(staff_id__contains=staff_id),
                                                              Q(last_name__contains=name)
                                                              | Q(first_name__contains=name),
                                                              # Q(date_joined__contains=date_joined),
                                                              Q(is_active=is_active),
                                                              Q(is_staff=False),)
            else:
                return User.objects.order_by(order_by).filter(Q(is_staff=False),)
        else:
            return User.objects.order_by(order_by).filter(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', 'last_name')

        # Filtering
        context['staff_id'] = self.request.GET.get('staff_id', '')
        context['name'] = self.request.GET.get('name', '')
        # context['date_joined'] = self.request.GET.get('date_joined', '')
        context['is_active'] = self.request.GET.get('is_active', 'True')

        context['is_active_options'] = dict(
            {'True': 'Active', '': 'Inactive'})

        context['filter'] = 'staff_id=%s&name=%s' % (  # &date_joined=%s
            context['staff_id'], context['name'], )  # context['date_joined']

        return context


class UserCreateView(LoginRequiredMixin, CreateView):
    form_class = forms.UserCreateForm
    model = User
    template_name = 'form_employee.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = forms.UserUpdateForm
    model = User
    slug = 'staff_id'
    template_name = 'form_employee.html'


class NormalUserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = forms.NormalUserUpdateForm
    model = User
    slug = 'staff_id'
    template_name = 'form_employee.html'


@ajax
def annual_leave_calculation(request):
    date_joined = datetime.datetime.strptime(
        request.GET['date_joined'], '%Y-%m-%d').date()
    annual_leave = utils.annual_leave_to_year_end(date_joined)
    return {'annual_leave': annual_leave}
