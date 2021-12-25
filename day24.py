import itertools
import operator
from functools import reduce

text = open("day24.txt").read()
chunks = text.split('inp w\n')
chunks = chunks[1:]
chunks = [[x.split(' ') for x in c.splitlines()] for c in chunks]

base_state = {
    'w': 0,
    'x': 0,
    'y': 0,
    'z': 0,
}

def do_instruction(parts, state):
    ins = parts[0]
    dest = parts[1]
    num = state[parts[2]] if parts[2] in state else int(parts[2])

    if ins == 'add':
        state[dest] = state[dest] + num
    elif ins == 'mul':
        state[dest] = state[dest] * num
    elif ins == 'div':
        if num == 0:
            return None
        state[dest] = state[dest] // num
    elif ins == 'mod':
        if state[dest] < 0 or num <=0:
            return None
        state[dest] = state[dest] % num
    elif ins == 'eql':
        state[dest] = int(state[dest] == num)
    else:
        assert(False)
    
    return state

def find_possible_zs(chunk, zs):
    for z in zs:
        for inp in range(1,10):
            state = dict(base_state)
            state['z'] = z[0]
            state['w'] = inp
            for ins in chunk:
                state = do_instruction(ins, state)
                if not state:
                    break
            if state:
                n = list(z[1])
                n.append(inp)
                yield (state['z'], n)

start_z = (0, [])

zs = [start_z]

def unique_z(zs):
    seen = set()
    for z in zs:
        if z[0] in seen:
            continue
        seen.add(z[0])
        yield z

def is_0(zs):
    for z in zs:
        if z[0] == 0:
            yield ''.join([str(x) for x in z[1]])

for i in range(len(chunks)):
    zs = find_possible_zs(chunks[i], zs)
    zs = list(unique_z(zs))
    print(len(zs))

for z0 in is_0(zs):
    print(i, z0)

print("Part 1: ", list(is_0(zs))[0])


print("Part 2: ", "incomplete")

