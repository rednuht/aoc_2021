import sys
import bisect
from dataclasses import dataclass
from typing import List


@dataclass
class Cuboid:
    type: bool
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int


def parse_line(line):
    a, b = line.strip().split()
    x_range_r, y_range_r, z_range_r = b.split(",")
    x1, x2 = x_range_r.split("=")[1].split("..")
    y1, y2 = y_range_r.split("=")[1].split("..")
    z1, z2 = z_range_r.split("=")[1].split("..")

    return Cuboid(a == "on", int(x1), int(x2) + 1, int(y1), int(y2) + 1, int(z1), int(z2) + 1)


def main():
    cuboids: List[Cuboid] = []
    xs: List[int] = []
    ys: List[int] = []
    zs: List[int] = []
    for line in sys.stdin:
        cuboid = parse_line(line)
        cuboids.append(cuboid)
        xs.append(cuboid.x1)
        xs.append(cuboid.x2)
        ys.append(cuboid.y1)
        ys.append(cuboid.y2)
        zs.append(cuboid.z1)
        zs.append(cuboid.z2)

    xs.sort()
    ys.sort()
    zs.sort()
    n = xs[-1]

    def get_index(c: List[int], cc: int) -> int:
        return int(
            bisect.bisect_left(c, cc, lo=c[0], hi=c[-1]) - c[0]
        )

    grid: List[List[List[bool]]] = [
        [
            [False] * n
            for _ in range(n)
        ]
        for _ in range(n)
    ]

    for cuboid in cuboids:
        x1 = get_index(xs, cuboid.x1)
        x2 = get_index(xs, cuboid.x2)
        y1 = get_index(xs, cuboid.y1)
        y2 = get_index(xs, cuboid.y2)
        z1 = get_index(xs, cuboid.z1)
        z2 = get_index(xs, cuboid.z2)

        for x in range(x1, x2):
            for y in range(y1, y2):
                for z in range(z1, z2):
                    grid[x][y][z] = cuboid.type

    ans = 0
    for x in range(0, n - 1):
        for y in range(0, n - 1):
            for z in range(0, n - 1):
                ans += int(grid[x][y][z]) * (xs[x + 1] - xs[x]) * (ys[y + 1] - ys[y]) * (zs[z + 1] - zs[y])

    print(ans)


if __name__ == '__main__':
    main()
