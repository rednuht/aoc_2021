import sys


def print_image(image):
    for row in image:
        print("".join(row))


def get_decoder_index(image, r, c, pad_pixel):
    rs = len(image[0])
    cs = len(image)
    decoder_index_bin = ""
    for rr in [-1, 0, 1]:
        for cc in [-1, 0, 1]:
            if 0 <= r + rr < rs and 0 <= c + cc < cs:
                p = image[r + rr][c + cc]
                decoder_index_bin += "0" if p == "." else "1"
            else:
                decoder_index_bin += "1" if pad_pixel == "#" else "0"
    return int(decoder_index_bin, 2)


def step(input_image, decoder, pad_pixel):
    output_image = []
    for r in range(-1, len(input_image) + 1):
        new_row = []
        for c in range(-1, len(input_image[0]) + 1):
            i = get_decoder_index(input_image, r, c, pad_pixel)
            new_row.append(decoder[i])
        output_image.append(new_row)
    return output_image


def main():
    decoder = sys.stdin.readline().strip()
    sys.stdin.readline()
    input_image = [list(line.strip()) for line in sys.stdin.readlines()]

    pad_pixel = "."
    for i in range(1, 50 + 1):
        input_image = step(input_image, decoder, pad_pixel)
        pad_pixel = decoder[0] if pad_pixel == "." else decoder[-1]
        if i == 2:
            lit_pixels = sum(row.count("#") for row in input_image)
            print("part1", lit_pixels)

    lit_pixels = sum(row.count("#") for row in input_image)
    print("part2", lit_pixels)


if __name__ == "__main__":
    main()
