import random
import json
import math

def eight_digit_id_gen():
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    num = '1234567890'
    
    try:
        with open("helper_gen_id_tracker.json", "r") as f:
            id_tracker = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        id_tracker = []

    while True:
        gen_id = ""
        for _ in range(8):
            if random.choice([True, False]):
                gen_id += random.choice(alphabet)
            else:
                gen_id += random.choice(num)
        
        if gen_id not in id_tracker:
            id_tracker.append(gen_id)
            with open("helper_gen_id_tracker.json", "w") as f:
                json.dump(id_tracker, f, indent=2)
            return gen_id
        
def parse_number(s):
    try:
        num = int(s)
    except ValueError:
        try:
            num = float(s)
        except ValueError:
            num = s
    return num

def pagination(contents, page,cpp=10):
    if isinstance(contents, set):
        contents = list(sorted(contents))
    clens = len(contents)
    divide = math.ceil((clens/cpp))

    if page > divide:
        print(f"max page is {divide}")
    elif page < 1:
        print('no')
    else:
        for i in range(((page*cpp) - cpp) + 1,(page*cpp) + 1):
            if i < clens + 1:
                print(contents[i-1])
        
        print(f"showing page {page}/{divide} | {clens} contents")



    