from parse import parse

#data = [l for l in open("input.txt").readlines()]
data = [parse("{:d}-{:d} {}: {}", l) for l in open("input.txt").readlines()]

def check_pw_part1(pw_data):
    cnt = len(pw_data[3]) - len(pw_data[3].replace(pw_data[2], ""))
    return cnt >= pw_data[0] and cnt <= pw_data[1]

def check_pw_part2(pw_data):
    a = ( pw_data[3][pw_data[0]-1] if pw_data[0]-1 < len(pw_data[3]) else "") == pw_data[2]
    b = ( pw_data[3][pw_data[1]-1] if pw_data[1]-1 < len(pw_data[3]) else "") == pw_data[2]
    return a ^ b

print("Part 1: ", len([p for p in data if check_pw_part1(p)]))
print("Part 2: ", len([p for p in data if check_pw_part2(p)]))

