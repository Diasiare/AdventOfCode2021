import itertools
import operator
from functools import reduce

text = open("day12.txt").read()
lines = text.splitlines()

edges = {}
for line in lines:
    (s, e) = line.split('-')
    if s not in edges:
        edges[s] = []
    edges[s].append(e)
    if e not in edges:
        edges[e] = []
    edges[e].append(s)

def is_big_cave(s):
    return s.isupper()

paths = [["start"]]
end_paths = []
while len(paths) > 0:
    path = paths.pop(0)
    es = edges[path[-1]]
    for e in es:
        if not is_big_cave(e) and e in path:
            continue
        pc = list(path)
        pc.append(e)
        if e == "end":
            end_paths.append(pc)
        else:
            paths.append(pc)


print("Part 1: ", len(end_paths))

class Path:
    def __init__(self):
        self.path = []
        self.small_visited = set()
        self.has_used_small_exeption = False

    def clone(self):
        path = Path()
        path.path = list(self.path)
        path.small_visited = set(self.small_visited)
        path.has_used_small_exeption = self.has_used_small_exeption
        return path
    
    def can_append(self, edge):
        if is_big_cave(edge):
            return True
        elif edge == "start":
            return False
        return not (edge in self.small_visited and self.has_used_small_exeption)

    def append(self, edge):
        self.path.append(edge)
        if not is_big_cave(edge) and edge in self.small_visited:
            self.has_used_small_exeption = True
        if not is_big_cave(edge):
            self.small_visited.add(edge)
        return self
        


start_path = Path()
start_path.append("start")
paths = [start_path]
end_paths = []
while len(paths) > 0:
    path = paths.pop(0)
    es = edges[path.path[-1]]
    for e in es:
        if not path.can_append(e):
            continue
        pc = path.clone()
        pc.append(e)
        if e == "end":
            end_paths.append(pc)
        else:
            paths.append(pc)


print("Part 2: ", len(end_paths))