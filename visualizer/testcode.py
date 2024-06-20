



print(2)

print("hi")

for i in range(3, 93, 3):
    print(i)



# print(2+"2")



for i in range(3):
    x = i * 2



# Example usage
code = """
for i in range(3):
    x = i * 2
"""
parsed_code = parse_code(code)
frames = generate_frames(parsed_code)
frames_json = frames_to_json(frames)
print(frames_json)