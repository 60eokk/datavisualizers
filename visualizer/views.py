from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.response import SimpleTemplateResponse
import subprocess # to execute code more safely
import sys # import sys and use sys.executable to dynamically get the Python path


def process_code(code):
    python_path = sys.executable  # Automatically gets the path of the current Python interpreter
    try:
        completed_process = subprocess.run(
            [python_path, "-c", code],
            text=True,
            capture_output=True,
            timeout=5,
        )
        return completed_process.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr}"
    except subprocess.TimeoutExpired:
        return "The code execution timed out."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    


def visualize(request):
    output = ""
    if request.method == 'POST':
        code = request.POST.get('code')
        output = process_code(code)
        # return render(request, 'result.html', {'output': output})
    return render(request, 'visualize.html', {'output': output})
    