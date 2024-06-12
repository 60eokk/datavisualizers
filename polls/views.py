from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("This is polls index.")
    return 2+3


