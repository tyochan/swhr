from django.urls import reverse_lazy
from django.views import generic
from .models import Payment
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from . import forms
from django.http import HttpResponseRedirect

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'payroll.html'
    context_object_name = 'payments'

    def get_queryset(self):
        return Payment.objects.all()
