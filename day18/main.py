import sys
import math
import copy
import itertools
from typing import List, Dict


def parse(numbers, d):
    nums = []

    for n in numbers:
        if isinstance(n, list):
            res = parse(n, d + 1)
            nums += res
        else:
            nums.append({
                "val": n,
                "depth": d
            })
    return nums


def reduce(numbers: List[Dict]):
    while True:
        i, _n = next(((i, n) for i, n in enumerate(numbers) if n["depth"] == 4), (-1, None))
        if i != -1:
            # need to explode
            if i == 0:
                # right
                numbers[i + 2]["val"] += numbers[i + 1]["val"]
                numbers = [{"val": 0, "depth": numbers[i]["depth"] - 1}] + numbers[i + 2:]
                continue
            elif 0 < i + 3 <= len(numbers):
                # both
                numbers[i - 1]["val"] += numbers[i]["val"]
                numbers[i + 2]["val"] += numbers[i + 1]["val"]
                numbers = numbers[0:i] + [{"val": 0, "depth": numbers[i]["depth"] - 1}] + numbers[i + 2:]
                continue
            elif i + 2 <= len(numbers):
                # left
                numbers[i - 1]["val"] += numbers[i]["val"]
                numbers = numbers[0:i] + [{"val": 0, "depth": numbers[i]["depth"] - 1}]
                continue

        i, n = next(((i, n) for i, n in enumerate(numbers) if n["val"] >= 10), (-1, None))
        if i != -1:
            # need to split
            lower = math.floor(n["val"] / 2)
            higher = math.ceil(n["val"] / 2)
            depth = n["depth"]
            if i + 1 < len(numbers):
                numbers = numbers[0:i] + [{"val": lower, "depth": depth + 1},
                                          {"val": higher, "depth": depth + 1}] + numbers[i + 1:]
            else:
                numbers = numbers[0:i] + [{"val": lower, "depth": depth + 1},
                                          {"val": higher, "depth": depth + 1}]
            continue

        break

    return numbers


def increase_depth(numbers):
    return [
        {
            "val": e["val"],
            "depth": e["depth"] + 1
        }
        for e in numbers
    ]


def magnitude(numbers):
    while len(numbers) > 1:
        max_i = 0
        max_depth = 0
        for i, n in enumerate(numbers):
            if n["depth"] > max_depth:
                max_depth = n["depth"]
                max_i = i

        numbers = numbers[0:max_i] + \
                  [{"val": numbers[max_i]["val"] * 3 + numbers[max_i + 1]["val"] * 2,
                    "depth": numbers[max_i]["depth"] - 1}] + numbers[max_i + 2:]

    return numbers[0]


def do_snailfish_sum(numbers):
    snailfish_sum = numbers[0]
    for n in numbers[1:]:
        snailfish_sum = increase_depth(snailfish_sum) + increase_depth(n)
        i = 0
        while True:
            before = copy.deepcopy(snailfish_sum)
            after = reduce(before)
            snailfish_sum = after
            if before == after:
                break
            i += 1

    res = magnitude(
        snailfish_sum
    )
    return res


def main():
    numbers = []
    for line in sys.stdin:
        numbers.append(parse(eval(line), 0))

    numbers_orig = copy.deepcopy(numbers)
    part1 = do_snailfish_sum(numbers)["val"]

    part2 = max(
        do_snailfish_sum(copy.deepcopy(p))["val"]
        for pair in itertools.combinations(numbers_orig, 2)
        for p in [pair, pair[::-1]]
    )

    print("part1", part1)
    print("part2", part2)


if __name__ == '__main__':
    main()
