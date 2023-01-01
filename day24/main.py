import operator
import sys
from functools import lru_cache

instructions = [line.strip().split() for line in sys.stdin]
print(instructions)


def expand(registry, expression):
    reg_name, _a, _b, op = expression

    a = _a
    b = _b
    # a = lit_or_reg(registry, _a)
    # b = lit_or_reg(registry, _b)

    if isinstance(a, int) and isinstance(b, int):
        res = op(a, b)
        registry[reg_name] = res
        return res
    elif isinstance(a, tuple) and isinstance(b, tuple):
        return op(expand(registry, a), expand(registry, b))
    elif isinstance(a, tuple):
        return op(expand(registry, a), b)
    elif isinstance(b, tuple):
        return op(a, expand(registry, b))
    else:
        assert False, "don't know what to do :("

    # return None


def lit_or_reg(registry, a: str):
    return registry[a] if a in registry else int(a)


@lru_cache(maxsize=None)
def search(i, w, x, y, z):
    if z > 10 ** 8:
        return False, ""
    # print(i)
    if i >= len(instructions):
        return z == 0, ""

    registry = {"w": w, "x": x, "y": y, "z": z}

    instruction = instructions[i]
    # print(instruction)
    i_type = instruction[0]
    reg_name = instruction[1]
    if i_type == "inp":
        for d in range(1, 10):
            registry[reg_name] = d
            success, s = search(i + 1, registry["w"], registry["x"], registry["y"], registry["z"])
            if success:
                print(i, w, x, y, z, str(d) + s)
                return True, str(d) + s

        return False, 0

    i_type = instruction[0]
    b = lit_or_reg(registry, instruction[2])

    if i_type == "add":
        registry[reg_name] += b
    elif i_type == "mul":
        registry[reg_name] *= b
    elif i_type == "div":
        if b == 0:
            return False, 0
        registry[reg_name] = int(registry[reg_name] / b)
    elif i_type == "mod":
        if registry[reg_name] < 0 or b <= 0:
            return False, 0
        registry[reg_name] %= b
    elif i_type == "eql":
        registry[reg_name] = 1 if registry[reg_name] == b else 0
    else:
        assert False

    return search(i + 1, registry["w"], registry["x"], registry["y"], registry["z"])


print(search(0, 0, 0, 0, 0))


def run_instructions(instructions, bits):
    registry = {
        "w": 0,
        "x": 0,
        "y": 0,
        "z": 0
    }

    for j, instruction in enumerate(instructions):
        i_type = instruction[0]

        if len(instruction) == 3:
            a, b = instruction[1:]
            reg_name = a
            a = lit_or_reg(registry, a)
            b = lit_or_reg(registry, b)
            # if not isinstance(a, int) or not isinstance(b, int):
            #     stack.appendleft((i_type, a, b))
            #     continue
        else:
            a = instruction[1]
            reg_name = a
            b = None

        if i_type == "inp":
            registry[reg_name] = bits.pop(0)
            # if stack:
            #     print("something in the stack")

        elif i_type == "add":
            if isinstance(a, int) and isinstance(b, int):
                registry[reg_name] = a + b
            elif a == 0:
                registry[reg_name] = b
            elif b == 0:
                registry[reg_name] = a
            else:
                registry[reg_name] = (reg_name, a, b, operator.add)
                # assert False, f"Can't add {a} and {b} :("

        elif i_type == "mul":
            if a == 0 or b == 0:
                registry[reg_name] = 0
            elif a == 1 and not isinstance(b, int):
                registry[reg_name] = b
            elif b == 1 and not isinstance(a, int):
                registry[reg_name] = a
            elif isinstance(a, int) and isinstance(b, int):
                registry[reg_name] = a * b
            else:
                registry[reg_name] = (reg_name, a, b, operator.mul)
                # assert False, f"can't mul {a} and {b}"

        elif i_type == "div":
            if isinstance(a, int) and isinstance(b, int):
                registry[reg_name] = a // b
            elif b == 1:
                registry[reg_name] = a
            else:
                registry[reg_name] = (reg_name, a, b, operator.floordiv)
                # assert False, f"can't div {a} and {b}"

        elif i_type == "mod":
            if isinstance(a, int) and isinstance(b, int):
                registry[reg_name] = a % b
            elif a == 0:
                registry[reg_name] = 0
            else:
                registry[reg_name] = (reg_name, a, b, operator.mod)
                # assert False, f"Can't mod {a} and {b}"
        elif i_type == "eql":
            if isinstance(a, int) and isinstance(b, int) or isinstance(a, str) and isinstance(b, str):
                registry[reg_name] = 1 if a == b else 0
            else:
                registry[reg_name] = (reg_name, a, b, operator.eq)
        else:
            assert False

    return registry


