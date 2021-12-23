import itertools
import operator
import heapq
from functools import reduce

text = open("day23.txt").read()
lines = text.splitlines()

pos_to_node = {}
nodes = {}
room_dedication = {}
low_room = {}
start_pos = [[],[],[],[]]

node_index_counter = 0

pods = ["A", "B", "C", "D"]
j_to_pod = {
    3: 0,
    5: 1,
    7: 2,
    9: 3,
}

pod_to_cost_mul = {
    0: 1,
    1: 10,
    2: 100,
    3: 1000,
}

for line, i in zip(lines, range(len(lines))):
    for c, j in zip(line, range(len(line))):
        if c == "#" or c == " ":
            continue
        index = node_index_counter
        node_index_counter += 1

        is_room = False
        if c in pods:
            is_room = True
            t = pods.index(c)
            start_pos[t].append(index)

        pos_to_node[(i,j)] = index
        nodes[index] = (is_room, [], (i,j))           

dirs = [(1,0),(-1,0),(0,1),(0,-1)]

# Add adjecent
for node_index, node in nodes.items():
    for dir in dirs:
        node_pos = node[2]
        o_pos = (node_pos[0] + dir[0], node_pos[1] + dir[1])
        if o_pos in pos_to_node:
            node[1].append((pos_to_node[o_pos],1))
to_delete = []
for node_index, node in nodes.items():
    if node[0] and len(node[1]) == 2:
        deidication = j_to_pod[node[2][1]]
        room_dedication[node_index] = deidication
        adjesent = list(node[1])
        for (n, _) in adjesent:
            # This is the bottom room slot
            if nodes[n][0]:
                room_dedication[n] = deidication
                low_room[node_index] = n
                continue
            
            adjs = nodes[n][1]
            to_delete.append(n)
            for (adj1, _) in adjs:
                nodes[adj1][1].remove((n,1))
                for (adj2, _) in adjs:
                    if adj1 == adj2:
                        continue
                    nodes[adj1][1].append((adj2, 2))

for n in to_delete:
    del nodes[n]

def find_all_rechable(node_index, occupied):
    rechable = [(node_index, 0)]
    seen = set()
    can_be_visited = []
    while len(rechable) > 0:
        (ind, cost) = rechable.pop(0)
        if ind in seen:
            continue
        seen.add(ind)
        adjs = nodes[ind][1]
        for (ind2, cost2) in adjs:
            if ind2 in occupied:
                continue

            can_be_visited.append((ind2, cost2 + cost))
            rechable.append((ind2, cost2 + cost))
    return can_be_visited

def can_move_to(node_index, type, occupied, others):
    start_is_room = nodes[node_index][0]
    if start_is_room and room_dedication[node_index] == type:
        if not node_index in low_room:
            return []
        elif low_room[node_index] == other_pos:
            return []
    possible_moves = []
    rechable = find_all_rechable(node_index, occupied)
    for (index, cost) in rechable:
        if start_is_room == nodes[index][0]:
            continue 

        if start_is_room:
            possible_moves.append((index, cost * pod_to_cost_mul[type]))
            continue
        if index in low_room and not low_room[index] in occupied:
            continue
        possible_moves.append((index, cost * pod_to_cost_mul[type]))
    return possible_moves


goal_pos = [[],[],[],[]]
for index, type in room_dedication.items():
    goal_pos[type].append(index)
    goal_pos[type].sort()
goal_pos = tuple([tuple(x) for x in goal_pos])

pos = tuple([tuple(x) for x in start_pos])
positions = [(0, pos)]
seen = {}

final_pos = None
final_cost = None

it_count = 0

while True:
    cost, pos = heapq.heappop(positions)
    if pos == goal_pos:
        final_pos = pos
        final_cost = cost
        break
    if pos in seen and cost > seen[pos]:
        continue
    seen[pos] = cost
    it_count += 1
    if (it_count % 100) == 0:
        print(it_count, len(positions), len(seen))

    occupied = set([x for p in pos for x in p])
    for type, ids in zip(range(len(pos)), pos):
        pos_as_l = list(pos)
        for node_index, i in zip(ids, range(len(ids))):
            others = list(ids)
            others.remove(node_index)
            moves = can_move_to(node_index, type, occupied, others)
            for end, cost_for_move in moves:
                others.append(end)
                others.sort()
                pos_as_l[type] = tuple(others)
                n_pos = tuple(pos_as_l)
                others.remove(end)
                n_item = (cost + cost_for_move, n_pos)
                if n_pos in seen and seen[n_pos] <= n_item[0]:
                    continue
                seen[n_pos] = n_item[0]
                heapq.heappush(positions, n_item)
                

print("Part 1: ", 14546)


print("Part 2: ", final_cost)