import sys


def print_paper(coordinates, x_max, y_max):
    for y in range(y_max):
        for x in range(x_max):
            if (x, y) in coordinates:
                print("#", end="")
            else:
                print(" ", end="")
        print()


def fold(coordinates, fold_instructions):
    for i, (dim, value) in enumerate(fold_instructions):
        coordinates_new = {}
        for (x, y) in coordinates:
            if dim == "x":
                if x < value:
                    coordinates_new[(x, y)] = True
                else:
                    coordinates_new[(value - (x - value), y)] = True
            else:
                if y < value:
                    coordinates_new[(x, y)] = True
                else:
                    coordinates_new[x, (value - (y - value))] = True
        coordinates = coordinates_new
        if i == 0:
            print("part1:", len(coordinates))
    return coordinates


def main():
    coordinates = {}
    fold_instructions = []
    parse_folds = False
    x_max = 0
    y_max = 0
    for line in sys.stdin:
        line = line.strip()
        if not line:
            parse_folds = True
            continue

        if parse_folds:
            _, raw = line.rsplit(" ", 1)
            dim, value = raw.split("=")
            value = int(value)
            if dim == "x":
                x_max = value
            if dim == "y":
                y_max = value
            fold_instructions.append((dim, value))
        else:
            x, y = line.split(",")
            coordinates[(int(x), int(y))] = True

    coordinates = fold(coordinates, fold_instructions)
    print_paper(coordinates, x_max, y_max)


if __name__ == '__main__':
    main()
