import itertools
import operator
from functools import reduce
import heapq

text = open("day15.txt").read()

grid = [list(map(int, line)) for line in text.splitlines()]

def neighbours(grid, p):
    ds = [(1 ,0), (-1, 0), (0, 1), (0, -1)]
    for (dy, dx) in ds:
        x = p[1] + dx
        y = p[0] + dy

        if y < 0 or y >= len(grid):
            continue
        line = grid[y]
        if x < 0 or x >= len(line):
            continue
        yield (y, x)

def shortest_path(grid, start, end):
    pqueue = [(0, start)]
    seen = set()

    while len(pqueue) > 0:
        (cost, p) = heapq.heappop(pqueue)
        
        if p == end:
            return cost
        if p in seen:
            continue
        seen.add(p)

        for (y , x) in neighbours(grid, p):
            danger = grid[y][x]
            if (y , x) in seen:
                continue
            heapq.heappush(pqueue, (cost + danger, (y, x)))

end = (len(grid) - 1, len(grid[-1]) - 1)
start = (0, 0)


print("Part 1: ", shortest_path(grid, start, end))

def add_1(line):
    n_line = [n + 1 for n in line]
    return [n if n < 10 else 1 for n in n_line]

n_first_block = []

for line in grid:
    n_line = []
    p_line = line
    n_line.extend(p_line)
    for _ in range(4):
        p_line = add_1(p_line)
        n_line.extend(p_line)
    n_first_block.append(n_line)

n_grid = []
p_block = n_first_block
n_grid.extend(p_block)
for _ in range(4):
    n_block = []
    for line in p_block:
        n_block.append(add_1(line))
    p_block = n_block
    n_grid.extend(p_block)

end = (len(n_grid) - 1, len(n_grid[-1]) - 1)
start = (0, 0)


print("Part 2: ", shortest_path(n_grid, start, end))