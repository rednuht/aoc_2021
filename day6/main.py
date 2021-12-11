import sys
from collections import defaultdict


def main():
    fishes = [int(d) for d in sys.stdin.readline().strip().split(",")]

    fish_map = defaultdict(int)

    for fish in fishes:
        if fish not in fish_map:
            fish_map[fish] = 0
        fish_map[fish] += 1

    for day in range(256):
#print(day)
        #print(fish_map)
        new_fish_map = defaultdict(int)
        for fish, count in fish_map.items():
            if fish == 0:
                new_fish_map[8] += count
                new_fish_map[6] += count
            else:
                new_fish_map[fish - 1] += count
        fish_map = new_fish_map

    print(sum(fish_map.values()))



if __name__ == '__main__':
    main()
