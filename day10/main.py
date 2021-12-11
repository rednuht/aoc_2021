import sys
from collections import deque

incorrect_bracket_points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

missing_bracket_points = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

brackets = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}


def main():
    score = 0
    incomplete_scores = []
    for line in sys.stdin:
        chars = list(line.strip())
        stack = deque()
        is_corrupted = False
        for c in chars:
            if c in brackets.keys():
                stack.appendleft(c)
            else:
                matching = stack.popleft()
                if brackets[matching] != c:
                    score += incorrect_bracket_points[c]
                    is_corrupted = True

        if not is_corrupted:
            missing = [brackets[m] for m in stack]
            s = 0
            for m in missing:
                s *= 5
                s += missing_bracket_points[m]
            incomplete_scores.append(s)

    incomplete_scores.sort()
    print("part1", score)
    print("part2", incomplete_scores[int(len(incomplete_scores) / 2)])


if __name__ == '__main__':
    main()
