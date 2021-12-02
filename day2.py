import itertools
import operator
from functools import reduce

text = open("day2.txt").read()
commands = [(x[0], int(x[1])) for x in map(lambda line: line.split(' '), text.splitlines())]


depth = 0
distance = 0
for command in commands:
    if command[0] == "forward":
        distance = distance + command[1]
    elif command[0] == "up":
        depth = depth - command[1]
    elif command[0] == "down":
        depth = depth + command[1]

print("Part 1: ", depth * distance)

depth = 0
distance = 0
aim = 0
for command in commands:
    if command[0] == "forward":
        distance = distance + command[1]
        depth = depth + command[1]*aim
    elif command[0] == "up":
        aim = aim - command[1]
    elif command[0] == "down":
        aim = aim + command[1]

print("Part 2: ", depth * distance)