def solve(z, z_div, x_add, y_add):
    for w in range(9, 0, -1):
        # x = z % 26
        # z = z // z_div
        # x += x_add
        # x = 1 if x == w else 0
        # x = 1 if x == 0 else 0
        # y = 25 * x + 1
        # z *= y
        # y = w + y_add
        # y *= x
        # z += y
        #
        # yield w, z

        x = z % 26
        z //= z_div
        x += x_add

        if x != w:
            z *= 26
            y = w
            y += y_add
            z += y

        yield w, z


def run():
    for b1, z1 in solve(0, 1, 15, 15):
        for b2, z2 in solve(z1, 1, 15, 10):
            for b3, z3 in solve(z2, 1, 12, 2):
                for b4, z4 in solve(z3, 1, 13, 16):
                    for b5, z5 in solve(z4, 26, -12, 12):
                        for b6, z6 in solve(z5, 1, 10, 11):
                            for b7, z7 in solve(z6, 26, -9, 5):
                                for b8, z8 in solve(z7, 1, 14, 16):
                                    for b9, z9 in solve(z8, 1, 13, 6):
                                        for b10, z10 in solve(z9, 26, -14, 15):
                                            for b11, z11 in solve(z10, 26, -11, 3):
                                                for b12, z12 in solve(z11, 26, -2, 12):
                                                    for b13, z13 in solve(z12, 26, -16, 10):
                                                        for b14, z14 in solve(z13, 26, -14, 13):
                                                            if z14 == 0:
                                                                # print(b1)
                                                                yield int(
                                                                    f"{b1}{b2}{b3}{b4}{b5}{b6}{b7}{b8}{b9}{b10}{b11}{b12}{b13}{b14}")


def run2():
    # w =     [9, 9, 9, 9,  9, 9,  9, 9, 9,  9,  9,  9,  9, 9]
    w = [0] * 14
    #        x    x   x   x    x   x   x   x   x   x    x    x    x
    z_div = [1, 1, 1, 1, 26, 1, 26, 1, 1, 26, 26, 26, 26, 26]
    x_add = [15, 15, 12, 13, -12, 10, -9, 14, 13, -14, -11, -2, -16, -14]
    y_add = [15, 10, 2, 16, 12, 11, 5, 16, 6, 15, 3, 12, 10, 13]

    while True:
        x = 0
        y = 0
        z = 0
        for i in range(14):
            z26 = z % 26
            goal = z26 + x_add[i]
            if 1 <= goal <= 9:
                w[i] = goal
            z //= z_div[i]
            x = 0 if w[i] == goal else 1
            z *= (25 if x == 1 else 0) + 1
            z += (w[i] + y_add[i] if x == 1 else 0)
            if x_add[i] < 10 and w[i] != goal:
                break
        if z == 0 and 0 not in w:
            print(w)
            return


def run3(bits):
    z_div = [1, 1, 1, 1, 26, 1, 26, 1, 1, 26, 26, 26, 26, 26]
    x_add = [15, 15, 12, 13, -12, 10, -9, 14, 13, -14, -11, -2, -16, -14]
    y_add = [15, 10, 2, 16, 12, 11, 5, 16, 6, 15, 3, 12, 10, 13]

    z = 0
    for i in range(14):
        w = bits.pop(0)
        x = z % 26
        z = int(z / z_div[i])
        x += x_add[i]

        if x != w:
            z *= 26
            y = w
            y += y_add[i]
            z += y

    return z

# def main():
#     global instructions
#     z_div = [1, 1, 1, 1, 26, 1, 26, 1, 1, 26, 26, 26, 26, 26]
#     x_add = [15, 15, 12, 13, -12, 10, -9, 14, 13, -14, -11, -2, -16, -14]
#     y_add = [15, 10, 2, 16, 12, 11, 5, 16, 6, 15, 3, 12, 10, 13]

# highest_i = 0
# for i in range(99999999999999, 11111111111111, -1):
#     bits = list(int(d) for d in str(i))
#     if 0 not in bits:
#         z = run3(bits)
#         if z == 0:
#             highest_i = i
#             break
# print("part1", highest_i)

