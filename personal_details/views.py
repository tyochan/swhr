from django.shortcuts import render
from django.http import HTTPResponse

# Create your views here.
def index(Response):
    return HTTPResponse('<h1>Homepage')
