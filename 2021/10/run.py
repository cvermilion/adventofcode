data = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

data = open("input.txt").read()

lines = data.split("\n")

closers = {
	"(": ")",
	"{": "}",
	"[": "]",
	"<": ">"
}

def first_illegal(stack, text):
	if not text:
		return None
	top = stack[-1] if stack else None
	nxt, text = text[0], text[1:]
	if top in closers and closers[top] == nxt:
		stack.pop()
		return first_illegal(stack, text)
	if nxt not in closers:
		return nxt
	stack.append(nxt)
	return first_illegal(stack, text)

ill = [first_illegal([], l) for l in lines]

points = {
	")": 3,
	"}": 1197,
	"]": 57,
	">": 25137,
	None: 0
}

score = sum([points[first_illegal([], l)] for l in lines ])
print("Part 1:", score)

def open_part(stack, text):
	if not text:
		return stack
	top = stack[-1] if stack else None
	nxt, text = text[0], text[1:]
	if top in closers and closers[top] == nxt:
		stack.pop()
		return open_part(stack, text)
	if nxt not in closers:
		raise RuntimeError("wat")
	stack.append(nxt)
	return open_part(stack, text)

incoms = [open_part([], l) for l in lines if not first_illegal([], l)]

comps = [list(reversed([closers[c] for c in l])) for l in incoms]

value = {
	")":1,
	"]":2,
	"}":3,
	">":4
}

def score(l):
	if not l:
		return 0
	return value[l[-1]] + 5*score(l[:-1])

scores = [score(l) for l in comps]

mid = sorted(scores)[int(len(scores)/2)]
print("Part 2:", mid)
