from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(Response):
    return HttpResponse('<h1>Homepage')
