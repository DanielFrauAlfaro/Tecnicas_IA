

def teset(a):
    if a == 0:
        return a

    value = 1+teset(a-1)
    print(value)
    return value
    

teset(6)