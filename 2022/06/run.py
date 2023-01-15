import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#test()
input = get_input()

for part, N in enumerate([4,14]):
	for i in range(N, len(input)):
		if len(set(input[i-N:i])) == N:
			break
	print("Part {:d}: {:d}".format(part+1, i))

