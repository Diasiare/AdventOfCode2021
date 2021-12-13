import itertools
import operator
from functools import reduce

text = open("day13.txt").read()
dots = text.split("\n\n")[0].splitlines()
folds = text.split("\n\n")[1].splitlines()

dots = [dot.split(",") for dot in dots]
dots = [(int(dot[0]), int(dot[1])) for dot in dots]

folds = [fold.replace("fold along ", "").split("=") for fold in folds]
folds = [(fold[0], int(fold[1])) for fold in folds]

cdots = set(dots)

def fold(dots, fold):
    new_set = set()
    for dot in dots:
        if fold[0] == "y":
            new_y = dot[1] if dot[1] < fold[1] else fold[1] - abs(dot[1] - fold[1])
            new_set.add((dot[0], new_y))
        else:
            new_x = dot[0] if dot[0] < fold[1] else fold[1] - abs(dot[0] - fold[1])
            new_set.add((new_x, dot[1]))

    if fold[0] == "y":
        min_y = min([dot[1] for dot in new_set])
        if min_y < 0:
            new_set = set([(dot[0], dot[1] + abs(min_y)) for dot in new_set])
    else:
        min_y = min([dot[0] for dot in new_set])
        if min_y < 0:
            new_set = set([(dot[0] + abs(min_y), dot[1]) for dot in new_set])
    return new_set

def print_dots(dots):
    max_x = max([dot[0] for dot in dots])
    max_y = max([dot[1] for dot in dots])

    line = [" "] * (max_x + 1)
    lines = []
    
    for i in range(max_y + 1):
        lines.append(list(line))

    for (x, y) in dots:
        lines[y][x] = "#"
    
    l = "\n"
    for line in lines:
        l += "".join(line)
        l += "\n"
    return l 

cdots = fold(cdots, folds[0])

print("Part 1: ", len(cdots))

for foldc in folds[1:]:
    cdots = fold(cdots, foldc)

print("Part 2: ", print_dots(cdots))