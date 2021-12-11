import sys


def main():
    count_p1 = 0
    count_p2 = 0
    stack = []
    for i, line in enumerate(sys.stdin):
        nr = int(line.strip())
        if i > 0:
            if stack[-1] < nr:
                count_p1 += 1

            if i > 2:
                if stack[0] < nr:
                    count_p2 += 1
                stack.pop(0)

        stack.append(nr)

    print("part1", count_p1)
    print("part2", count_p2)


if __name__ == '__main__':
    main()
