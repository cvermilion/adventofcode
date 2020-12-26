from functools import reduce
from operator import mul

def parse_num(buf):
    digs, buf = buf[0], buf[1:]
    while buf and buf[0] in "0123456789":
        digs, buf = digs+buf[0], buf[1:]
    return int(digs), buf 

def parse_sub(buf):
    # find index of matching ')'
    i = 0
    p = 0
    while True:
        if buf[i] == "(":
            p += 1
        elif buf[i] == ")":
            p -= 1
        if p == 0:
            return parse(buf[1:i]), buf[i+1:]
        i += 1

def parse(buf):
    """ Parse an arithmetic expression from a string, return a list of numbers, operators, or lists (sub-expressions) """
    expr = []
    while buf:
        b =(buf[0])
        if b == " ":
            buf = buf[1:]
        elif b == "(":
            sub, buf = parse_sub(buf)
            expr.append(sub)
        elif b in ["*", "+"]:
            expr.append(b)
            buf = buf[1:]
        else:
            n, buf = parse_num(buf)
            expr.append(n)

    return expr

def eval(expr):
    # must be at least three terms to evaluate:
    op = expr[1]
    arg1 = eval(expr[0]) if isinstance(expr[0], list) else expr[0]
    arg2 = eval(expr[2]) if isinstance(expr[2], list) else expr[2]
    if op == "+":
        result = arg1 + arg2
    else:
        result = arg1 * arg2
    if len(expr) == 3:
        return result
    return eval([result] + expr[3:])

print("Part 1:", sum(eval(parse(s.strip())) for s in open("input.txt")))

def eval2(expr):
    # first find any additions and evaluate them first
    if "+" in expr:
        idx = expr.index("+")
        arg1 = eval2(expr[idx-1]) if isinstance(expr[idx-1], list) else expr[idx-1]
        arg2 = eval2(expr[idx+1]) if isinstance(expr[idx+1], list) else expr[idx+1]
        if len(expr) == 3:
            return arg1 + arg2
        expr = expr[:idx-1] + [arg1 + arg2] + expr[idx+2:]
        return eval2(expr)
    op = expr[1]
    arg1 = eval2(expr[0]) if isinstance(expr[0], list) else expr[0]
    arg2 = eval2(expr[2]) if isinstance(expr[2], list) else expr[2]
    result = arg1 * arg2
    if len(expr) == 3:
        return result
    return eval2([result] + expr[3:])

print("Part 2:", sum(eval2(parse(s.strip())) for s in open("input.txt")))
