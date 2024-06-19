import ast
import json


def parse_code(code):
    # print(ast.parse(code))
    # print("parse_code works")
    return ast.parse(code)

def gen_data(ast_node): # complex code
    frames = []

    return frames

def frames_tojson(frames):
    return json.dumps(frames)

