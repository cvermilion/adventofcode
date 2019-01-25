input=open("text.txt").read().strip()
print(len(input))

output = []

def top(stack):
	if len(stack) > 0:
		return stack[-1]
	return ' '

def pop(stack):
	return stack[:-1]

def cancel(c1, c2):
	o1, o2 = ord(c1), ord(c2)
	return abs(o1-o2) == 32

def push(stack, c):
	if cancel(top(stack), c):
		#print(top(stack),"and",c,"cancel")
		s = pop(stack)
		#print("".join(s))
		return s
	else:
		#print("appending",c)
		stack.append(c)
		#print("".join(stack))
		return stack
		
#input="dabAcCaCBAcCcaDA"
#print(input[0], input[-1])

def compress(s):
	out = []
	for c in s:
		out = push(out, c)
	return out
	

print(len(compress(input)))
#print(output[:20])
#print(output[-20:])

shortest = len(input)
for A in range(ord('A'), ord('A')+26):
	a = A+32
	text = input.replace(chr(A), "").replace(chr(a), "")
	l = len(compress(text))
	if l < shortest:
		shortest = l

print(shortest)
	
