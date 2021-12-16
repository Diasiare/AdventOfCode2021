import itertools
import operator
from functools import reduce
import math

text = open("day16.txt").read()

def hex_to_bin(digit):
    num = int(digit, 16)
    as_bin = [x for x in bin(num)[2:]]
    padding = [0 for _ in range(4-len(as_bin))]
    padding.extend(as_bin)
    return padding

def bin_to_int(b):
    return int("".join([str(i) for i in b]), 2)


digits = [int(i) for x in text for i in hex_to_bin(x)]  

class Packet:
    def __init__(self, version, typeId, length, value=None, sub_packets=None):
        self.version = version
        self.typeId = typeId
        self.length = length
        self.value = value
        self.sub_packets = sub_packets
    
    def __str__(self) -> str:
        return str({'version': self.version, 'typeId': self.typeId, 'length': self.length, 'value': self.value, 'sub_packets': self.sub_packets})

    def __repr__(self) -> str:
        return str({'version': self.version, 'typeId': self.typeId, 'length': self.length, 'value': self.value, 'sub_packets': self.sub_packets})


def parse_by_length(rem, length):
    out = []
    p_len = 0
    while p_len < length:
        p = parse_one(rem)
        rem = rem[p.length:]
        p_len += p.length
        out.append(p)
    assert(p_len == length)
    return out


def parse_by_num(rem, num):
    out = []
    for _ in range(num):
        p = parse_one(rem)
        rem = rem[p.length:]
        out.append(p)
    return out 

def parse_one(rem):
    version = bin_to_int(rem[0:3])
    typeId = bin_to_int(rem[3:6])
    rem = rem[6:]

    if typeId == 4:
        (leng, num) = parse_num(rem)
        return Packet(version, typeId, 6 + leng, value=bin_to_int(num))
    else:
        l_type = rem[0]
        if l_type == 0:
            length = bin_to_int(rem[1:16])
            rem = rem[16:]
            sub_packets = parse_by_length(rem, length)
            return Packet(version, typeId, 6 + 16 + length, sub_packets=sub_packets)
        else:
            count = bin_to_int(rem[1:12])
            rem = rem[12:]
            sub_packets = parse_by_num(rem, count)
            length = 6 + 12 + sum([p.length for p in sub_packets])
            return Packet(version, typeId, length, sub_packets=sub_packets)

def parse_num(rem):
    out = []
    mark = rem[0]
    part = rem[1:5]
    leng = 0
    out.extend(part)
    leng += 5
    while mark == 1:
        rem = rem[5:]
        mark = rem[0]
        part = rem[1:5]
        out.extend(part)
        leng += 5
    return (leng, out)

packet = parse_one(digits)

def sum_version(packet):
    v = packet.version
    if packet.sub_packets:
        v += sum([sum_version(p) for p in packet.sub_packets])
    return v

print("Part 1: ", sum_version(packet))


def evaluate(packet):
    if packet.typeId == 4:
        return packet.value
    if packet.typeId == 0:
        return sum([evaluate(s) for s in packet.sub_packets])
    if packet.typeId == 1:
        return math.prod([evaluate(s) for s in packet.sub_packets])
    if packet.typeId == 2:
        return min([evaluate(s) for s in packet.sub_packets])
    if packet.typeId == 3:
        return max([evaluate(s) for s in packet.sub_packets])
    if packet.typeId == 5:
        sp = [evaluate(s) for s in packet.sub_packets]
        assert(len(sp) == 2)
        return 1 if sp[0] > sp[1] else 0
    if packet.typeId == 6:
        sp = [evaluate(s) for s in packet.sub_packets]
        assert(len(sp) == 2)
        return 1 if sp[0] < sp[1] else 0
    if packet.typeId == 7:
        sp = [evaluate(s) for s in packet.sub_packets]
        assert(len(sp) == 2)
        return 1 if sp[0] == sp[1] else 0


print("Part 2: ", evaluate(packet))