# Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

# Models
from .models import Leave
from django.db.models import Q
from personal_details.models import User

# Form classes
from . import forms

# Response
from django.http import HttpResponseRedirect

# Utils
from django.contrib.auth.decorators import login_required
from . import choices
from django_ajax.decorators import ajax
import datetime
from swhr import utils


class IndexView(LoginRequiredMixin, ListView):
    context_object_name = 'leaves'
    paginate_by = 13
    template_name = 'leave_records.html'

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', '-end_date')
        if self.request.user.is_superuser:
            # Filtering
            staff_id = self.request.GET.get('staff_id', '')
            name = self.request.GET.get('name', '')
            type = self.request.GET.get('type', '')
            day_type = self.request.GET.get('day_type', '')
            status = self.request.GET.get('status', '')

            if bool(staff_id + name + type + day_type + status):
                print('Leave Filtering: %s %s %s %s %s' %
                      (staff_id, name, type, day_type, status))
                return Leave.objects.order_by(order_by).filter(Q(user__is_active=True),
                                                               Q(user__staff_id__contains=staff_id),
                                                               Q(user__last_name__contains=name) |
                                                               Q(user__first_name__contains=name) | Q(user__nick_name__contains=name),
                                                               Q(type__contains=type),
                                                               Q(day_type__contains=day_type),
                                                               Q(status__contains=status),)
            else:
                return Leave.objects.order_by(order_by).filter(Q(user__is_active=True),)
        else:
            return Leave.objects.order_by(order_by).filter(user__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '-end_date')

        # Filtering
        context['staff_id'] = self.request.GET.get('staff_id', '')
        context['name'] = self.request.GET.get('name', '')
        context['type'] = self.request.GET.get('type', '')
        context['day_type'] = self.request.GET.get('day_type', '')
        context['status'] = self.request.GET.get('status', '')

        context['type_options'] = dict((key, val)
                                       for key, val in choices.LEAVE_TYPE)
        context['status_options'] = dict((key, val)
                                         for key, val in choices.STATUS_CHOICES)
        context['day_type_options'] = dict((key, val)
                                           for key, val in choices.LEAVE_DAY_TYPE)
        context['filter'] = 'staff_id=%s&name=%s&type=%s&day_type=%s&status=%s' % (
            context['staff_id'], context['name'], context['type'], context['day_type'], context['status'])
        return context


class LeaveCreateView(LoginRequiredMixin, CreateView):
    form_class = forms.LeaveCreateForm
    model = Leave
    template_name = 'form_leave.html'

    # Update annual leave quota
    def form_valid(self, form):
        user = User.objects.get(
            staff_id=form.cleaned_data['user'].staff_id)
        user.annual_leave -= form.cleaned_data['spend']
        user.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(LeaveCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class LeaveUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = forms.LeaveUpdateForm
    model = Leave
    permission_required = ('leave_records.change_leave')
    template_name = 'form_leave.html'

    # Updating annual leave quota and leave status

    def form_valid(self, form):
        leave = Leave.objects.get(id=self.kwargs['pk'])
        if 'reject' not in self.request.POST:
            leave.status = 'AP'
        else:
            user = leave.user
            user.annual_leave += leave.spend
            user.save()
            leave.status = 'RE'
        leave.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(LeaveUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class LeaveDetailView(UserPassesTestMixin, UpdateView):
    form_class = forms.LeaveDetailForm
    model = Leave
    template_name = 'form_leave.html'

    # Prevent any update
    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(LeaveDetailView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        leave = self.get_object()
        return leave.user.id == self.request.user.id or self.request.user.is_superuser


@ajax
def leave_calculation(request):
    start_date = datetime.datetime.strptime(
        request.GET['start_date'], '%Y-%m-%d')
    end_date = datetime.datetime.strptime(
        request.GET['end_date'], '%Y-%m-%d')

    days_spend = utils.period_spend_days(start_date, end_date)

    if not days_spend:  # Broken period
        days_spend = 0
    elif days_spend == 1:  # same day
        days_spend = 1 if request.GET['day_type'] == 'FD' else 0.5

    return {'days_spend': days_spend}
