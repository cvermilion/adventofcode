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
#print(ill)

points = {
	")": 3,
	"}": 1197,
	"]": 57,
	">": 25137,
	None: 0
}

score = sum([points[first_illegal([], l)] for l in lines ])
print(score)
