from parse import parse

data = open("input.txt").readlines()
ops = [list(parse("{} {:d}", d)) for d in data]
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

def result_with_path(ops):
    acc = 0
    pc = 0
    path = []
    seen = set([])
    while not pc in seen:
        path.append(pc)
        seen.add(pc)
        op = ops[pc]
        pc, acc = defs[op[0]](pc, acc, op[1])
    return path, acc

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

def step(ops, pc, acc, full_seen):
    seen = set([])
    while not pc in seen:
        if (pc,acc) in full_seen:
            # signal infinite loop
            return None, None
        if pc == len(ops):
            return None, acc
        seen.add(pc)
        full_seen.add((pc,acc))
        op = ops[pc]
        pc, acc = defs[op[0]](pc, acc, op[1])
    return pc, acc

candidates = dict((i, [None, 0, 0, set([])]) for i in range(len(ops)) if ops[i][0] != "acc")
for i in candidates:
    newops = ops_copy()
    if newops[i][0] == "jmp":
        newops[i][0] = "nop"
    else:
        newops[i][0] == "jmp"
    candidates[i][0] = newops

def do_pass():
    new_candidates = {}
    for i,(ops,pc,acc,full_seen) in candidates.items():
        next_pc,next_acc = step(ops, pc, acc, full_seen)
        if next_acc is None:
            # can drop this candidate, infinite loop
            continue
        if next_pc is None:
            # winner winner
            print("Part 2:", next_acc)
            return None
        new_candidates[i] = [ops, next_pc, next_acc, full_screen]
    return new_candidates

    
i = 1
while False: #candidates:
    print(i)
    i+=1
    candidates = do_pass()

def check_term(i):
    if ops[i] == "acc":
        return None
    myops = ops_copy()
    if myops[i][0] == "nop":
        myops[i][0] = "jmp"
    else:
        myops[i][0] = "nop"
    return real_result(myops)


print(result_with_path(ops))
for i in range(len(ops)):
    r = check_term(i)
    if r is not None:
        print("Part 2:", r)
        break



