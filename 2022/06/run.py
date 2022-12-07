input_test = "mjqjpqmgbljsphdztnvjfqwrcgsml"

input = input_test
input = open("input.py").read()

for N in (4,14):
	for i in range(N, len(input)):
		if len(set(input[i-N:i])) == N:
			break
	print(i)

