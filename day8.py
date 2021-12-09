import itertools
import operator
from functools import reduce

text = open("day8.txt").read()
lines = text.splitlines()

second_parts = [line.split(" | ")[1] for line in lines]
first_parts = [line.split(" | ")[0].split(" ") for line in lines]
nums = [len(n) for part in second_parts for n in part.split(" ")]
c = len(list(filter(lambda n: n < 5 or n == 7, nums)))

print("Part 1: ", c)

base_numbers = {
	0: "abcefg",
	1: "cf",
	2: "acdeg",
	3: "acdfg",
	4: "bcdf",
	5: "abdfg",
	6: "abdefg",
	7: "acf",
	8: "abcdefg",
	9: "abcdfg",
}
base_number_array = [frozenset(s) for s in base_numbers.values()]
base_number_set = frozenset(base_number_array)
letters = base_numbers[8]

def all_mappings(s, index, excluded_out):
	if index >= len(s):
		yield []
	else:
		for c in s:
			if c not in excluded_out:
				for m in all_mappings(s, index + 1, excluded_out | frozenset([c])):
					m.append((s[index], c))
					yield m

mappings = list(all_mappings(letters, 0, frozenset()))


def mapping_to_map(mapping):
	m = {}
	for (f, to) in mapping:
		m[f] = to
	return m
mappings = [mapping_to_map(m) for m in mappings]

def mapping_fits(mapping, line):

	for n in line:
		s = set()
		for c in n:
			s.add(mapping[c])
		if s not in base_number_set:
			return False
	return True

def calc_num(mapping, num):
	s = set()
	for c in num:
		s.add(mapping[c])
	return base_number_array.index(s)

def calc_nums(mapping, second_part):
	mult = 1000
	accum = 0
	for n in map(lambda num: calc_num(mapping, num), second_part):
		accum += mult * n
		mult = mult / 10
	return accum

accum = 0
for (f,s) in zip(first_parts, second_parts):
	for mapping in mappings:
		if mapping_fits(mapping, f):
			accum += calc_nums(mapping, s.split(" "))
			break


print("Part 2: ", int(accum))