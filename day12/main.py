import sys
from dataclasses import dataclass
from typing import Dict, Set, Any


@dataclass
class Cave:
    small: bool
    name: str
    caves: Set['Cave']

    def __hash__(self):
        return self.name.__hash__()

    def __repr__(self):
        cave_names = [c.name for c in self.caves]
        return f"{self.name} -> {cave_names}"

    def __str__(self):
        return self.__repr__()


def traverse_part1(current: Cave, visited: Set[str]):
    s = 0
    if current.name == "end":
        return 1
    else:
        for cave in current.caves:
            if cave.small and cave.name in visited:
                continue
            else:
                new_visited = visited.copy()
                if cave.small:
                    new_visited.add(cave.name)
                s += traverse_part1(cave, new_visited)

    return s


def traverse_part2(current: Cave, visited: Dict[str, int]):
    s = 0
    if current.name == "end":
        return 1
    else:
        for cave in current.caves:
            nr_visits = visited.get(cave.name, 0)
            if cave.small:
                if cave.name in ["start", "end"] and nr_visits == 1:
                    continue
                elif 2 in visited.values() and nr_visits in [1, 2]:
                    continue

            new_visited = visited.copy()
            if cave.small:
                if cave.name in new_visited and 2 not in visited.values():
                    new_visited[cave.name] += 1
                else:
                    new_visited[cave.name] = 1
            s += traverse_part2(cave, new_visited)

    return s


def main():
    lines = [
        "start-A",
        "start-b",
        "A-c",
        "A-b",
        "b-d",
        "A-end",
        "b-end",
    ]

    caves: Dict[str, Cave] = dict()
    for line in sys.stdin:
        f, t = line.strip().split("-")

        f_cave = caves.get(f, Cave(small=f.lower() == f, name=f, caves=set()))
        t_cave = caves.get(t, Cave(small=t.lower() == t, name=t, caves=set()))
        f_cave.caves.add(t_cave)
        t_cave.caves.add(f_cave)
        caves[f] = f_cave
        caves[t] = t_cave

    start = caves["start"]
    print("part1", traverse_part1(start, {start.name}))
    print("part2", traverse_part2(start, {start.name: 1}))


if __name__ == '__main__':
    main()
