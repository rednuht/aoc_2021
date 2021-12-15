import sys
from collections import defaultdict


def main():
    template = sys.stdin.readline().strip()
    sys.stdin.readline()
    pair_insertions = {}
    for line in sys.stdin:
        adjacent, element = line.strip().split(" -> ")
        pair_insertions[adjacent] = element

    # count occurrence of each pair
    pair_count = defaultdict(int)
    for i in range(len(template) - 1):
        pair = template[i:i + 2]
        pair_count[pair] += 1

    print("part1", solve(pair_insertions, pair_count.copy(), 10, template))
    print("part2", solve(pair_insertions, pair_count.copy(), 40, template))


def solve(insertions, pair_count, steps, template):
    for step in range(1, steps + 1):
        new_pair_count = defaultdict(int)
        # each pair AB will create a two new pairs AX and XB
        for pair, n in pair_count.items():
            # we need to increment the number by "n" since the pair AB occurs "n" times and thus
            # would create "n" AX and "n" XB
            new_pair_count[pair[0] + insertions[pair]] += n
            new_pair_count[insertions[pair] + pair[1]] += n
        pair_count = new_pair_count

    char_count = defaultdict(int)
    for k in pair_count:
        # first letter of each pair
        # since the last letter is both the first and the last of two pairs, e.g. ABC, A(B) and (B)C
        char_count[k[0]] += pair_count[k]
    # add the last letter in the input template string
    char_count[template[-1]] += 1
    return max(char_count.values()) - min(char_count.values())


if __name__ == '__main__':
    main()
