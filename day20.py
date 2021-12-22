import itertools
import operator
from functools import reduce

text = open("day20.txt").read()
mask = text.split("\n\n")[0]
image = text.split("\n\n")[1].splitlines()

mask = [c == '#' for c in mask if c != '\n']

lights = [[c == '#' for c in line] for line in image]

combos = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
combos.reverse()
clen = len(combos)

def readNearby(il, jl, lights, default):
    index = 0
    for ci in range(clen):
        id, jd, = combos[ci]
        i = il + id
        j = jl + jd
        is_light = False
        if i < 0 or j < 0 or i >= len(lights) or j >= len(lights[i]):
            is_light = default
        else:
            is_light = lights[i][j]
        if is_light:
            index += 1 << ci
    return index

max_i = len(image)
min_i = -1
max_j = len(image[0])
min_j = -1

def step(lights, default_is_ligth):
    
    new_lights = []

    for i in range(-1, len(lights) + 1):
        line = []
        for j in range(-1, len(lights[0]) + 1):
            line.append(mask[readNearby(i, j, lights, default_is_ligth)])
        new_lights.append(line)
    return new_lights

def pretty_print(lights):

    out = []
    for line in lights:
        l = []
        for c in line:
            l.append('#' if c else '.')
        out.append(''.join(l))
    return "\n".join(out)

def update_def(default, mask):
    return mask[0] if not default else mask[-1]

old_lights = lights

default = False

for _ in range(2):
    lights = step(lights, default)
    default = update_def(default, mask)


print("Part 1: ", len([x for line in lights for x in line if x]))


lights = old_lights
default = False

for _ in range(50):
    lights = step(lights, default)
    default = update_def(default, mask)

print("Part 2: ",  len([x for line in lights for x in line if x]))