# trace function
# was initially created inside visuazlier/views.py to in order to better understand the input and code and animate
# however, it was unnecessary
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