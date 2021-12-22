import itertools
import operator
from functools import reduce

text = open("day22.txt").read()
lines = text.splitlines()

cuts = []
for line in lines:
    line = line.replace("x=", "").replace("z=", "").replace("y=", "")
    command = line.split(" ")[0]
    ranges = line.split(" ")[1].split(",")
    f_ranges = []
    for range in ranges:
        vs = list(map(int, range.split("..")))
        f_ranges.append((min(vs), max(vs) + 1))
    cuts.append((command == "on", f_ranges))

# rv (before, after)
def cut_cube_by_plane(cube, dir, val):
    c_dir = cube[dir]
    if c_dir[1] <= val:
        return (cube, None)
    elif c_dir[0] >= val:
        return (None, cube)
    
    before = list(cube)
    after = list(cube)

    before[dir] = (c_dir[0], val)
    after[dir] = (val, c_dir[1])
    
    return (before, after)

# (before, after) -> (inside, out)
def d_low(p):
    return (p[1], p[0])
def d_hi(p):
    return p

# plane = (val, dir, trans)
def decompose_to_planes(cube):
    return [(cube[0][0], 0, d_low), (cube[0][1], 0, d_hi), (cube[1][0], 1, d_low), (cube[1][1], 1, d_hi), (cube[2][0], 2, d_low), (cube[2][1], 2, d_hi)]

# cube, cube -> (parts of c1 outside c2, rest)
def cut_cube_by_cube(cube1, cube2):
    inside = [cube1]
    outside = []

    for (val, dir, trans) in decompose_to_planes(cube2):
        if len(inside) == 0:
            return ([cube1], [])
        for c in inside:
            ins, out = trans(cut_cube_by_plane(c, dir, val))
            n_ins = []
            if ins:
                n_ins.append(ins)
            if out:
                outside.append(out)
        inside = n_ins
    return (outside, inside)

def do_operation(is_on, cubes, op_cube):

    new_cubes = None
    if is_on:
        new_cubes = list(cubes)
        op_cube_rem = [op_cube]
        for cube in cubes:
            n_rem = []
            for rem in op_cube_rem:
                (to_add, _) = cut_cube_by_cube(rem, cube)
                n_rem.extend(to_add)
            op_cube_rem = n_rem
        new_cubes.extend(op_cube_rem)
        return new_cubes
    
    # Is off
    new_cubes = []
    for cube in cubes:
        (rem, _) = cut_cube_by_cube(cube, op_cube)
        new_cubes.extend(rem)
    return new_cubes

def volume(cube):
    diffs = map(lambda p: p[1] - p[0], cube)
    return reduce(operator.mul, diffs)

containmen_cube = [(-50, 51),(-50, 51),(-50, 51)]

on_cubes = []
for op, cube in cuts:
    (_, in_cont) = cut_cube_by_cube(cube, containmen_cube)
    if len(in_cont) > 0:
        assert(len(in_cont) == 1)
        on_cubes = do_operation(op, on_cubes, in_cont[0])

print("Part 1: ", reduce(operator.add, map(volume, on_cubes)))

on_cubes = []
for op, cube in cuts:
    on_cubes = do_operation(op, on_cubes, cube)


print("Part 2: ", reduce(operator.add, map(volume, on_cubes)))