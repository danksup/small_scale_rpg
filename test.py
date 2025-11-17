import math

def pagination(contents, page,cpp=10): #cpp = contents per page
    if isinstance(contents, set):
        contents = list(sorted(contents))
    clens = len(contents)
    divide = math.ceil((clens/cpp))

    if page > divide:
        print(f"max page is {divide}")
    elif page < 1:
        print('no')
    else:
        print(f"showing page {page}/{divide}")
        for i in range(((page*cpp) - cpp) + 1,(page*cpp) + 1):
            if i < clens + 1:
                print(contents[i-1])

contens = [i for i in range(1,101)]
pagination(contens, 2)
