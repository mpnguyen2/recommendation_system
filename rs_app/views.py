from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(requests):
    return HttpResponse('Hello. You\'re at index page')