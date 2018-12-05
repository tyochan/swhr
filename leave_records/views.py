from django.shortcuts import render
from django.views import generic
from .models import Leave
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import forms

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'leave_records.html'
    context_object_name = 'leaves'

    def get_queryset(self):
        return Leave.objects.all()


class LeaveCreateView(CreateView):
    form_class = forms.LeaveCreateForm
    model = Leave
    template_name = 'form.html'


class LeaveUpdateView(UpdateView):
    form_class = forms.LeaveUpdateForm
    model = Leave
    template_name = 'form.html'
