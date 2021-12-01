import itertools
import operator
from functools import reduce

lines = open("day1in.txt").read()
deeps = [int(x) for x in lines.splitlines()]


count = reduce(lambda count, pair: count + (1 if pair[1] > pair[0] else 0), zip(deeps, deeps[1:]), 0)

print("Part 1: ", count)

sums = [reduce(operator.add, p) for p in zip(deeps, deeps[1:], deeps[2:])]
count = reduce(lambda count, pair: count + (1 if pair[1] > pair[0] else 0), zip(sums, sums[1:]), 0)

print("Part 2: ", count)