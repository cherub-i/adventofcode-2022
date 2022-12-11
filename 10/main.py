class SpriteLine:
    def __init__(self):
        self._line = list()

    def set(self, pos):
        self._line = [" " for i in range(40)]
        for i in range(pos - 1, pos + 2):
            if i < len(self._line) and i >= 0:
                self._line[i] = "#"

    def printAt(self, i):
        print(self._line[i % 40], end="")

    def content(self):
        return "".join(self._line)

    def print(self):
        print(self.content())


class Cycle:
    def __init__(self):
        self.i = 0
        self.x = 1
        self.x_at_cycle = list()
        self.sprite_line = SpriteLine()
        self.sprite_line.set(self.x)

    def execute(self):
        self.x_at_cycle.append(self.x)
        # print(f"{self.x:2} : {self.sprite_line.content()}")
        self.sprite_line.printAt(self.i)
        if self.i != 0 and (self.i + 1) % 40 == 0:
            print("")
        self.i += 1

    def add_x(self, value):
        self.x += value
        self.sprite_line.set(self.x)

    def print_signal_strenght(self):
        total_signal_strength = 0
        for i in range(20, len(self.x_at_cycle), 40):
            x = self.x_at_cycle[i - 1]
            signal_strength = x * i
            print(f"at cycle {i}, x is {x} - resulting in {signal_strength}")
            total_signal_strength += signal_strength
        print(f"total signal strength is {total_signal_strength}")


def main():
    # file = "10/test.txt"
    file = "10/input.txt"

    cycle = Cycle()

    print("=== Part Two ===")
    with open(file, "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")

        i = 0
        while line != "":
            if line == "noop":
                cycle.execute()
            elif line.startswith("addx "):
                cycle.execute()
                cycle.execute()
                cycle.add_x(int(line.split(" ")[1]))

            line = input_file.readline().replace("\n", "")

    print("=== Part One ===")
    cycle.print_signal_strenght()


if __name__ == "__main__":
    main()
