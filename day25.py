import itertools
import operator
from functools import reduce

text = open("day25.txt").read()
lines = text.splitlines()

max_i = len(lines)
max_j = max([len(x) for x in lines])

east_facing = set()
south_facing = set()

for i, line in zip(range(len(lines)), lines):
    for j , c in zip(range(len(line)), line):
        if c == '>':
            east_facing.add((i,j))
        elif c == 'v':
            south_facing.add((i,j))

def calc_next(pos, dir, positions):
    next_pos = ((pos[0] + dir[0]) % max_i, (pos[1] + dir[1]) % max_j)
    if next_pos in positions:
        return pos
    return next_pos

def step(east_facing, south_facing):
    positions = east_facing | south_facing
    n_east_facing = set()
    for pos in east_facing:
        n_east_facing.add(calc_next(pos, (0,1), positions))
    positions = n_east_facing | south_facing
    n_south_facing = set()
    for pos in south_facing:
        n_south_facing.add(calc_next(pos, (1,0), positions))
    
    return (n_east_facing, n_south_facing)

count = 0

while True:
    count += 1
    (n_east_facing, n_south_facing) = step(east_facing, south_facing)
    if n_east_facing == east_facing and n_south_facing == south_facing:
        break
    east_facing = n_east_facing
    south_facing = n_south_facing



print("Part 1: ", count)


print("Part 2: ", "incomplete")