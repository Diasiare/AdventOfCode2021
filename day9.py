import itertools
import operator
from functools import reduce
import math

text = open("day9.txt").read()
lines = [[int(x) for x in list(s)] for s in text.splitlines()]

def getOrInf(lines, i, j):
    if i < 0 or i >= len(lines) or j < 0:
        return math.inf
    line = lines[i]
    if j >= len(line):
        return math.inf
    return line[j]

risk_level = 0
low_points = []
for i in range(len(lines)):
    line = lines[i]
    for j in range(len(line)):
        center = lines[i][j]
        nearby = [getOrInf(lines, i + 1, j), getOrInf(lines, i - 1, j), getOrInf(lines, i, j + 1), getOrInf(lines, i, j - 1)]
        less = reduce(lambda v, n: v and (center < n),nearby, True)
        if less:
            risk_level += center + 1
            low_points.append((i, j))

print("Part 1: ", risk_level)

def getOrInf2(lines, i, j):
    if i < 0 or i >= len(lines) or j < 0:
        return None
    line = lines[i]
    if j >= len(line):
        return None
    return (line[j], (i, j))

basin_sizes = []
for low_point in low_points:
    frontier = [low_point]
    found = set()
    while len(frontier) > 0:
        current = frontier.pop(0)
        if current in found:
            continue
        found.add(current)
        (i, j) = current
        nearby = [getOrInf2(lines, i + 1, j), getOrInf2(lines, i - 1, j), getOrInf2(lines, i, j + 1), getOrInf2(lines, i, j - 1)]
        nearby = [x for x in nearby if x != None and x[0] < 9]
        for (_, point) in nearby:
            frontier.append(point)
    basin_sizes.append(len(found))

basin_sizes.sort()


print("Part 2: ", basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3])