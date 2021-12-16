import sys

table = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

length_type_table = {
    "0": 15,
    "1": 11
}


def convert(d):
    binary = ""

    for c in d:
        binary += table[c]

    return binary


def calculate(values, operator_type):
    # print("doing calculations on", values, operator_type)
    if operator_type == 0:
        return sum(values)
    elif operator_type == 1:
        ans = 1
        for v in values:
            ans *= v
        return ans
    elif operator_type == 2:
        return min(values)
    elif operator_type == 3:
        return max(values)
    elif operator_type == 5:
        assert len(values) == 2
        return 1 if values[0] > values[1] else 0
    elif operator_type == 6:
        assert len(values) == 2
        return 1 if values[0] < values[1] else 0
    elif operator_type == 7:
        assert len(values) == 2
        return 1 if values[0] == values[1] else 0
    else:
        # print("unknown operator type", operator_type)
        assert False


sum_version = 0


def read_packet(bits, i):
    global sum_version
    if i > len(bits):
        return i, 0

    # print("bits from i:", i, bits[i:])
    packet_version = int(bits[i + 0:i + 3], 2)
    packet_type = int(bits[i + 3:i + 6], 2)
    # print("version dec", int(packet_version, 2), "type dec", int(packet_type,2))
    sum_version += packet_version
    if packet_type == 4:
        # literal
        # print("is literal")
        i += 6
        literal_value = ""
        while True:
            group = bits[i:i + 5]
            # #print(group)
            literal_value += group[1:]
            i += 5
            if group[0] == "0":
                break
        # print("literal value is", literal_value, int(literal_value, 2))
        return i, int(literal_value, 2)
    else:
        # operator
        # print("is operator")
        length_type = bits[i + 6]
        # print("length type", length_type)
        length = length_type_table[length_type]
        # print("length is", length)
        if length_type == "0":
            number_bits = int(bits[i + 7:i + 7 + length], 2)
            # print("number of bits", number_bits)
            i += 7 + length
            s = i
            values = []
            while True:
                ni, value = read_packet(bits, i)
                values.append(value)
                if ni - s == number_bits:
                    return ni, calculate(values, packet_type)
                else:
                    i = ni
        elif length_type == "1":
            number_packets = int(bits[i + 7:i + 7 + length], 2)
            # print("number of packets", number_packets)
            i += 7 + length
            values = []
            for p in range(number_packets):
                ni, value = read_packet(bits, i)
                values.append(value)
                i = ni
            return i, calculate(values, packet_type)
        else:
            assert False


def main():
    bits = convert(list(sys.stdin.readline().strip()))
    _, val = read_packet(bits, 0)
    print("part1", sum_version)
    print("part2", val)


if __name__ == '__main__':
    main()
