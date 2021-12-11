import itertools
import operator
from functools import reduce

text = open("day10.txt").read()
lines = text.splitlines()

bracket_matches = {
    '[': ']',
    '(': ')',
    '{': '}',
    '<': '>'
}

scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

def first_missmatch(line):
    stack = []
    for c in line:
        if c in bracket_matches:
            stack.append(c)
        else:
            pair = stack.pop()
            if c != bracket_matches[pair]:
                return c
    return None

score = 0
uncorruped = []
for line in lines:
    miss = first_missmatch(line)
    if miss:
        score += scores[miss]
    else: 
        uncorruped.append(line)

print("Part 1: ", score)

scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

def calc_stack(line):
    stack = []
    for c in line:
        if c in bracket_matches:
            stack.append(c)
        else:
            pair = stack.pop()
            if c != bracket_matches[pair]:
                return None
    return stack

def calc_score(rem_stack):
    score = 0
    for b in reversed(rem_stack):
        score *= 5
        score += scores[bracket_matches[b]]
    return score

score_per_line = []
for line in uncorruped:
    stack = calc_stack(line)
    score_per_line.append(calc_score(stack))

score_per_line.sort()
mid = int(len(score_per_line) / 2)

print("Part 2: ", score_per_line[mid])