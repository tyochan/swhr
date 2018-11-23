from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('<h1>Homepage')

def details(request, employee_id):
    return HttpResponse('<p>details of employee %s' % employee_id)
