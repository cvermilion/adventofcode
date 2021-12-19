import math
import functools

data = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""

data = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

data = open("input.txt").read().strip()

ts = list(map(eval, data.split("\n")))

class Node(object):
    def __init__(self, par, inp):
        self.parent = par
        if isinstance(inp, int):
            self.val = inp
        else:
            self.val = None
            self.left = Left(self, inp[0])
            self.right = Right(self, inp[1])

    def leaf(self):
        return self.val is not None

    def tup(self):
        if self.val is not None:
            return self.val
        return [self.left.tup(), self.right.tup()]

    def mag(self):
        if self.val is not None:
            return self.val
        return 3 * self.left.mag() + 2 * self.right.mag()

class Left(Node):
    pass

class Right(Node):
    pass

class Root(Node):
    def __init__(self, inp):
        # never a leaf
        self.val = None
        self.parent = None
        self.left = Left(self, inp[0])
        self.right = Right(self, inp[1])

def first_left_neighbor(node):
    if isinstance(node, Right):
        n = node.parent.left
        while not n.leaf():
            n = n.right
        return n
    elif isinstance(node, Left):
        return first_left_neighbor(node.parent)
    # root
    return None

def first_right_neighbor(node):
    if isinstance(node, Left):
        n = node.parent.right
        while not n.leaf():
            n = n.left
        return n
    elif isinstance(node, Right):
        return first_right_neighbor(node.parent)
    # root
    return None

def explode(node):
    l = node.left.val
    r = node.right.val
    n = first_left_neighbor(node)
    if n:
        n.val += l
    n = first_right_neighbor(node)
    if n:
        n.val += r
    node.val = 0
    node.left = None
    node.right = None

# try to descend at least depth nodes to find a pair
def descend_to_pair(node, depth):
    if node.leaf():
        return None
    if depth == 0:
        return node
    return descend_to_pair(node.left, depth-1) or descend_to_pair(node.right, depth-1)

def split(node):
    val = node.val
    l = math.floor(val/2)
    r = math.ceil(val/2)
    node.left = Left(node, l)
    node.right = Right(node, r)
    node.val = None

def first_over_10(node):
    if node.leaf():
        if node.val >= 10:
            return node
        return None
    return first_over_10(node.left) or first_over_10(node.right)

def add(t1, t2):
    # would be more efficient to define an add that operated on nodes instead of converting back to lists, but :shrug:
    r = Root([t1, t2])
    while True:
        # reduction loop: try to explode, if nothing to explode, try a split
        n = descend_to_pair(r, 4)
        if n:
            explode(n)
            continue
        n = first_over_10(r)
        if n:
            split(n)
        else:
            # nothing left
            break
    return r.tup()

s = Root(functools.reduce(add, ts))
print("Part 1:", s.mag())

# Part 2: find largest magnitude of sum of two numbers:
largest = 0
for i,t1 in enumerate(ts):
    for j,t2 in enumerate(ts):
        if i == j:
            continue
        s = Root(add(t1,t2)).mag()
        if s > largest:
            largest = s

print("Part 2:", largest)

