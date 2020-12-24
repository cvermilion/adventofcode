nums = [int(l) for l in open("input.txt")]
window = 25

def check(nums, i, window):
    total = nums[i]
    preamble = nums[i-window:i]
    for j in range(window):
        for k in range(j+1, window):
            if preamble[j] != preamble[k] and preamble[j] + preamble[k] == total:
                return True
    return False

N = 0
for i in range(window, len(nums)):
    if not check(nums, i, window):
        N = nums[i]
        print("Part 1:", N)
        break

# Part 2: find a contiguous range that sums to N

# Approach: iterate over L, the size of the window we're summing, and compute the sum of nums[i:i+L] for each i and check

L=2
while True:
    sums = [(i, sum(nums[i:i+L])) for i in range(len(nums)-L)]
    match = [(i,s) for (i,s) in sums if s == N]
    if match:
        i = match[0][0]
        nn = nums[i:i+L]
        print("Part 2:", min(nn)+max(nn))
        break
    L+=1



