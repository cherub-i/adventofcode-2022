from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


class MinMax:
    def __init__(self, value):
        self.min = value
        self.max = value

    def include(self, *values):
        for value in values:
            if value < self.min:
                self.min = value
            elif value > self.max:
                self.max = value

    def range(self):
        return abs(self.max - self.min + 1)


class Knot:
    def __init__(self):
        self._coord = Point(0, 0)
        self._x_minmax = MinMax(0)
        self._y_minmax = MinMax(0)
        self.position_list = list()
        self.position_list.append(self._coord)

    def move(self, direction):
        if direction == "L":
            self._coord.x -= 1
            self._x_minmax.include(self._coord.x)
        elif direction == "R":
            self._coord.x += 1
            self._x_minmax.include(self._coord.x)
        elif direction == "U":
            self._coord.y += 1
            self._y_minmax.include(self._coord.y)
        elif direction == "D":
            self._coord.y -= 1
            self._y_minmax.include(self._coord.y)
        else:
            raise ValueError(f"unknown direction: '{direction}'")
        self.position_list.append(Point(self._coord.x, self._coord.y))

    def follow(self, point):
        if not self._in_contact(point):
            dist_to_point_x = point.x - self._coord.x
            dist_to_point_y = point.y - self._coord.y
            if self._coord.x == point.x:
                self._coord.y += dist_to_point_y // 2
            elif self._coord.y == point.y:
                self._coord.x += dist_to_point_x // 2
            elif abs(dist_to_point_x) > abs(dist_to_point_y):
                self._coord.x += dist_to_point_x // 2
                self._coord.y = point.y
            elif abs(dist_to_point_x) < abs(dist_to_point_y):
                self._coord.x = point.x
                self._coord.y += dist_to_point_y // 2
            elif abs(dist_to_point_x) == abs(dist_to_point_y):
                self._coord.x += dist_to_point_x // 2
                self._coord.y += dist_to_point_y // 2
            else:
                raise RuntimeError(
                    f"unknown follow-constellation for lead: {point}, follower: {self._coord}"
                )
            self._x_minmax.include(self._coord.x)
            self._y_minmax.include(self._coord.y)
        self.position_list.append(Point(self._coord.x, self._coord.y))

    def _in_contact(self, point):
        return (
            abs(self._coord.x - point.x) <= 1
            and abs(self._coord.y - point.y) <= 1
        )


class Rope:
    def __init__(self, knots, screen_size_x=3, screen_size_y=3):
        self._knots = list()
        for i in range(knots):
            self._knots.append(Knot())
        self._screen = Screen(screen_size_x, screen_size_y)

    def move(self, direction):
        self._knots[0].move(direction)
        for i in range(1, len(self._knots)):
            self._knots[i].follow(self._knots[i - 1]._coord)

    def print(
        self,
        show_current,
        show_head_journey,
        show_tail_journey,
    ):
        x_minmax = MinMax(0)
        x_minmax.include(
            *[knot._x_minmax.min for knot in self._knots],
            *[knot._x_minmax.max for knot in self._knots],
        )
        y_minmax = MinMax(0)
        y_minmax.include(
            *[knot._y_minmax.min for knot in self._knots],
            *[knot._y_minmax.max for knot in self._knots],
        )
        self._screen.prepare(x_minmax, y_minmax)

        message = ""
        if show_current:
            self._screen.add_point(Point(0, 0), "s")
            self._screen.add_point(self._knots[0]._coord, "H")
            i = 1
            for knot in self._knots[1:]:
                self._screen.add_point(knot._coord, str(i))
                i += 1

        if show_head_journey:
            count = 0
            for point in self._knots[0].position_list:
                count += self._screen.add_point(point, "h")
                message = f"head visisted {count} different points"

        if show_tail_journey:
            count = 0
            for point in self._knots[-1].position_list:
                count += self._screen.add_point(point, "t")
                message = f"tail visisted {count} different points"

        self._screen.print()
        if message:
            print(message)


class Screen:
    def __init__(self, size_x, size_y):
        self._x_size = size_x
        self._y_size = size_y
        self._x_mm = MinMax(0)
        self._y_mm = MinMax(0)
        self._x_shift = 0
        self._y_shift = 0
        self._screen = list()

    def prepare(self, x_minmax, y_minmax, char="."):
        if self._x_size <= x_minmax.range():
            self._x_size = x_minmax.range()
        if self._y_size <= y_minmax.range():
            self._y_size = y_minmax.range()

        self._x_shift = -x_minmax.min
        self._y_shift = -y_minmax.min

        self._screen = [
            [char for col in range(self._x_size)]
            for row in range(self._y_size)
        ]

    def add_point(self, point, char):
        if (
            self._screen[point.y + self._y_shift][point.x + self._x_shift]
            != char
        ):
            self._screen[point.y + self._y_shift][
                point.x + self._x_shift
            ] = char
            return 1
        return 0

    def print(self):
        for row in reversed(self._screen):
            print("".join(row))


def main():
    file = "9/test.txt"
    file = "9/test2.txt"
    file = "9/input.txt"

    rope = Rope(10, 26, 21)

    print("=== Part One ===")
    with open(file, "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")

        while line != "":
            direction = line.split(" ")[0]
            distance = int(line.split(" ")[1])
            # print()
            # print(f"== {direction} {distance} ==")
            # print()
            for step in range(distance):
                rope.move(direction)
                # rope.print(True, False, False)
                # print()

            line = input_file.readline().replace("\n", "")

    print()
    rope.print(False, True, False)
    print()
    rope.print(False, False, True)


if __name__ == "__main__":
    main()
