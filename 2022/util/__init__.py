# global imports
from parse import parse
from functools import *
from itertools import *
import operator
import math
import time


# NB: Pythonista forces a .py extension so the input files end in .py...
input = open("input.py").read().strip("\n")

def test():
	global input
	input = open("input_test.py").read().strip("\n")

def test2():
	global input
	input = open("input_test2.py").read().strip("\n")

import sys
if "--test" in sys.argv:
    test()

if "--test2" in sys.argv:
    test2()

def get_input():
    return input
