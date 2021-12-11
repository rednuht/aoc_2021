import sys
from collections import defaultdict
from typing import Tuple, List, Dict, Set


def add_to_dict(d, x, y):
    if (x, y) in d:
        d[(x, y)] += 1
    else:
        d[(x, y)] = 0


def part1(coordinates: List[Tuple[Tuple[int, int], Tuple[int, int]]]):
    intersections = defaultdict(int)
    for (x1, y1), (x2, y2) in coordinates:
        if x1 == x2 or y1 == y2:
            if x1 == x2:
                # vertical
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    intersections[(x1, y)] += 1
            elif y1 == y2:
                # horizontal
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    intersections[(x, y1)] += 1
        elif x1 == x2 and y1 == y2:
            print("they are single point line?")
        # else:
        #     print("is not horizontal or vertical")

    print("part1", sum(1 for v in intersections.values() if v > 1))
    return intersections


def part2(intersections: Dict[(Tuple[int, int], int)], coordinates: List[Tuple[Tuple[int, int], Tuple[int, int]]]):
    for (x1, y1), (x2, y2) in coordinates:
        if x1 != x2 and y1 != y2:
            factorx = 1 if x1 < x2 else -1
            factory = 1 if y1 < y2 else -1

            xs = range(x1, x2 + factorx, factorx)
            ys = range(y1, y2 + factory, factory)

            for x, y in zip(xs, ys):
                intersections[(x, y)] += 1

    print("part2", sum(1 for v in intersections.values() if v > 1))


def main():
    coordinates: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

    for line in sys.stdin:
        a, b = line.strip().split(" -> ")
        x1, y1 = a.split(",")
        x2, y2 = b.split(",")
        coordinates.append(((int(x1), int(y1)), (int(x2), int(y2))))

    intersections = part1(coordinates)
    part2(intersections, coordinates)


if __name__ == '__main__':
    main()
