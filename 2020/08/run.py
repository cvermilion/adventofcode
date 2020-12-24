from parse import parse

ops = [list(parse("{} {:d}", d)) for d in open("input.txt")]
def ops_copy():
    return [l[:] for l in ops]

defs = {
    "acc": lambda pc,acc,x: (pc+1, acc+x),
    "jmp": lambda pc,acc,x: (pc+x, acc),
    "nop": lambda pc,acc,x: (pc+1, acc),
}

def result_before_loop(ops):
    acc = 0
    pc = 0
    seen = set([])
    while not pc in seen:
        seen.add(pc)
        op = ops[pc]
        pc, acc = defs[op[0]](pc, acc, op[1])
    return acc

print("Part 1:", result_before_loop(ops))

def real_result(ops):
    acc = 0
    pc = 0
    seen = set([])
    while not pc in seen:
        if pc == len(ops):
            return acc
        seen.add(pc)
        op = ops[pc]
        pc, acc = defs[op[0]](pc, acc, op[1])
    return None

def check_term(i):
    if ops[i] == "acc":
        return None
    myops = ops_copy()
    if myops[i][0] == "nop":
        myops[i][0] = "jmp"
    else:
        myops[i][0] = "nop"
    return real_result(myops)

for i in range(len(ops)):
    r = check_term(i)
    if r is not None:
        print("Part 2:", r)
        break



