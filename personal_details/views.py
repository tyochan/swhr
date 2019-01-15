# Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth import views as auth_views

# Models
from .models import User, SalaryTitleRecord, AcademicRecord
from django.db.models import Q

# Form classes
from . import forms

# Response
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

# Utils
from django_ajax.decorators import ajax
import datetime
from swhr import utils


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'personal_details.html'
    context_object_name = 'users'
    paginate_by = 13

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return HttpResponseRedirect(reverse_lazy('personal_details:update_user', kwargs={'slug': self.request.user.slug}))
        return super().get(request)

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'last_name')
        if self.request.user.is_superuser:
            # Filtering
            staff_id = self.request.GET.get('staff_id', '')
            name = self.request.GET.get('name', '')
            is_active = bool(self.request.GET.get('is_active', 'True'))

            if bool(staff_id + name):
                print('Staff Filtering: %s %s %s' %
                      (staff_id, name, is_active))

                return User.objects.order_by(order_by).filter(Q(staff_id__contains=staff_id),
                                                              Q(last_name__contains=name)
                                                              | Q(first_name__contains=name),
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
        context['is_active'] = self.request.GET.get('is_active', 'True')

        context['is_active_options'] = dict(
            {'True': 'Active', '': 'Inactive'})

        context['filter'] = 'staff_id=%s&name=%s' % (
            context['staff_id'], context['name'], )

        return context


class UserCreateView(PermissionRequiredMixin, CreateView):
    form_class = forms.UserCreateForm
    model = User
    template_name = 'form_create_employee.html'
    permission_required = 'personal_details.create_user'

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['ARFormset'] = forms.AcademicRecordInlineFormset(
            queryset=AcademicRecord.objects.none())
        return context

    def form_valid(self, form):
        super().form_valid(form)
        user = User.objects.get(
            staff_id=form.cleaned_data['staff_id'])
        data = form.cleaned_data
        salary_record = SalaryRecord(
            date_changed=data['date_joined'], amount=data['salary'], grade=data['salary_grade'], user=user)
        salary_record.save()

        title_record = TitleRecord(
            date_changed=data['date_joined'], name=data['title'], grade=data['title_grade'], user=user)
        title_record.save()
        return HttpResponseRedirect(reverse_lazy('personal_details:index'))


class UserUpdateView(UserPassesTestMixin, UpdateView):
    form_class = forms.UserUpdateForm
    model = User
    slug = 'staff_id'
    template_name = 'form_employee.html'

    def test_func(self):
        user = self.get_object()
        return (user.slug == self.request.user.slug and user.is_active) or self.request.user.is_superuser

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AcademicRecordChangeView(PermissionRequiredMixin, FormView):
    form_class = forms.AcademicRecordForm
    model = AcademicRecord
    template_name = 'formset_academic_record.html'
    permission_required = 'personal_details.create_user'

    def get_context_data(self, **kwargs):
        context = super(AcademicRecordChangeView,
                        self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = forms.AcademicRecordFormSet(self.request.POST)
        else:
            context['formset'] = forms.AcademicRecordFormSet()
            context['formset_helper'] = forms.AcademicRecordFormsetHelper()
        return context


@ajax
def annual_leave_calculation(request):
    date_joined = datetime.datetime.strptime(
        request.GET['date_joined'], '%Y-%m-%d').date()
    annual_leave = utils.annual_leave_to_year_end(date_joined)
    return {'annual_leave': annual_leave}
