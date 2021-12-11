import math
import sys
import statistics
from math import ceil, floor


def calculate_fuel_cost(numbers, i):
    return int(
        sum(
            abs(num - i) * (1 + abs(num - i)) / 2
            for num in numbers
        )
    )


def part1(numbers):
    median = statistics.median(numbers)
    print("part1", int(sum(abs(d - median) for d in numbers)))


def part2(numbers):
    median = statistics.median(numbers)
    mean = sum(numbers) / len(numbers)
    nr_strict_smaller = len([n for n in numbers if n < median])
    nr_greater = len([n for n in numbers if n > median])
    alignment = floor(mean) if nr_strict_smaller > nr_greater else ceil(mean)
    print("part2", calculate_fuel_cost(numbers, alignment))


def main():
    numbers = [int(d) for d in sys.stdin.readline().strip().split(",")]
    part1(numbers)
    part2(numbers)


# runner.bench_func("solve", solve)

if __name__ == '__main__':
    main()
