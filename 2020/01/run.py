nums = open("input.txt").read().splitlines()
nums = [int(n) for n in nums]

for i, ni in enumerate(nums[:-1]):
    for nj in nums[i+1:]:
        if ni+nj == 2020:
            print("Part 1: ", ni*nj)
            break

for i, ni in enumerate(nums[:-1]):
    for j, nj in enumerate(nums[i+1:]):
        for nk in nums[j+1:]:
            if ni+nj+nk == 2020:
                print("Part 2: ", ni*nj*nk)
                break
