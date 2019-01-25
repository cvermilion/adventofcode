# square N has (2N-1)^2 at lower right corner
# biggest square of odd n smaller than 312051 is 557^2 = 310249, making 279 square rings
# right side, top and left add 558 each, gets to new lower left 311923
# input is 129 into bottom row, which is 559 across, so 280-129=151 from middle
# so distance is 151 + 279 = 430
print("Part 1: 430")

"""
This is a known sequence, available at OEIS:
http://oeis.org/search?q=1%2C1%2C2%2C4%2C5%2C10%2C11%2C23&sort=&language=english&go=Search
=> http://oeis.org/A141481
=> manual scan reveals first element higher than 312052 is:
"""
print("Part 2: 312453")
