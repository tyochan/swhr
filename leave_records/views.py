from django.shortcuts import render
from django.views import generic
from .models import Leave
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import forms
from django.forms import ValidationError
from django.contrib import messages

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'leave_records.html'
    context_object_name = 'leaves'

    def get_queryset(self):
        return Leave.objects.all()


class LeaveCreateView(CreateView):
    form_class = forms.LeaveForm
    model = Leave
    template_name = 'form.html'

    def form_valid(self, form):
        if form.cleaned_data.get("spend"):
            cleaned_data = form.cleaned_data
            type = cleaned_data.get("type")
            if type == 'AL':
                quota = cleaned_data.get("employee").annual_leave
                spend = cleaned_data.get("spend")
                if spend > quota:
                    raise ValidationError('Leave spends exceeds quota.')
        return super().form_valid(form)


class LeaveUpdateView(UpdateView):
    form_class = forms.LeaveUpdateForm
    model = Leave
    template_name = 'form.html'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
