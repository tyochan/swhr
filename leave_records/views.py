from django.urls import reverse_lazy
from django.views import generic
from .models import Leave
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import forms
from django.http import HttpResponseRedirect

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'leave_records.html'
    context_object_name = 'leaves'

    def get_queryset(self):
        return Leave.objects.all()


class LeaveCreateView(CreateView):
    form_class = forms.LeaveCreateForm
    model = Leave
    template_name = 'form_leave.html'


class LeaveUpdateView(UpdateView):
    form_class = forms.LeaveUpdateForm
    model = Leave
    template_name = 'form_leave.html'

    # Updating employee leave quota and leave status
    def form_valid(self, form):
        leave = Leave.objects.get(id=self.kwargs['pk'])
        if 'reject' not in self.request.POST:
            employee = leave.employee
            employee.annual_leave -= form.cleaned_data['spend']
            employee.save()
            leave.status = 'AP'
        else:
            leave.status = 'RE'
        leave.save()
        return HttpResponseRedirect("/leave_records/")


class LeaveDetailView(UpdateView):
    form_class = forms.LeaveDetailForm
    model = Leave
    template_name = 'form_leave.html'
