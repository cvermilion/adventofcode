import aocd, re
from collections import namedtuple
from functools import cache, partial, reduce
from operator import add, mul
from queue import PriorityQueue, SimpleQueue

import math
product = math.prod

from parse import parse

from .token import *

def lmap(f, l):
	return list(map(f, l))

# Apply a sequence of functions to elements in an iterable
def pipe(seq, *element_funcs):
	acc = seq
	for spec in element_funcs:
		# func can be plain func of one arg
		# or list where func is first and rest are extra args
		if isinstance(spec, list):
			# local var so lambda doesn't capture loop var'
			func, args = spec[0], spec[1:]
			f = lambda x: func(x, *args)
		else:
			f = spec
		acc = map(f, acc)
	return acc

# Same but wrap in list()
def lpipe(seq, *element_funcs):
	return list(pipe(seq, *element_funcs))

def transpose(arr):
	return [*zip(*arr)]

def count(gen):
	return sum(1 for n in gen)

try:	
	input_test = open("input_test.txt").read().strip()
except:
	input_test = ""

get_data = aocd.get_data

def get_data_2023(day=None):
	return get_data(year=2023, day=day)

def get_data_2024(day=None):
	return get_data(year=2024, day=day)

def get_data_2025(day=None):
	return get_data(year=2025, day=day)
