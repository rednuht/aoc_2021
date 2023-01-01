import sys
import itertools


def die():
    while True:
        for i in range(1, 101):
            yield i


def part1(p1_position, p2_position):
    score_1 = 0
    score_2 = 0
    rolls = 0
    d = die()
    while True:
        score = next(d) + next(d) + next(d)
        p1_position = (p1_position + score) % 10
        score_1 += p1_position + 1
        rolls += 3
        if score_1 >= 1000:
            print("part1", score_2 * rolls)
            break
        score = next(d) + next(d) + next(d)
        p2_position = (p2_position + score) % 10
        score_2 += p2_position + 1
        if score_2 >= 1000:
            print("part1", score_1 * rolls)
            break
        rolls += 3


memo = {}


def dirac_play(p1_pos, p2_pos, p1_score, p2_score):
    if p1_score >= 21:
        return 1, 0
    if p2_score >= 21:
        return 0, 1

    key = (p1_pos, p2_pos, p1_score, p2_score)
    if key in memo:
        return memo[key]
    tally = (0, 0)
    for d1, d2, d3 in itertools.product(*[[1, 2, 3]] * 3):
        new_pos = (p1_pos + d1 + d2 + d3) % 10
        p1_tally, p2_tally = dirac_play(p2_pos, new_pos, p2_score, p1_score + new_pos + 1)
        tally = (tally[0] + p2_tally, tally[1] + p1_tally)
    memo[key] = tally
    return tally


def part2(p1_position, p2_position):
    p1_wins, p2_wins = dirac_play(p1_position, p2_position, 0, 0)
    if p1_wins > p2_wins:
        print("part2, p1 wins", p1_wins)
    else:
        print("part2, p2 wins", p2_wins)


def main():
    p1_position = sys.stdin.readline().strip().rsplit(" ", 1)[1]
    p2_position = sys.stdin.readline().strip().rsplit(" ", 1)[1]
    part1(int(p1_position) - 1, int(p2_position) - 1)
    part2(int(p1_position) - 1, int(p2_position) - 1)


if __name__ == '__main__':
    main()
