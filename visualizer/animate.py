import ast
import json


def parse_code(code):
    # print(ast.parse(code))
    print("parse_code works")
    return ast.parse()
    # parsed = ast.parse(code)
    # print(ast.dump(parsed, indent=4))
    # return parsed




class DataGenerator(ast.NodeVisitor):
    def __init__(self):
        self.frames = []

    def visit_Assign(self, node):
        # Handle assignment operations
        # Example: Extract variable name and value
        target = node.targets[0].id
        value = ast.dump(node.value)
        self.frames.append({target: value})
        self.generic_visit(node)

    def visit_For(self, node):
        # Handle loops
        # Example: Extract loop details
        self.frames.append({'loop_start': node.lineno})
        self.generic_visit(node)



def gen_data(ast_node):
    generator = DataGenerator()
    generator.visit(ast_node)
    return generator.frames


def frames_tojson(frames):
    # Convert frames data to JSON
    try:
        return json.dumps(frames)
    except TypeError as e:
        # Handle serialization errors
        return json.dumps({'error': str(e)})
