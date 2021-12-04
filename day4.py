import itertools
import operator
from functools import reduce


def parseBoard(lines):
    lines = lines[1:]
    out = []
    for line in lines:
        out.append([int(x) for x in line.split(" ") if x])
    return Board(out)    

class Board:
    def __init__(self, board):
        self.board = board
        self.marked = set()

    def is_victory(self, i, j):
        all_marked = True
        for i2 in range(len(self.board)):
            all_marked = all_marked and ((i2, j) in self.marked)
        if all_marked:
            return True
        all_marked = True
        for j2 in range(len(self.board[0])):
            all_marked = all_marked and ((i, j2) in self.marked)
        return all_marked



    def mark(self, num):
        won = False
        for i in range(len(self.board)):
            line = self.board[i]
            for j in range(len(line)):
                if line[j] == num:
                    self.marked.add((i, j))
                    won = won or self.is_victory(i, j)
        return won

    def score(self, num):
        total = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (i,j) not in self.marked:
                    total += self.board[i][j]
        return total * num




text = open("day4.txt").read()
lines = text.splitlines()
order = [int(x) for x in lines[0].split(',')]
rest = lines[1:]
boards = [parseBoard(rest[i*6:(i+1)*6]) for i in range(int(len(rest)/6))]

wining_board = None
winning_num = 0
for num in order:
    wining_board = None
    for board in boards:
        won = board.mark(num)
        if won:
            wining_board = board
    if wining_board:
      winning_num = num
      break


print("Part 1: ", wining_board.score(winning_num))

for board in boards:
    board.marked = set()

last_board = None
winning_num = 0
for num in order:
    wining_boards = []
    for board in boards:
        won = board.mark(num)
        if won:
            wining_boards.append(board)
    if len(boards) == 1 and len(wining_boards) == 1:
        last_board = wining_boards[0]
        winning_num = num

    for board in wining_boards:
        boards = [b for b in boards if b != board]

print("Part 2: ", last_board.score(winning_num))