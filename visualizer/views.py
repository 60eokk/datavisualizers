from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.response import SimpleTemplateResponse
import subprocess # to execute code more safely


def process_code(code):
    try:
        # Execute code safely in a subprocess with limited rights
        completed_process = subprocess.run(
            ["python", "-c", code],
            text=True,
            capture_output=True,
            timeout=5,  # Set a reasonable timeout to prevent long-running scripts
            check=True  # Raises CalledProcessError for non-zero exit statuses
        )
        return completed_process.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {str(e)}"
    except subprocess.TimeoutExpired:
        return "The code execution timed out."
    except Exception as e:
        return str(e)
    


def visualize(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        output = process_code(code)
        return render(request, 'result.html', {'output': output})
    return render(request, 'visualize.html')
    