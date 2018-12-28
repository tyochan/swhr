# Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Models
from .models import Leave
from django.db.models import Q
from personal_details.models import Employee

# Form classes
from . import forms

# Response
from django.http import HttpResponseRedirect

# Utils
from . import choices


class IndexView(ListView):
    template_name = 'leave_records.html'
    context_object_name = 'leaves'
    paginate_by = 13

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', '-end_date')

        # Filtering
        staff_no = self.request.GET.get('staff_no', '')
        name = self.request.GET.get('name', '')
        type = self.request.GET.get('type', '')
        day_type = self.request.GET.get('day_type', '')
        status = self.request.GET.get('status', '')

        print('Leave Filtering: %s %s %s %s %s' %
              (staff_no, name, type, day_type, status))
        return Leave.objects.order_by(order_by).filter(Q(employee__staff_no__contains=staff_no),
                                                       Q(employee__last_name__contains=name) |
                                                       Q(employee__first_name__contains=name),
                                                       Q(type__contains=type),
                                                       Q(day_type__contains=day_type),
                                                       Q(status__contains=status),)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '-end_date')

        # Filtering
        context['staff_no'] = self.request.GET.get('staff_no', '')
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
        context['filter'] = 'staff_no=%s&name=%s&type=%s&day_type=%s&status=%s' % (
            context['staff_no'], context['name'], context['type'], context['day_type'], context['status'])

        return context


class LeaveCreateView(CreateView):
    form_class = forms.LeaveCreateForm
    model = Leave
    template_name = 'form_leave.html'

    # Update annual leave quota
    def form_valid(self, form):
        employee = Employee.objects.get(
            staff_no=form.cleaned_data['employee'].staff_no)
        employee.annual_leave -= form.cleaned_data['spend']
        employee.save()
        return super().form_valid(form)


class LeaveUpdateView(UpdateView):
    form_class = forms.LeaveUpdateForm
    model = Leave
    template_name = 'form_leave.html'

    # Updating annual leave quota and leave status
    def form_valid(self, form):
        leave = Leave.objects.get(id=self.kwargs['pk'])
        if 'reject' not in self.request.POST:
            leave.status = 'AP'
        else:
            employee = leave.employee
            employee.annual_leave += leave.spend
            employee.save()
            leave.status = 'RE'
        leave.save()
        return HttpResponseRedirect("/leave_records/")


class LeaveDetailView(UpdateView):
    form_class = forms.LeaveDetailForm
    model = Leave
    template_name = 'form_leave.html'

    # Prevent any update
    def form_valid(self, form):
        return HttpResponseRedirect("/leave_records/")
