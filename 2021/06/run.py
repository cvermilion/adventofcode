import numpy as np
from numpy.linalg import matrix_power

data = open("input.txt").read()
fish = eval("[" + data + "]")

# As Tolstoy said, every happy lanternfish is the same.
# So we just track how many exist for each counter.
initial_state = [len([f for f in fish if f == i]) for i in range(9)]

# The key bit: when we just track the number of each counter, each
# step is a linear transformation, i.e., a matrix multiplication on
# the counter vector.
tr = np.zeros((9,9))
# each counter gets its next value from the one higher
for i in range(8):
    tr[i,i+1] = 1
# plus, counters 6 and 8 "spawn" from the previous 0 value
tr[6,0] = 1
tr[8,0] = 1

# Each step is just tr * state, N steps is (tr^N) * state
print("Part 1:", np.sum(np.matmul(matrix_power(tr, 80), initial_state)))
print("Part 2:", np.sum(np.matmul(matrix_power(tr, 256), initial_state)))



