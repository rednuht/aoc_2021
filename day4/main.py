import sys
from typing import List


class Board:
    def __init__(self, raw: List[List[int]]):
        self.rows = raw
        self.cols = list(zip(*raw[::-1]))
        self.sum = sum(d for r in self.rows for d in r)
        self.marked = set()
        self.played = set()
        self.last_played_number: int = -1

    def play_number(self, number: int):
        self.played.add(number)
        self.last_played_number = number
        for row in self.rows:
            for r in row:
                if r not in self.marked and r == number:
                    self.marked.add(number)

    def sum_unmarked(self) -> int:
        return self.sum - sum(self.marked)

    def check_win(self) -> bool:
        win = False
        for i in range(5):
            # check i:th row
            if set(self.rows[i]).issubset(self.played):
                win = True
                break
            # check i:th column
            if set(self.cols[i]).issubset(self.played):
                win = True
                break

        return win

    def __str__(self):
        s = ""
        for row in self.rows:
            s += " ".join([str(d) for d in row])
            s += "\n"
        return s

    def __repr__(self):
        return self.__str__()


def main():
    numbers = [int(d) for d in sys.stdin.readline().strip().split(",")]
    boards: List[Board] = []
    # skip empty line after numbers
    sys.stdin.readline()
    for line in sys.stdin:
        # skip empty lines
        if line.strip() == "":
            continue
        # read five lines
        raw = []
        for _ in range(5):
            raw.append(
                [int(d) for d in line.strip().split()]
            )
            line = sys.stdin.readline()
        boards.append(Board(raw))

    winning_boards = []
    for number in numbers:
        for board in boards:
            if board in winning_boards:
                # board has already won so don't need to check it
                continue
            board.play_number(number)
            if board.check_win():
                winning_boards.append(board)

    first_board = winning_boards[0]
    last_board = winning_boards[-1]
    print("part1", first_board.sum_unmarked() * first_board.last_played_number)
    print("part2", last_board.sum_unmarked() * last_board.last_played_number)


if __name__ == '__main__':
    main()
