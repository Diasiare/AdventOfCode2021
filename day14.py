from collections import defaultdict
import itertools
import operator
from functools import reduce
from typing import Counter

text = open("day14.txt").read()
start = text.split("\n\n")[0]
rule_lines = text.split("\n\n")[1].splitlines()

rules = {}
for rule_line in rule_lines:
    parts = rule_line.split(" -> ")
    rules[(parts[0][0], parts[0][1])] = parts[1]

def step(line, rules):
    out = []
    out.append(line[0])
    for p in zip(line, line[1:]):
        if p in rules:
            out.append(rules[p])
        out.append(p[1])
    return out

line = start

for _ in range(10):
    line = step(line, rules)

c = Counter(line)
counts = c.most_common()

print("Part 1: ", counts[0][1] - counts[-1][1])


line = start

layer = {}


def depth_count(r_depth, p, rules):
    if r_depth == 0:
        return Counter([p[0]])
    
    if p in rules:
        mid = rules[p]
        c1 = depth_count(r_depth - 1, (p[0], mid), rules)
        c1.update(depth_count(r_depth - 1, (mid, p[1]), rules))
        return c1
    else:
        return Counter([p[0]])

def count_steps(prev_layer, rules):
    layer = {}
    for (rule, mid) in rules.items():
        c = Counter()
        p1 = (rule[0], mid)
        p2 = (mid, rule[1])
        if p1 in prev_layer:
            c.update(prev_layer[p1])
        else:
            c.update([p1[0]])
        if p2 in prev_layer:
            c.update(prev_layer[p2])
        else:
            c.update([p2[0]])
        layer[rule] = c
    return layer



for _ in range(40):
    layer = count_steps(layer, rules)

c = Counter()
c.update(Counter([line[-1]]))
for p in zip(line, line[1:]):
    if p in layer:
        c.update(layer[p])
    else:
        c.update([p[0]])

counts = c.most_common()

print("Part 2: ", counts[0][1] - counts[-1][1])