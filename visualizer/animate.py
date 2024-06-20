import ast
import json

def parse_code(code):
    """ Parse Python code to an AST. """
    return ast.parse(code)

def resolve_value(node):
    """ Simplistically resolve values from AST nodes. """
    if isinstance(node, ast.Num):  # For Python 3.7 and below
        return node.n
    elif isinstance(node, ast.Constant):  # For Python 3.8 and above
        return node.value
    elif isinstance(node, ast.List):
        return [resolve_value(elem) for elem in node.elts]
    elif isinstance(node, ast.UnaryOp):
        operand = resolve_value(node.operand)
        if isinstance(node.op, ast.USub):
            return -operand
    return None

def gen_data(ast_node):
    """ Generate frames by manually traversing the AST. """
    frames = []
    for node in ast.walk(ast_node):
        if isinstance(node, ast.For):
            # Resolve iteration variable and range
            iter_var = node.target.id if isinstance(node.target, ast.Name) else None
            iter_range = resolve_value(node.iter)
            
            # Start of loop
            frames.append({'type': 'loop_start', 'iter_var': iter_var, 'iter_range': iter_range})
            
            # Hypothetically execute loop body
            for _ in range(iter_range):  # Assuming it's a simple range
                for body_node in node.body:
                    if isinstance(body_node, ast.Assign):
                        # Handle assignments within the loop
                        target = body_node.targets[0].id if isinstance(body_node.targets[0], ast.Name) else None
                        value = resolve_value(body_node.value)
                        frames.append({'type': 'assign', 'target': target, 'value': value})
            
            # End of loop
            frames.append({'type': 'loop_end', 'iter_var': iter_var})

    return frames

def frames_tojson(frames):
    """ Convert frames to JSON format. """
    try:
        return json.dumps(frames)
    except TypeError as e:
        return json.dumps({'error': str(e)})
