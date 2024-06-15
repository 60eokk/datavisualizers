from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.response import SimpleTemplateResponse
import subprocess # to execute code more safely
import sys # import sys and use sys.executable to dynamically get the Python path
import trace
from io import StringIO
import textwrap


def home(request):
    # return HttpResponse("Welcome to Code Visualizer!")
    return render(request, 'home.html')


def trace_execution(code):
    # Redirect stdout to capture output
    original_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()

    # Setting up the trace
    tracer = trace.Trace(count=False, trace=True)
    
    # Wrap the user's code into a function to isolate it
    wrapped_code = f"def temp_func():\n{textwrap.indent(code, '    ')}\ntemp_func()"

    # Execute the wrapped code under the tracer
    try:
        exec(wrapped_code)
        # Run the tracer
        tracer.run(wrapped_code)
    except Exception as e:
        return f"Trace Failed: {str(e)}"
    finally:
        # Restore standard output
        sys.stdout = original_stdout

    return captured_output.getvalue()

def process_code(code):
    python_path = sys.executable
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
            return "Error:\n" + completed_process.stderr
        trace_output = trace_execution(code)
        return f"Output:\n{completed_process.stdout}\nTrace:\n{trace_output}"
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