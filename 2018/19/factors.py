# By inspection: program calculates the sum of factors of N, which if r0 starts at 0 is 958; if r0 starts at 1, 10551358.

N = 10551358
factors = [1,N]
half = N/2
factors.append(half)
factors.append(2)

i = 3
from math import sqrt
stop = sqrt(N)
while i < stop:
	x = N / i
	if int(x) == x:
		factors += [i,x]
	i += 2

print(factors)
print(sum(factors))
