import sys

import pyperf as pyperf


def solve(signal_patterns, output_value):
    one = next((s for s in signal_patterns if len(s) == 2), None)
    seven = next((s for s in signal_patterns if len(s) == 3), None)
    four = next((s for s in signal_patterns if len(s) == 4), None)
    eight = next((s for s in signal_patterns if len(s) == 7), None)
    three = next((s for s in signal_patterns if len(s) == 5 and set(one) <= set(s)), None)
    nine = next((s for s in signal_patterns if len(s) == 6 and set(one) <= set(s) and set(three) <= set(s)), None)
    zero = next((s for s in signal_patterns if len(s) == 6 and s != nine and set(one) <= set(s)), None)
    six = next((s for s in signal_patterns if len(s) == 6 and s != nine and s != zero), None)
    c_segment = set(eight) - set(six)
    two = next((s for s in signal_patterns if len(s) == 5 and s != three and c_segment <= set(s)), None)
    five = next((s for s in signal_patterns if len(s) == 5 and s != three and not c_segment <= set(s)), None)

    m = {
        "".join(sorted(zero)): 0,
        "".join(sorted(one)): 1,
        "".join(sorted(two)): 2,
        "".join(sorted(three)): 3,
        "".join(sorted(four)): 4,
        "".join(sorted(five)): 5,
        "".join(sorted(six)): 6,
        "".join(sorted(seven)): 7,
        "".join(sorted(eight)): 8,
        "".join(sorted(nine)): 9
    }

    v = "".join(str(m["".join(sorted(o))]) for o in output_value)

    return int(v)


def main():
    part1_c = 0
    part2_c = 0
    for line in sys.stdin:
        first, second = line.strip().split("|")
        signal_patterns = first.strip().split()
        output_value = second.strip().split()
        part1_c += count_part1(output_value)
        part2_c += solve(signal_patterns, output_value)

    print("part1", part1_c)
    print("part2", part2_c)


def count_part1(output_value):
    return sum(1 for o in output_value if len(o) in [2, 3, 4, 7])


if __name__ == '__main__':
    main()
