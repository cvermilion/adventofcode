# NB: Pythonista forces a .py extension so the input files end in .py...
input_test = open("input_test.py").read().strip()
input = open("input.py").read().strip()

def test():
    global input
    input = input_test

import sys
if "--test" in sys.argv:
    test()

def get_input():
    return input
