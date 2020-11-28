CHECK_MODE = False

def check(condtion, str):
    if CHECK_MODE and condtion:
        print('[Check Failed] -----', str)
        exit(0)