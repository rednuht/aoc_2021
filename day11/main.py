import sys


def print_grid(grid):
    for row in grid:
        print("".join(str(d) for d in row))


def get_neighbor_coords(grid, r, c):
    for rr in [-1, 0, 1]:
        for cc in [-1, 0, 1]:
            if rr == 0 and cc == 0:
                continue
            if 0 <= r + rr < len(grid) and 0 <= c + cc < len(grid[0]):
                yield r + rr, c + cc


def coords(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            yield r, c


def main():
    grid = [[int(d) for d in line.strip()] for line in sys.stdin]
    nr_octopuses = len(grid) * len(grid[0])
    nr_flashes = 0
    step = 0
    while 1:
        step += 1
        flashed = set()
        for r, c in coords(grid):
            coordinates_to_check = [(r, c)]
            while coordinates_to_check:
                (row, col) = coordinates_to_check.pop(0)
                if (row, col) not in flashed:
                    grid[row][col] += 1
                    if grid[row][col] > 9:
                        nr_flashes += 1
                        flashed.add((row, col))
                        grid[row][col] = 0
                        coordinates_to_check += list(get_neighbor_coords(grid, row, col))

        if len(flashed) == nr_octopuses:
            print("part2", step)
            break

        if step == 100:
            print("part1", nr_flashes)


if __name__ == '__main__':
    main()
