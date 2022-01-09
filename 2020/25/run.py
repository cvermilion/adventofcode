def find_loop_size(key):
	i = 0
	n = 1
	while n != key:
		n = (n*7) % 20201227
		i += 1
	return i

def enc_key(loops, pub_key):
	n = 1
	for i in range(loops):
		n = (n*pub_key)% 20201227
	return n

# test
card_pub_key = 5764801
door_pub_key = 17807724

# real
card_pub_key = 8458505
door_pub_key = 16050997

card_loops = find_loop_size(card_pub_key)
door_loops = find_loop_size(door_pub_key)

k = enc_key(card_loops, door_pub_key)
print("Part 1:", k)
