import itertools
import operator
from functools import reduce

text = open("day3.txt").read()
lines = text.splitlines()

def count_ones(lines, index):
    one_count = 0
    for line in lines:
        c = line[index]
        one_count = one_count + (1 if c == "1" else 0)
    return one_count
def bin_to_dec(nums):
    mul = 1
    sum = 0
    nums.reverse()
    for num in nums:
        sum += mul *num
        mul *= 2
    nums.reverse()
    return sum

most_common = []
for j in range(len(lines[0])):
    one_count = count_ones(lines, j)
    to_append = 1 if one_count > len(lines) / 2 else 0
    most_common.append(to_append)

omega = bin_to_dec(most_common)
epsilon = bin_to_dec([abs(x-1) for x in most_common])

print("Part 1: ", omega*epsilon)

def oxygen(lines, index):
    if len(lines) == 1:
        return lines[0]
    one_count = count_ones(lines,index)
    filter_on = "1" if one_count >= len(lines)/2 else "0"
    return oxygen([l for l in lines if l[index] == filter_on], index + 1)

def co2(lines, index):
    if len(lines) == 1:
        return lines[0]
    one_count = count_ones(lines,index)
    filter_on = "0" if one_count >= len(lines)/2 else "1"
    return co2([l for l in lines if l[index] == filter_on], index + 1)

oxygen_num = int(oxygen(lines, 0), base=2)
co2_num = int(co2(lines, 0), base=2)

print("Part 2: ", oxygen_num * co2_num)