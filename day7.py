import itertools
import operator
from functools import reduce
from collections import Counter
import statistics
import math

text = open("day7.txt").read()
distances = list(map(int, text.split(",")))

mx = max(distances)
mn = min(distances)

fuel_cost = math.inf
for line in range(mn, mx + 1):
    s = sum([abs(line - x) for x in distances])
    fuel_cost = min(fuel_cost, s)

print("Part 1: ", fuel_cost)

def cost(line, x):
    dist = abs(line - x)
    return dist * (dist + 1) / 2

fuel_cost = math.inf
for line in range(mn, mx + 1):
    s = int(sum([cost(line, x) for x in distances]))
    fuel_cost = min(fuel_cost, s)

print("Part 2: ", fuel_cost)
