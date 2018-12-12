from django.urls import reverse_lazy
from django.views import generic
# from .models import Leave
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from . import forms
from django.http import HttpResponseRedirect

# Create your views here.


class IndexView():
    template_name = 'payroll.html'
    # context_object_name = 'leaves'

    # def get_queryset(self):
    #     return Leave.objects.all()
