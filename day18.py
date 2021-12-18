import itertools
import operator
import ast
import copy
from functools import reduce

text = open("day18.txt").read().splitlines()
snail_numbers = [ast.literal_eval(s) for s in text]

def is_list(x):
    return type(x) == list

def add_to_rightmost(num, to_add):
    if not is_list(num[1]):
        num[1] += to_add
        return True
    else:
        return add_to_rightmost(num[1], to_add)

def add_to_leftmost(num, to_add):
    if not is_list(num[0]):
        num[0] += to_add
        return True
    else:
        return add_to_leftmost(num[0], to_add)

def maybe_explode_recursive(num, depth):
    if depth == 4:
        assert(not is_list(num[0]))
        assert(not is_list(num[1]))
        return (num[0], num[1])
    
    rv = None
    if is_list(num[0]):
        rv = maybe_explode_recursive(num[0], depth + 1)
    if rv and depth == 3:
        num[0] = 0
    if rv and not rv[1] == None:
        if is_list(num[1]):
            assert(add_to_leftmost(num[1], rv[1]))
        else:
            num[1] += rv[1] 
        return (rv[0], None)
    elif rv:
        return rv
    
    rv = None
    if is_list(num[1]):
        rv = maybe_explode_recursive(num[1], depth + 1)
    
    if rv and depth == 3:
        num[1] = 0
    
    if rv and rv[0]:
        if is_list(num[0]):
            assert(add_to_rightmost(num[0], rv[0]))
        else:
            num[0] += rv[0]
        return (None, rv[1])
    return rv

def maybe_explode(num):
    rv = maybe_explode_recursive(num, 0)
    return not rv == None

def sp(num):
    if num % 2 == 0:
        return [num // 2, num // 2]
    else:
        return [num // 2, (num // 2) + 1]

def maybe_split(num):
    rv = False
    if is_list(num[0]):
        rv = maybe_split(num[0])
    elif num[0] > 9:
        num[0] = sp(num[0])
        rv = True
    
    if not rv:
        if is_list(num[1]):
            rv = maybe_split(num[1])
        elif num[1] > 9:
            num[1] = sp(num[1])
            rv = True
    return rv

def reduce(num):
    did_something = True
    while did_something:
        did_something = maybe_explode(num) or maybe_split(num)

def add(num1, num2):
    num = [num1, num2]
    reduce(num)
    return num

def magnitude(num):
    if not is_list(num):
        return num
    
    return 3*magnitude(num[0]) + 2 * magnitude(num[1])

start = copy.deepcopy(snail_numbers[0])
for num in snail_numbers[1:]:
    start = add(start, copy.deepcopy(num))


print("Part 1: ", magnitude(start))

max_mag = 0

for num1 in snail_numbers:
    for num2 in snail_numbers:
        if num1 == num2:
            continue
        max_mag = max(max_mag, magnitude(add(copy.deepcopy(num1), copy.deepcopy(num2))))


print("Part 2: ", max_mag)