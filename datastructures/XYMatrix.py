import numpy as np


class XYMatrix:
    valid_direction_list = ["^", "v", "<", ">"]

    def __init__(self, size: tuple = (0, 0), initial_content: str = "."):
        if not XYMatrix.is_content_valid(initial_content):
            raise ValueError(f"content is invalid: '{initial_content}'")
        self.data = np.chararray((size[1], size[0]))
        self.initial_content: str = initial_content
        self.data[:] = self.initial_content
        self.x_shift: int = 0
        self.y_shift: int = 0
        self.x_size: int = size[0]
        self.y_size: int = size[1]
        self.print_line_numbers: bool = False

    @property
    def x_min(self):
        return 0 + self.x_shift

    @property
    def y_min(self):
        return 0 + self.y_shift

    @property
    def x_max(self):
        return self.x_size + self.x_shift - 1

    @property
    def y_max(self):
        return self.y_size + self.y_shift - 1

    def extend(self, direction_list: list[str], amount):
        for direction in direction_list:
            if direction not in XYMatrix.valid_direction_list:
                raise ValueError(f"direction is invalid: '{direction}")

            if direction in ["^", "v"]:
                self.y_size += amount
            elif direction in ["<", ">"]:
                self.x_size += amount
            new_data = np.chararray((self.y_size, self.x_size))
            new_data[:] = self.initial_content

            if direction == "^":
                self.y_shift -= amount
                new_data[amount:] = self.data[:]
            elif direction == "v":
                new_data[: self.data.shape[0]] = self.data[:]
            elif direction == "<":
                self.x_shift -= amount
                for i, row in enumerate(new_data):
                    row[amount:] = self.data[i]
            elif direction == ">":
                for i, row in enumerate(new_data):
                    row[: self.data.shape[1]] = self.data[i]
            self.data = new_data

    def set_data(self, position: tuple, content: str) -> None:
        self.check_positions([position])
        self.data[
            position[1] - self.y_shift, position[0] - self.x_shift
        ] = content

    def set_data_line(self, start: tuple, end: tuple, content: str) -> None:
        self.check_positions([start, end])
        ordered_start = (
            min(start[0], end[0]),
            min(start[1], end[1]),
        )
        ordered_end = (
            max(start[0], end[0]),
            max(start[1], end[1]),
        )

        # vertical
        if ordered_start[0] == ordered_end[0]:
            for i in range(ordered_start[1], ordered_end[1] + 1):
                self.set_data((ordered_start[0], i), content)
        # horizontal
        elif ordered_start[1] == ordered_end[1]:
            for i in range(ordered_start[0], ordered_end[0] + 1):
                self.set_data((i, ordered_start[1]), content)
        else:
            raise ValueError(
                f"invalid line configuration from {start} to {end}"
            )

    def get_data(self, position: tuple):
        self.check_positions([position])
        return chr(
            ord(
                (
                    self.data[
                        position[1] - self.y_shift, position[0] - self.x_shift
                    ]
                )
            )
        )

    def check_positions(self, position_list: list[tuple]) -> None:
        for position in position_list:
            if not self.contains(position):
                raise IndexError(
                    f"Position {position} is not part of the matrix with top left: ({self.x_min}, {self.y_min}) and bottom right:  ({self.x_max}, {self.y_max})"
                )

    def contains(self, position: tuple) -> bool:
        if (
            self.x_min <= position[0] <= self.x_max
            and self.y_min <= position[1] <= self.y_max
        ):
            return True
        return False

    def __str__(self) -> str:
        line_number_width = len(str(self.y_max))
        line_number_height = len(str(self.x_max))
        content = ""

        if self.print_line_numbers:
            header_prefix = " " * line_number_width + "  "
            header: list = list()
            for row_number in range(line_number_height):
                header_line = ""
                for col_number in range(self.data.shape[1]):
                    header_line += str(col_number + self.x_shift).rjust(
                        line_number_height
                    )[-(row_number + 1)]
                header.append(header_prefix + header_line)

            header.reverse()
            for line in header:
                content += line + "\n"

        for row_number, row in enumerate(self.data):
            if self.print_line_numbers:
                content += (
                    str(row_number + self.y_shift).rjust(line_number_width)
                    + ": "
                )
            for element in row:
                content += chr(element[0])
            content += "\n"
        return content

    @classmethod
    def is_content_valid(cls, content: str) -> bool:
        return content != " " and len(content) == 1

    @staticmethod
    def distance(point_a, point_b) -> tuple[int, int, int]:
        x_distance = abs(point_a[0] - point_b[0])
        y_distance = abs(point_a[1] - point_b[1])
        return x_distance, y_distance, x_distance + y_distance


def main():
    test: XYMatrix = XYMatrix((3, 3), ".")
    print(test)

    test.set_data((1, 1), "x")
    print(test)

    test.print_line_numbers = True
    print(test)

    test.x_shift = 10
    test.y_shift = 100
    print(test)

    test.set_data((12, 102), "!")
    print(test)

    test.extend(["^", "v", "<", ">"], 2)
    print(test)

    test.set_data((14, 104), "@")
    print(test)

    test.set_data_line((8, 98), (14, 98), "-")
    print(test)

    test.set_data_line((8, 98), (8, 104), "|")
    print(test)


if __name__ == "__main__":
    main()
