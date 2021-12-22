from timeit import default_timer as timer

def char_to_bit(char):
    return 1 if char == '#' else 0

def bit_to_char(bit):
    return '.#'[bit]

class Image:
    def __init__(self, lines) -> None:
        self.image = [[char_to_bit(c) for c in line] for line in lines]
        self.void_fill = 0

        self.height = len(self.image)
        self.width = len(self.image[0])

    def get_window(self, i, j):
        """Get the values in the 3*3 window centred at i, j"""
        for x in range(i-1, i+2):
            for y in range(j-1, j+2):
                if x < 0 or x >= self.height or y < 0 or y >= self.height:
                    yield self.void_fill
                else:
                    yield self.image[x][y]

    def get_new_pixel(self, i, j, code):
        value = 0
        for x in self.get_window(i, j):
            value = (value << 1) | x
        return char_to_bit(code[value]) 

    def enhance(self, code):
        new_image = [[0] * (self.width + 2) for _ in range(self.height + 2)]
        for i, row in enumerate(new_image):
            for j in range(self.width + 2):
                new_image[i][j] = self.get_new_pixel(i - 1, j - 1, code)
        
        self.image = new_image
        self.void_fill = char_to_bit(code[self.void_fill * 511])
        self.height += 2
        self.width += 2

    def count_pixels(self):
        if self.void_fill == 1:
            return float('inf')

        return sum(sum(line) for line in self.image)

    def print(self):
        border = bit_to_char(self.void_fill)
        print(border * (self.width + 2))
        for line in self.image:
            print(border + ''.join(map(bit_to_char, line)) + border)
        print(border * (self.width + 2))

if __name__ == "__main__":
    start = timer()
    with open("input20.txt") as f:
        code, _, *image_lines = f.read().splitlines()

    image = Image(image_lines)

    print(f"There are {image.count_pixels()} pixels in the input.")
    for _ in range(2):
        image.enhance(code)
    print(
        f"After 2 enhancement(s) there are {image.count_pixels()} pixels in the image.\n"
    )

    for _ in range(48):
        image.enhance(code)
    print(
        f"After 50 enhancement(s) there are {image.count_pixels()} pixels in the image.\n"
    )
    


    print(f"Solution took {timer() - start:.3}s to complete.")
