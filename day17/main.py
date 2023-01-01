import sys


def trace(x_v, y_v, x_f, x_t, y_f, y_t):
    x = 0
    y = 0
    y_max = 0
    hits = []
    while True:
        x += x_v
        y += y_v

        if y > y_max:
            y_max = y

        if x_f <= x <= x_t and y_f <= y <= y_t:
            hits.append(y_max)

        if x > x_t or y < y_f:
            break

        if x_v > 0:
            x_v -= 1
        elif x_v < 0:
            x_v += 1

        y_v -= 1

    return hits


def main():
    data = sys.stdin.readline().strip().split("target area: ")[1]
    x_data, y_data = data.split(", ")

    x_range = x_data.split("x=")[1].split("..")
    y_range = y_data.split("y=")[1].split("..")
    x_range = (int(x_range[0]), int(x_range[1]))
    y_range = (int(y_range[0]), int(y_range[1]))

    y_maxes = []
    coords = []
    for x_v in range(1, 300):
        for y_v in range(-300, 300):
            hits = trace(x_v, y_v, *x_range, *y_range)
            for hit in hits:
                y_maxes.append(hit)
                coords.append((x_v, y_v))

    print("part1", max(y_maxes))
    print("part2", len(set(coords)))


if __name__ == '__main__':
    main()