# gen = run()
# for _ in range(10):
#     ans = next(gen)
#     print("part1", ans)

# instructions = [line.strip().split() for line in sys.stdin]
# print(search(0, 0, 0, 0, 0))

# highest = li(run())
# print(highest)
# valid_numbers = list(run())
# print("part1", max(valid_numbers))


# def main():
#     # lines = [
#     #     "inp w",
#     #     "mul x 0",
#     #     "add x z",
#     #     "mod x 26",
#     #     "div z 1",
#     #     "add x 15",
#     #     "eql x w",
#     #     "eql x 0",
#     #     "mul y 0",
#     #     "add y 25",
#     #     "mul y x",
#     #     "add y 1",
#     #     "mul z y",
#     #     "mul y 0",
#     #     "add y w",
#     #     "add y 15",
#     #     "mul y x",
#     #     "add z y",
#     #     "inp w",
#     #     "mul x 0",
#     #     "add x z",
#     #     "mod x 26",
#     #     "div z 1",
#     #     "add x 15",
#     #     "eql x w",
#     #     "eql x 0",
#     #     "mul y 0",
#     #     "add y 25",
#     #     "mul y x",
#     #     "add y 1",
#     #     "mul z y",
#     #     "mul y 0",
#     #     "add y w",
#     #     "add y 10",
#     #     "mul y x",
#     #     "add z y",
#     #     "inp w",
#     #     "mul x 0",
#     #     "add x z",
#     #     "mod x 26",
#     #     "div z 1",
#     #     "add x 12",
#     #     "eql x w",
#     #     "eql x 0",
#     #     "mul y 0",
#     #     "add y 25",
#     #     "mul y x",
#     #     "add y 1",
#     #     "mul z y",
#     #     "mul y 0",
#     #     "add y w",
#     #     "add y 2",
#     #     "mul y x",
#     #     "add z y",
#     #     "inp w",
#     #     "mul x 0",
#     #     "add x z",
#     #     "mod x 26",
#     #     "div z 1",
#     #     "add x 13",
#     #     "eql x w",
#     #     "eql x 0",
#     #     "mul y 0",
#     #     "add y 25",
#     #     "mul y x",
#     #     "add y 1",
#     #     "mul z y",
#     #     "mul y 0",
#     #     "add y w",
#     #     "add y 16",
#     #     "mul y x",
#     #     "add z y",
#     #     "inp w",
#     #     "mul x 0",
#     #     "add x z",
#     #     "mod x 26",
#     #     "div z 26",
#     #     "add x -12",
#     #     "eql x w",
#     #     "eql x 0",
#     #     "mul y 0",
#     #     "add y 25",
#     #     "mul y x",
#     #     "add y 1",
#     #     "mul z y",
#     #     "mul y 0",
#     #     "add y w",
#     #     "add y 12",
#     #     "mul y x",
#     #     "add z y",
#     #     "inp w",
#     #     "mul x 0",
#     #     "add x z",
#     #     "mod x 26",
#     #     "div z 1",
#     #     "add x 10",
#     #     "eql x w",
#     #     "eql x 0",
#     #     "mul y 0",
#     #     "add y 25",
#     #     "mul y x",
#     #     "add y 1",
#     #     "mul z y",
#     #     "mul y 0",
#     #     "add y w",
#     #     "add y 11",
#     #     "mul y x",
#     #     "add z y",
#     #     "inp w",
#     #     "mul x 0",
#     #     "add x z",
#     #     "mod x 26",
#     #     "div z 26",
#     #     "add x -9",
#     #     "eql x w",
#     #     "eql x 0",
#     #     "mul y 0",
#     #     "add y 25",
#     #     "mul y x",
#     #     "add y 1",
#     #     "mul z y",
#     #     "mul y 0",
#     #     "add y w",
#     #     "add y 5",
#     #     "mul y x",
#     #     "add z y",
#     #     "inp w",
#     #     "mul x 0",
#     #     "add x z",
#     #     "mod x 26",
#     #     "div z 1",
#     #     "add x 14",
#     #     "eql x w",
#     #     "eql x 0",
#     #     "mul y 0",
#     #     "add y 25",
#     #     "mul y x",
#     #     "add y 1",
#     #     "mul z y",
#     #     "mul y 0",
#     #     "add y w",
#     #     "add y 16",
#     #     "mul y x",
#     #     "add z y",
#     #     "inp w",
#     #     "mul x 0",
#     #     "add x z",
#     #     "mod x 26",
#     #     "div z 1",
#     #     "add x 13",
#     #     "eql x w",
#     #     "eql x 0",
#     #     "mul y 0",
#     #     "add y 25",
#     #     "mul y x",
#     #     "add y 1",
#     #     "mul z y",
#     #     "mul y 0",
#     #     "add y w",
#     #     "add y 6",
#     #     "mul y x",
#     #     "add z y",
#     #     "inp w",
#     #     "mul x 0",
#     #     "add x z",
#     #     "mod x 26",
#     #     "div z 26",
#     #     "add x -14",
#     #     "eql x w",
#     #     "eql x 0",
#     #     "mul y 0",
#     #     "add y 25",
#     #     "mul y x",
#     #     "add y 1",
#     #     "mul z y",
#     #     "mul y 0",
#     #     "add y w",
#     #     "add y 15",
#     #     "mul y x",
#     #     "add z y",
#     #     "inp w",
#     #     "mul x 0",
#     #     "add x z",
#     #     "mod x 26",
#     #     "div z 26",
#     #     "add x -11",
#     #     "eql x w",
#     #     "eql x 0",
#     #     "mul y 0",
#     #     "add y 25",
#     #     "mul y x",
#     #     "add y 1",
#     #     "mul z y",
#     #     "mul y 0",
#     #     "add y w",
#     #     "add y 3",
#     #     "mul y x",
#     #     "add z y",
#     #     "inp w",
#     #     "mul x 0",
#     #     "add x z",
#     #     "mod x 26",
#     #     "div z 26",
#     #     "add x -2",
#     #     "eql x w",
#     #     "eql x 0",
#     #     "mul y 0",
#     #     "add y 25",
#     #     "mul y x",
#     #     "add y 1",
#     #     "mul z y",
#     #     "mul y 0",
#     #     "add y w",
#     #     "add y 12",
#     #     "mul y x",
#     #     "add z y",
#     #     "inp w",
#     #     "mul x 0",
#     #     "add x z",
#     #     "mod x 26",
#     #     "div z 26",
#     #     "add x -16",
#     #     "eql x w",
#     #     "eql x 0",
#     #     "mul y 0",
#     #     "add y 25",
#     #     "mul y x",
#     #     "add y 1",
#     #     "mul z y",
#     #     "mul y 0",
#     #     "add y w",
#     #     "add y 10",
#     #     "mul y x",
#     #     "add z y",
#     #     "inp w",
#     #     "mul x 0",
#     #     "add x z",
#     #     "mod x 26",
#     #     "div z 26",
#     #     "add x -14",
#     #     "eql x w",
#     #     "eql x 0",
#     #     "mul y 0",
#     #     "add y 25",
#     #     "mul y x",
#     #     "add y 1",
#     #     "mul z y",
#     #     "mul y 0",
#     #     "add y w",
#     #     "add y 13",
#     #     "mul y x",
#     #     "add z y",
#     # ]
#
#     lines = [
#         "inp w",
#         "mul x 0",
#         "add x z",
#         "mod x 26",
#         "div z 1",
#         "add x 15",
#         "eql x w",
#         "eql x 0",
#         "mul y 0",
#         "add y 25",
#         "mul y x",
#         "add y 1",
#         "mul z y",
#         "mul y 0",
#         "add y w",
#         "add y 15",
#         "mul y x",
#         "add z y",
#     ]
#
#     instructions = [line.strip().split() for line in lines]
#
#     # 11111111111111
#     # 99999999999999
#     valid_numbers = []
#     # for i in range(99999999999999, 11111111111111, -1):
#     for i in range(9, 0, -1):
#         bits = list(int(d) for d in str(i))
#         if 0 not in bits:
#             registry = run_instructions(instructions, bits)
#             # print(registry.get("z"))
#             # print(expand(registry, registry.get("z")))
#             # break
#             print(i)
#             if registry.get("z") == 0:
#                 valid_numbers.append(i)
#             elif registry.get("z") < 0:
#                 print("less than:", registry.get("z"))
#             else:
#                 print("greater than:", registry.get("z"))
#
#     print(valid_numbers)
#     print("part1", max(valid_numbers))

#
# if __name__ == '__main__':
#     main()
