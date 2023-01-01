import sys
import copy


def print_grid(grid):
    for row in grid:
        print("".join(row))


def next_pos(grid, r_size, c_size, r_cur, c_cur):
    sea_cucumber_type = grid[r_cur][c_cur]
    if sea_cucumber_type == ">":
        next_c = c_cur + 1 if c_cur + 1 < c_size else 0
        if grid[r_cur][next_c] == ".":
            return True, (r_cur, next_c)
    elif sea_cucumber_type == "v":
        next_r = r_cur + 1 if r_cur + 1 < r_size else 0
        if grid[next_r][c_cur] == ".":
            return True, (next_r, c_cur)
    else:
        assert False

    return False, (r_cur, c_cur)


def move_sea_cucumbers(grid, r_size, c_size, sea_cucumber_type):
    new_grid = [["."] * c_size for _ in range(r_size)]
    flipped = set()
    for r in range(r_size):
        for c in range(c_size):
            if (r, c) in flipped:
                flipped.remove((r, c))
                continue
            if grid[r][c] == sea_cucumber_type:
                can_move, (new_r, new_c) = next_pos(grid, r_size, c_size, r, c)
                if can_move:
                    flipped.add((new_r, new_c))
                    new_grid[new_r][new_c] = grid[r][c]
                else:
                    new_grid[r][c] = grid[r][c]
            else:
                new_grid[r][c] = grid[r][c]
    return new_grid


def main():
    grid = [list(line.strip()) for line in sys.stdin]
    r_size = len(grid)
    c_size = len(grid[0])
    step = 1
    while True:
        new_grid = move_sea_cucumbers(
            move_sea_cucumbers(grid, r_size, c_size, ">"),
            r_size,
            c_size,
            "v"
        )
        if grid != new_grid:
            grid = copy.deepcopy(new_grid)
        else:
            break
        step += 1

    print("part1", step)


if __name__ == '__main__':
    main()
