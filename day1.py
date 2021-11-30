import itertools
import operator
from functools import reduce

lines = open("day1in.txt").read()
numbers = [int(x) for x in lines.splitlines()]

pair = next(filter(lambda a: reduce(operator.add, a) == 2020, itertools.combinations(numbers, 3)))
print(reduce(lambda x,y: x*y, pair))