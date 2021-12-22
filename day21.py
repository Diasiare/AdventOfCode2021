import itertools
import operator
from functools import reduce
from collections import defaultdict

text = open("day21.txt").read()
lines = text.splitlines()

test_players = [(3,0), (7,0)]
real_players = [(9,0), (1,0)]

players = list(test_players)

def roll_3(next_roll):
    total = 0
    for _ in range(3):
        total += next_roll
        if next_roll == 100:
            next_roll = 1
        else:
            next_roll += 1
    return (total, next_roll)

current_player = 0
roll_count = 0
next_roll = 1
while True:
    position, score = players[current_player]
    rolls, next_roll = roll_3(next_roll)
    position = (position + rolls) % 10
    roll_count += 3
    score += position + 1
    players[current_player] = (position, score)
    
    if score >= 1000:
        break
    current_player = (current_player  + 1) % 2


loosing_score = players[current_player + 1 % 2][1]

print("Part 1: ", loosing_score * roll_count)

counts = defaultdict(int)

for x in range(1, 4):
    for y in range(1, 4):
        for z in range(1, 4):
            counts[x + y + z] += 1

players = list(test_players)

class Position:
    def __init__(self, accum, current_player, next_player):
        self.accum = accum
        self.current_player = current_player
        self.next_player = next_player
    
    def __repr__(self):
        return repr({
            'accum': self.accum,
            'current': self.current_player,
            'next': self.next_player, 
        })

playing_positions = [Position(1, players[0], players[1])]
win_counts = defaultdict(int)

turn = 0
while len(playing_positions) > 0:
    counters = defaultdict(int)
    for position in playing_positions:
        for roll, count in counts.items():
            next_position = (position.current_player[0] + roll) % 10
            next_score = position.current_player[1] + next_position + 1
            pos = ((next_position, next_score), position.next_player)
            counters[pos] += position.accum * count 

    playing_positions = []
    for pos, accum in counters.items():
        current_player = pos[0]
        next_player = pos[1]
        position = Position(accum, next_player, current_player)
        if current_player[1] >= 4:
            win_counts[turn] += accum
        else:
            playing_positions.append(position)
    turn = (turn + 1) % 2

print("Part 2: ", max(win_counts.values()))