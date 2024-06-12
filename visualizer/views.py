from django.shortcuts import render, redirect
from django.http import HttpResponse


# def index(request):
#     return HttpResponse("This is main function index.")



def visualize(request):
    # return HttpResponse("HIHI")
    if request.method == 'POST':
        code = request.POST.get('code')

        visualization_result = process_code(code)
        return render(request, 'result.html', {'visualization': visualization_result})
    return render(request, 'visualize.html')