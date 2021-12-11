import sys


def part1(instructions):
    depth = 0
    horizontal = 0
    for cmd, nr in instructions:
        if cmd == "forward":
            horizontal += nr
        elif cmd == "down":
            depth += nr
        elif cmd == "up":
            depth -= nr

    return horizontal * depth


def part2(instructions):
    aim = 0
    depth = 0
    horizontal = 0
    for cmd, nr in instructions:
        if cmd == "forward":
            horizontal += nr
            depth += aim * nr
        elif cmd == "down":
            aim += nr
        elif cmd == "up":
            aim -= nr

    return horizontal * depth


def to_instruction(raw):
    cmd, nr = raw.split()
    return cmd, int(nr)


def main():
    instructions = [to_instruction(line.strip()) for line in sys.stdin]
    print("part1", part1(instructions))
    print("part2", part2(instructions))


if __name__ == '__main__':
    main()
