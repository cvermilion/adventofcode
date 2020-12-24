nums = [n.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1") for n in open("input.txt")]
nums = [int(n, 2) for n in nums]

print("Part 1: ", max(nums))

missing = [n for n in range(2**10) if not n in nums]
mine = [n for n in missing if n+1 in nums and n-1 in nums]
print("Part 2: ", mine)

