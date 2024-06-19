from django.shortcuts import render, redirect
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


def animation_view(request):
    """Handle requests to generate animations."""
    code = request.POST.get('code', '')
    ast_node = parse_code(code)
    frames = gen_data(ast_node)
    frames_json = frames_tojson(frames)
    return JsonResponse({'frames': frames_json})


def process_code(code):
    python_path = sys.executable # fetches path to current Python interpreter being used (ACE Editor in this case)
    try:
        # Execute the code normally to capture stdout and stderr
        completed_process = subprocess.run(
            [python_path, "-c", code],
            text=True,
            capture_output=True,
            timeout=5
        )
        # Handle errors and normal output
        if completed_process.stderr:
            return "Error:\n" + completed_process.stderr, False
        # print("working")
        # return parse_code(code)
        return completed_process.stdout, True
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr}", False
    except subprocess.TimeoutExpired:
        return "The code execution timed out.", False
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", False
    

def visualize(request):
    code = ""  # Default to empty if no POST request
    output = ""
    success = False # Default to false
    if request.method == 'POST':
        code = request.POST.get('code')
        output = process_code(code)
    # rendering response back to user KEEPS original input
    # request: original HTTP request object
    # context library {}: code is input which is retrieved, output: is result whether it be error or output
    return render(request, 'visualize.html', {'code': code, 'output': output, 'success': success}) 
    