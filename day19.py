import itertools
import operator
from functools import reduce

text = open("day19.txt").read()
scanner_text = text.split("\n\n")

scanners =  []
for st in scanner_text:
    lines = st.splitlines()
    beacons = []
    for beacon in lines[1:]:
        parts = beacon.split(",")
        beacons.append((int(parts[0]),int(parts[1]),int(parts[2])))
    scanners.append(set(beacons))


def rotate_90_in_z(beacon):
    (x, y, z) = beacon
    return (-y, x, z)

def rotate_90_in_x(beacon):
    (x, y, z) = beacon
    return (x, -z, y)

def rotate_90_in_y(beacon):
    (x, y, z) = beacon
    return (z, y, -x)

def call_x(x, b, f):
    out = b
    for _ in range(x):
        out = f(out)
    return out

def all_permutations(beacons):
    sets = []
    for x in range(4):
        for y in range(4):
            for z in range(4):
                rotation = frozenset([call_x(x, call_x(y, call_x(z, b, rotate_90_in_z), rotate_90_in_y), rotate_90_in_x) for b in beacons])
                sets.append(({'x': x, 'y': y, 'z': z}, rotation))
    
    seen = set()
    out = []
    for s in sets:
        if s[1] in seen:
            continue
        seen.add(s[1])
        out.append(s)
    return out

def normailize_to_beacon(b, beacons):   
    (bx, by, bz) = b
    return frozenset([(x - bx, y - by, z - bz) for (x, y, z) in beacons])

def undo_rotations(p, rotations):
    out = p
    for rotation in rotations:
        out = call_x(4 - rotation['z'], call_x(4 - rotation['y'], call_x(4 - rotation['x'], out, rotate_90_in_x), rotate_90_in_y), rotate_90_in_z)
    return out

def do_rotations(p, rotations):
    out = p
    for rotation in rotations:
        out = call_x(4 - rotation['x'], call_x(4 - rotation['y'], call_x(4 - rotation['z'], out, rotate_90_in_z), rotate_90_in_y), rotate_90_in_x)
    return out

scanners = [all_permutations(s) for s in scanners]

scanner_positions = {0 : ((0,0,0), [{'x': 0, 'y': 0, 'z': 0}])}
checked = set((0 , 0))


while len(scanner_positions) != len(scanners):
    print("Solved", len(scanner_positions))
    for first in range(len(scanners)):
        for second in range(len(scanners)):
            if first not in scanner_positions or second in scanner_positions or (first, second) in checked:
                continue
            checked.add((first, second))
            sbs = scanners[second][0][1]
            found = False

            for permutation in scanners[first]:
                fbs = permutation[1]
                for fb in fbs:
                    fbsn = normailize_to_beacon(fb, fbs)
                    for sb in sbs:
                        sbsn = normailize_to_beacon(sb, sbs)
                        intersection = sbsn & fbsn
                        if len(intersection) >= 12:
                            found = True
                            in_perm = (fb[0] - sb[0], fb[1] - sb[1], fb[2] - sb[2])
                            unrotated_relative_to_first = undo_rotations(in_perm, [permutation[0]])
                            first_pos = scanner_positions[first]
                            rot_to_0 = undo_rotations(unrotated_relative_to_first, first_pos[1])
                            fp = first_pos[0]
                            first_perm = first_pos

                            perm =  [permutation[0]]
                            perm.extend(first_pos[1]) 

                            relative_to_0 = (rot_to_0[0] + fp[0], rot_to_0[1] + fp[1], rot_to_0[2] + fp[2])

                            scanner_positions[second] = (relative_to_0, perm)
                            break
                if found:
                    break
            if found:
                    break


beacons = set()
for (scanner, (pos, rots)) in scanner_positions.items():
    bs = scanners[scanner][0][1]
    for b in bs:
        rb = undo_rotations(b, rots)
        beacons.add((rb[0] + pos[0], rb[1] + pos[1], rb[2] + pos[2]))


print("Part 1: ", len(beacons))


max_dist = 0
for (_, (pos, _)) in scanner_positions.items():
    for (_, (pos2, _)) in scanner_positions.items():
        dist = abs(pos[0] - pos2[0]) + abs(pos[1] - pos2[1]) + abs(pos[2] - pos2[2])
        max_dist = max(max_dist, dist)


print("Part 2: ", max_dist)