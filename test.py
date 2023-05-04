import random

def randomTokens():
    tokens = ''
    for i in range(6):
        val = str(random.randint(1, 9))
        tokens += val
        print(val)
    print(tokens)

randomTokens()
# print(test)