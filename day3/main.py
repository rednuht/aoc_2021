import sys


def filter(numbers, bit, constraint):
    num_m = dict()
    new_numbers = []
    one_numbers = []
    zero_numbers = []
    cc = 0
    for j, number in enumerate(numbers):
        num_m[j] = number
        if number[bit] == "1":
            cc += 1
            one_numbers.append(number)
        else:
            zero_numbers.append(number)

    print("cc is", cc)
    if cc > (len(numbers) - cc):
        if constraint == 1:
            new_numbers += one_numbers
        else:
            new_numbers += zero_numbers
    elif cc == (len(numbers) - cc):
        if constraint == 1:
            new_numbers += one_numbers
        else:
            new_numbers += zero_numbers
    else:
        new_numbers += zero_numbers

    if constraint == 1:
        new_numbers = one_numbers if len(one_numbers) > len(zero_numbers) else zero_numbers
    else:
        new_numbers = one_numbers if len(one_numbers) < len(zero_numbers) else zero_numbers

    if len(one_numbers) == len(zero_numbers):
        if one_numbers[0].count(f"{constraint}") > zero_numbers[0].count(f"{constraint}"):
            new_numbers = one_numbers
        else:
            new_numbers = zero_numbers

    print(bit, one_numbers, ",", zero_numbers, "returning", new_numbers)

    return new_numbers


def find_most_common(numbers):
    s = len(numbers)
    nums = numbers
    s = len(numbers[0])
    for i in range(0, s):
        nums = filter(nums, i, 1)
        if len(nums) == 1:
            break

    print("in the end mc:", nums, int(nums[0], 2))
    return nums[0]


def find_least_common(numbers):
    print("least common", numbers)
    s = len(numbers)
    nums = numbers
    s = len(numbers[0])
    for i in range(0, s):
        nums = filter(nums, i, 0)
        if len(nums) == 1:
            break

    print("in the end lc:", nums, int(nums[0], 2))
    return nums[0]


def main():
    lines = [line.strip() for line in sys.stdin]

    bits = dict()
    for line in lines:
        for i, d in enumerate(line):
            bits.setdefault(i, []).append(int(d))

    gamma = ""
    epsilon = ""
    # print(bits)
    for i in range(len(lines[0])):
        # print(bits.get(i))
        nr_1s = sum(bits.get(i))
        c = len(bits.get(i))
        # print("1s", nr_1s)
        # print("c1", c)
        if nr_1s > (c - nr_1s):
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"

    print(int(gamma, 2) * int(epsilon, 2))

    mc = find_most_common(lines)
    lc = find_least_common(lines)

    print(int(mc, 2)* int(lc, 2))


if __name__ == '__main__':
    main()
