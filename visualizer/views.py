from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.response import SimpleTemplateResponse
import subprocess # to execute code more safely
import sys # import sys and use sys.executable to dynamically get the Python path
import trace
from io import StringIO
import textwrap
from .animate import parse_code, gen_data, frames_tojson



def home(request):
    # return HttpResponse("Welcome to Code Visualizer!")
    return render(request, 'home.html')


def process_code(code):
    """ Execute Python code safely and capture stdout, stderr, and exit status. """
    python_path = sys.executable  # Fetches path to current Python interpreter being used
    try:
        # Execute the code to capture stdout and stderr
        completed_process = subprocess.run(
            [python_path, "-c", code],
            text=True,
            capture_output=True,
            timeout=5
        )
        if completed_process.stderr:
            return completed_process.stderr, False
        return completed_process.stdout, True
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr}", False
    except subprocess.TimeoutExpired:
        return "The code execution timed out.", False
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", False

def visualize(request):
    """ Handle requests to display the code visualization page. """
    code = request.POST.get('code', '')
    output, success = process_code(code) if request.method == 'POST' else ("", False)
    return render(request, 'visualize.html', {'code': code, 'output': output, 'success': success})

def animation_view(request):
    """ Handle requests to generate animations from code. """
    if request.method == 'POST':
        code = request.POST.get('code', '')
        ast_node = parse_code(code)
        frames = gen_data(ast_node)
        frames_json = frames_tojson(frames)
        return JsonResponse({'frames': frames_json})
    return JsonResponse({'error': 'Invalid request'}, status=400)