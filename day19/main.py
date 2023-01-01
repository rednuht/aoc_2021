import itertools
import sys
import copy

# the scanners do not know their own position.
# at least 12 beacons that both scanners detect within the overlap
from collections import defaultdict
from functools import lru_cache
from statistics import median, mean


def get_centroid(coords):
    xs = []
    ys = []
    zs = []

    for x, y, z in coords:
        xs.append(x)
        ys.append(y)
        zs.append(z)

    return [int(median(xs)), int(median(ys)), int(median(zs))]


def shift_coord(coord, from_i):
    coord = list(coord)
    return tuple(coord[from_i:] + coord[:from_i])


def get_directions():
    return list(itertools.product([1, -1], repeat=3))


def coord_change_direction(coord, direction):
    x, y, z = coord
    dx, dy, dz = direction
    return x * dx, y * dy, z * dz


def get_scanner_combinations(coords, directions):
    for i in range(6):
        new_coords = copy.deepcopy(coords)
        cs = []
        for c in new_coords:
            cs.append(list(itertools.permutations(c))[i])
        yield cs
        cs_d = []
        for direction in directions:
            for c in cs:
                cs_d.append(coord_change_direction(c, direction))
            yield cs_d
            cs_d = []


def bring_to_origo(coords, centroid):
    return [
        (
            x - centroid[0],
            y - centroid[1],
            z - centroid[2]
        )
        for x, y, z in coords
    ]


def center_coords(coords_map):
    new_coords_map = {}

    for s, coords in coords_map.items():
        centroid = get_centroid(coords)
        new_coords_map[s] = bring_to_origo(coords, centroid)

    return new_coords_map


def diff_many(coords_a, coords_b):
    # assert len(coords_a) == len(coords_b)
    return [
        (
            coords_a[i][0] - coords_b[i][0],
            coords_a[i][1] - coords_b[i][1],
            coords_a[i][2] - coords_b[i][2],
        )
        for i in range(len(coords_a))
    ]


def diff_one(a, b):
    x, y, z = b
    return a[0] - x, a[1] - y, a[2] - z


def add_one(a, b):
    x, y, z = b
    return a[0] + x, a[1] + y, a[2] + z


def add_single_to_many(coords, coord):
    return [
        (
            coords[i][0] + coord[0],
            coords[i][1] + coord[1],
            coords[i][2] + coord[2],
        )
        for i in range(len(coords))
    ]


def remove_single_to_many(coords, coord):
    return [
        (
            coords[i][0] - coord[0],
            coords[i][1] - coord[1],
            coords[i][2] - coord[2],
        )
        for i in range(len(coords))
    ]


def overlap(coords_a, coords_b, directions):
    for b in get_scanner_combinations(coords_b, directions):
        if coords_a == b:
            print("trying to compare the same!")
            continue
        for ac in coords_a:
            for bc in b:
                offset = diff_one(ac, bc)
                shifted_b = add_single_to_many(b, offset)
                matches = set(coords_a) & set(shifted_b)
                if len(matches) >= 12:
                    return shifted_b, offset, matches
    return None, None, None


def manhattan_distance(coord_1, coord_2):
    xa, ya, za = coord_1
    xb, yb, zb = coord_2

    return abs(xa - xb) + abs(ya - yb) + abs(za - zb)


def main():
    directions = tuple(get_directions()[1:])
    scanner_id = -1
    scanner_to_coords = {}
    for line in sys.stdin:
        if line.startswith("---"):
            scanner_id += 1
            while True:
                line = sys.stdin.readline().strip()
                if not line:
                    break
                x, y, z = line.split(",")
                scanner_to_coords.setdefault(scanner_id, []).append((int(x), int(y), int(z)))

    precomputed_scanners = [
        # (0, 0, 0), (1097, -115, -112), (-33, -61, -1239), (-55, 1187, -97), (1174, 52, -1197),
        # (1074, -1275, 45), (1070, 1093, -62), (2395, -106, -98), (-43, 2417, -105),
        # (1079, 1212, -1164), (1131, -1276, -1223), (2274, -1197, -71), (1127, -2418, -93),
        # (1085, 2334, 30), (1167, -2366, -1155), (2353, -1317, -1185), (2235, -1278, 1231),
        # (-107, -2447, 37), (1043, -3698, -1315), (2298, -2362, 1159), (2325, -1216, 2449),
        # (3507, -1224, 1185), (-176, -3622, -1332), (2384, -3626, 1097), (3482, -1294, 2448),
        # (1126, -1165, 2407), (4788, -1246, 1252), (-37, -4786, -1203), (-118, -1199, 2300),
        # (4780, 56, 1252), (5917, -1266, 1251), (-85, -4917, 50), (4709, 1128, 1142),
        # (5920, -1317, 2386), (4778, 2364, 1246)
    ]

    if not precomputed_scanners:
        matched_scanners = {0: scanner_to_coords.pop(0)}
        scanner_locations = [(0, 0, 0)]
        while scanner_to_coords:
            for scanner_1, scanner_2 in itertools.product(matched_scanners, scanner_to_coords):
                coords1 = matched_scanners[scanner_1]
                coords2 = scanner_to_coords[scanner_2]
                new_coords2, scanner_2_location, common = overlap(coords1, coords2, directions)
                if new_coords2 is not None and scanner_2_location is not None and common is not None:
                    print(f"scanner {scanner_1} match with scanner {scanner_2}, scanner 2 at {scanner_2_location}")
                    matched_scanners[scanner_2] = new_coords2
                    scanner_locations.append(scanner_2_location)
                    scanner_to_coords.pop(scanner_2)
                    break
        print(scanner_locations)
        beacons = {coord for coords in matched_scanners.values() for coord in coords}
        print("part1", len(beacons))
        precomputed_scanners = scanner_locations

    max_manhattan = 0
    for i in range(len(precomputed_scanners)):
        for j in range(i + 1, len(precomputed_scanners)):
            distance = manhattan_distance(precomputed_scanners[i], precomputed_scanners[j])
            if distance > max_manhattan:
                max_manhattan = distance

    print("part2", max_manhattan)


if __name__ == '__main__':
    main()
