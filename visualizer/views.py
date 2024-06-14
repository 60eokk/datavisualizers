from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.response import SimpleTemplateResponse
import subprocess # to execute code more safely
import sys # import sys and use sys.executable to dynamically get the Python path

def home(request):
    # return HttpResponse("Welcome to Code Visualizer!")
    return render(request, 'home.html')

def process_code(code):
    python_path = sys.executable  # Use the Python executable that's running the script
    try:
        completed_process = subprocess.run(
            [python_path, "-c", code],
            text=True,
            capture_output=True,
            timeout=5
        )
        # Check if there was an error
        if completed_process.stderr:
            return "Error:\n" + completed_process.stderr
        return completed_process.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr}"
    except subprocess.TimeoutExpired:
        return "The code execution timed out."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    


def visualize(request):
    code = ""  # Default to empty if no POST request
    output = ""
    if request.method == 'POST':
        code = request.POST.get('code')
        output = process_code(code)
    return render(request, 'visualize.html', {'code': code, 'output': output})