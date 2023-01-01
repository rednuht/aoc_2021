import sys
import itertools
from typing import Set


class Cuboid:

    def __init__(self, x1, x2, y1, y2, z1, z2, on):
        self.x1: int = x1
        self.x2: int = x2
        self.y1: int = y1
        self.y2: int = y2
        self.z1: int = z1
        self.z2: int = z2
        self.on: bool = on

    def volume(self):
        return abs(self.x2 - self.x1 + 1) * abs(self.y2 - self.y1 + 1) * abs(self.z2 - self.z1 + 1)

    def overlap(self, cuboid, on):
        x1 = max(self.x1, cuboid.x1)
        x2 = min(self.x2, cuboid.x2)
        y1 = max(self.y1, cuboid.y1)
        y2 = min(self.y2, cuboid.y2)
        z1 = max(self.z1, cuboid.z1)
        z2 = min(self.z2, cuboid.z2)

        if x1 <= x2 and y1 <= y2 and z1 <= z2:
            c = Cuboid(x1, x2, y1, y2, z1, z2, on)
            return c

        return None


def part1(lines):
    lit = set()
    for i, line in enumerate(lines):
        a, b = line.strip().split()
        x_range_r, y_range_r, z_range_r = b.split(",")
        x1, x2 = x_range_r.split("=")[1].split("..")
        y1, y2 = y_range_r.split("=")[1].split("..")
        z1, z2 = z_range_r.split("=")[1].split("..")

        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        z1 = int(z1)
        z2 = int(z2)

        if -50 <= x1 and x2 <= 50 and -50 <= y1 and y2 <= 50 and -50 <= z1 and z2 <= 50:
            xs = range(x1, x2 + 1)
            ys = range(y1, y2 + 1)
            zs = range(z1, z2 + 1)
            if a == "on":
                lit = lit.union(set(itertools.product(xs, ys, zs)))
            else:
                lit = lit - set(itertools.product(xs, ys, zs))

    print("part1", len(lit))


def part2_faster(lines):
    cubes: Set[Cuboid] = set()
    for i, line in enumerate(lines):
        a, b = line.strip().split()
        x_range_r, y_range_r, z_range_r = b.split(",")
        x1, x2 = x_range_r.split("=")[1].split("..")
        y1, y2 = y_range_r.split("=")[1].split("..")
        z1, z2 = z_range_r.split("=")[1].split("..")

        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        z1 = int(z1)
        z2 = int(z2)

        cuboid = Cuboid(x1, x2, y1, y2, z1, z2, a == "on")
        new_cubes = {cuboid} if cuboid.on == 1 else set()
        for c in cubes:
            overlap = c.overlap(cuboid, not c.on)
            if overlap is not None:
                new_cubes.add(overlap)
        cubes |= new_cubes

    ans = sum(cube.volume() * (1 if cube.on else -1) for cube in cubes)
    print("part2", ans)


def compress(nums):
    nums = sorted(nums)
    nums_map = {}
    lengths = {}
    for i, num in enumerate(nums):
        nums_map[num] = i
        if i + 1 < len(nums):
            length = nums[i + 1] - num
            lengths[i] = length
    return nums_map, lengths


def parse_line(line):
    a, b = line.strip().split()
    # print(i)
    x_range_r, y_range_r, z_range_r = b.split(",")
    x1, x2 = x_range_r.split("=")[1].split("..")
    y1, y2 = y_range_r.split("=")[1].split("..")
    z1, z2 = z_range_r.split("=")[1].split("..")

    return int(x1), int(x2), int(y1), int(y2), int(z1), int(z2), a == "on"


def part2(lines):
    cubes = []
    xs = set()
    ys = set()
    zs = set()
    for line in lines:
        x1, x2, y1, y2, z1, z2, on = parse_line(line)
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        z1, z2 = min(z1, z2), max(z1, z2)
        cubes.append((x1, x2, y1, y2, z1, z2, on))
        xs.add(x1)
        xs.add(x2 + 1)
        ys.add(y1)
        ys.add(y2 + 1)
        zs.add(z1)
        zs.add(z2 + 1)

    xm, xl = compress(xs)
    ym, yl = compress(ys)
    zm, zl = compress(zs)
    lit = set()
    for x1, x2, y1, y2, z1, z2, on in cubes:
        for xx, yy, zz in itertools.product(range(xm[x1], xm[x2 + 1]),
                                            range(ym[y1], ym[y2 + 1]),
                                            range(zm[z1], zm[z2 + 1])):
            if on:
                lit.add((xx, yy, zz))
            elif (xx, yy, zz) in lit:
                lit.remove((xx, yy, zz))

    ans = sum(xl[x] * yl[y] * zl[z] for x, y, z in lit)

    print(ans)


def main():
    lines = sys.stdin.readlines()

    part1(lines)
    part2_faster(lines)





if __name__ == '__main__':
    main()
