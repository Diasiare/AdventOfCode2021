import itertools
import operator
from functools import reduce
import math

test = [(20, 30), (-10, -5)]
real = [(236, 262), (-78, -58)]

input = real

def x_step(pos, vel):
    return (pos + vel, vel - 1 if vel > 0 else (vel + 1 if vel < 0 else 0))

def find_x_options(target):
    t = set(range(min(target), max(target) + 1))
    min_t = min(target)
    max_t = max(target)
    min_v = 0
    max_v = 0
    if min_t > 0 and max_t > 0:
        min_v = 1
        max_v = max_t + 1
    elif min_t < 0 and max_t < 0:
        min_v = -1
        max_v = min_t
    else:
        min_v = min_t
        max_v = max_t
    
    print("x ts", min_v, max_v)

    possibilities = set()
    for start_v in range(min_v, max_v  + 1):
        v = start_v
        pos = 0
        while v != 0:
            (pos, v) = x_step(pos, v)
            if pos in t:
                possibilities.add(start_v)
                break
    print(possibilities)
    return possibilities

def y_step(pos, vel):
    return (pos + vel, vel - 1)

def find_y_options(target):
    t = set(range(min(target), max(target) + 1))
    min_t = min(target)
    max_t = max(target)
    min_v = 0
    max_v = 0
    if min_t > 0 and max_t > 0:
        min_v = 1
        max_v = max_t + 1
    elif min_t < 0 and max_t < 0:
        min_v = min_t - 1
        max_v = abs(min_t) + 1
    else:
        assert(False)
    print("y ts", min_v, max_v)
    print(t)

    possibilities = set()
    for start_v in range(min_v, max_v  + 1):
        v = start_v
        pos = 0
        while pos >= min_t or v >= 0:
            (pos, v) = y_step(pos, v)
            if pos in t:
                possibilities.add(start_v)
                break
    print(possibilities)
    return possibilities
            

x_pos = find_x_options(input[0])
y_pos = find_y_options(input[1])

def find_max_height(x_options, y_options, x_target, y_target):
    x_range = (0, 0)
    if min(x_target) > 0:
        x_range = (0, max(x_target))
    elif max(x_target) < 0:
        x_range = (min(x_target), 0)
    else:
        x_range = (min(x_target), max(x_target))
    min_y = min(y_target)


    x_target = set(range(min(x_target), max(x_target) + 1))
    y_target = set(range(min(y_target), max(y_target) + 1))


    true_max_height = -math.inf
    for (start_x, start_y) in itertools.product(x_options, y_options):
        x_pos = 0
        y_pos = 0
        y_vel = start_y
        x_vel = start_x
        max_height = -math.inf
        while x_pos >= x_range[0] and x_pos <= x_range[1] and (y_pos >= min_y or y_vel > 0):
            (x_pos, x_vel) = x_step(x_pos, x_vel)
            (y_pos, y_vel) = y_step(y_pos, y_vel)

            max_height = max(y_pos, max_height)

            if x_pos in x_target and y_pos in y_target:
                while y_vel > 0:
                    (y_pos, y_vel) = y_step(y_pos, y_vel)
                    max_height = max(y_pos, max_height)
                true_max_height = max(max_height, true_max_height)
    return true_max_height


print("Part 1: ", find_max_height(x_pos, y_pos, input[0], input[1]))


def count_pos(x_options, y_options, x_target, y_target):
    x_range = (0, 0)
    if min(x_target) > 0:
        x_range = (0, max(x_target))
    elif max(x_target) < 0:
        x_range = (min(x_target), 0)
    else:
        x_range = (min(x_target), max(x_target))
    min_y = min(y_target)


    x_target = set(range(min(x_target), max(x_target) + 1))
    y_target = set(range(min(y_target), max(y_target) + 1))


    count  = 0
    for (start_x, start_y) in itertools.product(x_options, y_options):
        x_pos = 0
        y_pos = 0
        y_vel = start_y
        x_vel = start_x
        while x_pos >= x_range[0] and x_pos <= x_range[1] and (y_pos >= min_y or y_vel > 0):
            (x_pos, x_vel) = x_step(x_pos, x_vel)
            (y_pos, y_vel) = y_step(y_pos, y_vel)

            if x_pos in x_target and y_pos in y_target:
                count += 1
                break
    return count

print("Part 2: ", count_pos(x_pos, y_pos, input[0], input[1]))