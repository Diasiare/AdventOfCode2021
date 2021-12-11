import itertools
import operator
from functools import reduce

text = open("day11.txt").read()
lines = text.splitlines()
lines = [list(map(int, line)) for line in lines]

base_lines = [[c for c in line] for line in lines]

coords = [(i, j) for i in range(len(lines)) for j in range(len(lines[i]))]


def getOrNone(lines, i, j):
    if i < 0 or i >= len(lines) or j < 0:
        return None
    line = lines[i]
    if j >= len(line):
        return None
    return (i, j)

def neighbours(i, j):
    ns = [1, 0, -1]
    for id in ns:
        for jd in ns:
            if id == 0 and jd == 0:
                continue
            yield (i + id, j + jd)

def step(lines):
    flashed = set()
    for coord in coords:
        lines[coord[0]][coord[1]] += 1
        if lines[coord[0]][coord[1]] == 10:
            flashed.add(coord)
    
    queue = [x for x in flashed]
    while len(queue) > 0:
        (i, j) = queue.pop(0)
        ns = neighbours(i, j)
        ns = [getOrNone(lines, i2, j2) for (i2, j2) in ns]
        ns = [x for x in ns if x and x not in flashed]

        for coord in ns:
            lines[coord[0]][coord[1]] += 1
            if lines[coord[0]][coord[1]] == 10:
                flashed.add(coord)
                queue.append(coord)
    num_flashed = len(flashed)
    for coord in flashed:
        lines[coord[0]][coord[1]] = 0
    return num_flashed

accum = 0
for i in range(100):
    accum += step(lines)



print("Part 1: ", accum)

lines = base_lines
num_to_flash = sum([len(line) for line in lines])
itt = 0
flashed = 0
while flashed < num_to_flash:
    flashed = step(lines)
    itt += 1

print("Part 2: ", itt)