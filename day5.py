import itertools
import operator
from functools import reduce
from collections import Counter

text = open("day5.txt").read()
lines = text.splitlines()

def to_segment(line):
    parts = line.split(' -> ')
    for part in parts:
        p = part.split(',')
        yield (int(p[0]), int(p[1]))

def covered_point(segment):
    (x1, y1) = segment[0]
    (x2, y2) = segment[1]
    if x1 == x2 and y1 == y2:
        yield (x1, y1)
        return

    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            yield (x1, y)
    if y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            yield (x, y1)

segments = [list(to_segment(line)) for line in lines]
points = [point for segment in segments for point in covered_point(segment)]

more_than_2_count = 0

for (p, c) in Counter(points).most_common():
    if c > 1:
        more_than_2_count += 1


print("Part 1: ", more_than_2_count)

def covered_point_p2(segment):
    (x1, y1) = segment[0]
    (x2, y2) = segment[1]
    if x1 == x2 and y1 == y2:
        yield (x1, y1)
        return

    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            yield (x1, y)
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            yield (x, y1)
    else:
        xm = 1 if x2 > x1 else -1
        ym = 1 if y2 > y1 else -1

        for i in range(max(x1, x2) - min(x1, x2) + 1):
            yield (x1 + xm*i, y1 + ym*i)

points = [point for segment in segments for point in covered_point_p2(segment)]

more_than_2_count = 0

for (p, c) in Counter(points).most_common():
    if c > 1:
        more_than_2_count += 1

print("Part 2: ", more_than_2_count)