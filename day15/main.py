import sys
from queue import PriorityQueue


def next_n(n):
    if n > 9:
        n = n % 9
        return 1 if n == 0 else n
    return n


def expand_cavern(cavern):
    expanded_rows = []

    # expand to the right
    for r, row in enumerate(cavern):
        expanded_row = []
        for i in range(0, 5):
            expanded_row += [next_n(n + i) for n in row]
        expanded_rows.append(expanded_row)

    # expand down
    expanded_cavern = [[] for _ in range(5 * len(cavern))]
    for r, row in enumerate(expanded_rows):
        expanded_cavern[r] = row
        for i in range(5):
            expanded_cavern[r + i * len(cavern)] = [next_n(n + i) for n in row]
    return expanded_cavern


def dijkstra(cavern):
    # init distances
    distances = [[1e9 for _ in range(len(cavern[0]))] for _ in range(len(cavern))]
    distances[0][0] = 0

    # priority queue with (distance, (x, y))
    queue = PriorityQueue()
    queue.put((0, (0, 0)))

    visited = set()
    x_length = len(cavern[0])
    y_length = len(cavern)

    while not queue.empty():
        dist, (x, y) = queue.get()
        visited.add((x, y))
        # for right, up, left, down neighbours
        for xx, yy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            # within the bounds
            if 0 <= x + xx < x_length and 0 <= y + yy < y_length:
                # that we haven't visited yet
                if (x + xx, y + yy) not in visited:
                    # calculate the distances
                    new_dist = distances[y][x] + cavern[y + yy][x + xx]
                    next_dist = distances[y + yy][x + xx]
                    if new_dist < next_dist:
                        # update the distance map and priority queue with new values
                        distances[y + yy][x + xx] = new_dist
                        queue.put((new_dist, (x + xx, y + yy)))

    return distances[len(cavern) - 1][len(cavern[0]) - 1]


def main():
    cavern = [[int(d) for d in list(line.strip())] for line in sys.stdin.readlines()]
    print("part1", dijkstra(cavern))
    print("part2", dijkstra(expand_cavern(cavern)))


if __name__ == '__main__':
    main()
