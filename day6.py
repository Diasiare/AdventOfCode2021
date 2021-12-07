import itertools
import operator
from functools import reduce
from collections import Counter

text = open("day6.txt").read()
start_ages = map(int, text.split(","))

counts = {}
m = 0
for age in start_ages:
    if age not in counts:
        counts[age] = 0
    counts[age] += 1
    m = max(m, age)

left_to_spawn = []

for a in range(m + 1):
    if a not in counts:
        left_to_spawn.append(0)
    else:
        left_to_spawn.append(counts[a])

for day in range(80):
    today = left_to_spawn.pop(0)
    if len(left_to_spawn) < 7:
        left_to_spawn.append(today)
    else: 
        left_to_spawn[6] += today
    
    if len(left_to_spawn) < 8:
        left_to_spawn.append(0)
    
    if len(left_to_spawn) < 9:
        left_to_spawn.append(today)

total = sum(left_to_spawn)

print("Part 1: ", total)

for day in range(256 - 80):
    today = left_to_spawn.pop(0)
    if len(left_to_spawn) < 7:
        left_to_spawn.append(today)
    else: 
        left_to_spawn[6] += today
    
    if len(left_to_spawn) < 8:
        left_to_spawn.append(0)
    
    if len(left_to_spawn) < 9:
        left_to_spawn.append(today)

total = sum(left_to_spawn)

print("Part 2: ", total)