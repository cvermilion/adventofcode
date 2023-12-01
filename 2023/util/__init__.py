import aocd
from functools import partial, reduce
from operator import add, mul
import re

try:
	input_test = open("input_test.txt").read().strip()
except:
	input_test = ""

def lmap(f, l):
	return list(map(f, l))

# Apply a sequence of functions to elements in a list
def thread(l, *element_funcs):
	return reduce(lambda acc, f: map(f, acc), element_funcs, l)

def get_data(day=None):
	return aocd.get_data(year=2023, day=day)

