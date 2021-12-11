import sys
from collections import deque


def get_adjacent_values(m, row, col):
    values = []
    with_coords = []

    # left
    if col - 1 >= 0:
        values.append(m[row][col - 1])
        with_coords.append((m[row][col - 1], row, col - 1))

    # right
    if col + 1 < len(m[0]):
        values.append(m[row][col + 1])
        with_coords.append((m[row][col + 1], row, col + 1))

    # up
    if row - 1 >= 0:
        values.append(m[row - 1][col])
        with_coords.append((m[row - 1][col], row - 1, col))

    # down
    if row + 1 < len(m):
        values.append(m[row + 1][col])
        with_coords.append((m[row + 1][col], row + 1, col))

    return values, with_coords


def part1(heightmap):
    low_points = []
    for i, row in enumerate(heightmap):
        for j, current in enumerate(row):
            adjacent, _ = get_adjacent_values(heightmap, i, j)
            smallest_adjacent = min(adjacent)
            if current < smallest_adjacent:
                low_points.append((current, (i, j)))
    return low_points


def part2(heightmap, low_points):
    basins = []
    seen = set()
    for _, (row, col) in low_points:
        if (row, col) not in seen:
            size = 0
            queue = deque()
            queue.append((row, col))
            while queue:
                (row, col) = queue.popleft()
                if (row, col) not in seen:
                    seen.add((row, col))
                    size += 1
                    _, adjacent = get_adjacent_values(heightmap, row, col)
                    for value, a_row, a_col in adjacent:
                        if value != 9:
                            queue.append((a_row, a_col))
            basins.append(size)
    basins.sort()
    return basins


def main():
    heightmap = [
        [int(d) for d in list(line.strip())]
        for line in sys.stdin.readlines()
    ]

    low_points = part1(heightmap)
    print("part1", sum(v + 1 for v, _ in low_points))

    basins = part2(heightmap, low_points)
    print("part2", basins[-1] * basins[-2] * basins[-3])


if __name__ == '__main__':
    main()
