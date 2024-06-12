from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.response import TemplateResponse

# def index(request):
#     return HttpResponse("This is main function index.")


def process_code(code):
    return 0


def visualize(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        visualization_result = process_code(code)
        return render(request, 'result.html', {'visualization': visualization_result})
    return render(request, 'visualize.html')
    return HttpResponse("HIHI")