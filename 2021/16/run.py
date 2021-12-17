import functools
import operator

data = open("input.txt").read().strip()

def hex_to_bits(s):
    return "".join(map("{0:04b}".format, (int(c, 16) for c in s)))

class ValuePacket(object):
    def __init__(self, version, val):
        self.version = version
        self.val = val

    def version_sum(self):
        return self.version

    def value(self):
        return self.val

class OperatorPacket(object):
    def __init__(self, version, type_id, sub_packets):
        self.version = version
        self.type_id = type_id
        self.sub_packets = sub_packets

    def version_sum(self):
        return self.version + sum([p.version_sum() for p in self.sub_packets])
    
    def value(self):
        return {
            0: sum,
            1: (lambda vals: functools.reduce(operator.mul, vals, 1)),
            2: min,
            3: max,
            5: (lambda vals: 1 if vals[0] > vals[1] else 0),
            6: (lambda vals: 1 if vals[0] < vals[1] else 0),
            7: (lambda vals: 1 if vals[0] == vals[1] else 0),
        }[self.type_id]([p.value() for p in self.sub_packets])

def parse_packet(buf):
    type_id = int(buf[3:6], 2)
    if type_id == 4:
        return parse_value_packet(buf)
    return parse_operator_packet(buf)

def parse_value_packet(buf):
    ver = int(buf[:3], 2)
    # next three bits are the ID, we know this is 4
    rem = buf[6:]
    s = ""
    consumed = 6
    while rem[0] == "1":
        s, rem = s + rem[1:5], rem[5:]
        consumed += 5
    # finally 0 + 4 bits
    s += rem[1:5]
    consumed += 5
    p = ValuePacket(ver, int(s, 2))
    return p, consumed

def parse_operator_packet(buf):
    ver = int(buf[:3], 2)
    type_id = int(buf[3:6], 2)
    length_type = buf[6]
    consumed = 7
    sub_packets = []
    if length_type == '0':
        sub_length = int(buf[7:22], 2)
        consumed += 15
        while consumed-22 < sub_length:
            p, n = parse_packet(buf[consumed:])
            consumed += n
            sub_packets.append(p)
    else:
        sub_n = int(buf[7:18], 2)
        consumed += 11
        while len(sub_packets) < sub_n:
            p, n = parse_packet(buf[consumed:])
            consumed += n
            sub_packets.append(p)
    return OperatorPacket(ver, type_id, sub_packets), consumed
                  
def packet(s):
    return parse_packet(hex_to_bits(s))[0]

p = packet(data)
print("Part 1:", p.version_sum())
print("Part 2:", p.value())
