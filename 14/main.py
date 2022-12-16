import sys, os
import numpy as np

sys.path.insert(0, os.path.abspath("."))
from datastructures import XYMatrix


class Sand:
    def __init__(self, position, scan: "Scan"):
        if scan.image.get_data(position) == "O":
            raise RuntimeError(
                f"Cannot set sand sand at {position}, that positionl is blocked by {scan.image.get_data(position)}"
            )
        self.position = position
        self.scan: Scan = scan
        self.at_rest = False

    def move(self) -> None:
        target_location_list: list[tuple] = list()
        target_location_list.append((self.position[0], self.position[1] + 1))
        target_location_list.append(
            (self.position[0] - 1, self.position[1] + 1)
        )
        target_location_list.append(
            (self.position[0] + 1, self.position[1] + 1)
        )

        for target_location in target_location_list:
            if self.scan.image.get_data(target_location) == ".":
                self.scan.image.set_data(self.position, ".")
                self.position = target_location
                self.scan.image.set_data(target_location, "o")
                return
        self.scan.image.set_data(self.position, "O")
        self.at_rest = True


class Scan:
    def __init__(self):
        self.rock_formation_list: list[tuple] = list()
        self.sand_source_location: tuple
        self.x_min: int = -1
        self.x_max: int = -1
        self.y_min: int = -1
        self.y_max: int = -1
        self.image: XYMatrix.XYMatrix

    def add_rocks(self, formation: str) -> None:
        from_location = formation.split(" -> ")[0]
        for part in formation.split(" -> ")[1:]:
            to_location = part
            self.rock_formation_list.append(
                (
                    ([int(coord) for coord in from_location.split(",")]),
                    ([int(coord) for coord in to_location.split(",")]),
                )
            )
            from_location = to_location

    def add_sand_source(self, sand_location: tuple) -> None:
        self.sand_source_location = sand_location

    def initialise(self) -> None:
        x_coordinate_list = [
            formation[0][0] for formation in self.rock_formation_list
        ]
        x_coordinate_list += [
            formation[1][0] for formation in self.rock_formation_list
        ]
        y_coordinate_list = [
            formation[0][1] for formation in self.rock_formation_list
        ]
        y_coordinate_list += [
            formation[1][1] for formation in self.rock_formation_list
        ]
        self.x_min = min(x_coordinate_list)
        self.x_max = max(x_coordinate_list)
        self.y_min = 0
        self.y_max = max(y_coordinate_list)

        self.image = XYMatrix.XYMatrix(
            (self.x_max - self.x_min + 1, self.y_max + 1)
        )
        self.image.x_shift = self.x_min
        self.image.print_line_numbers = True

        # sand
        self.image.set_data(self.sand_source_location, "+")

        # rocks
        for start, end in self.rock_formation_list:
            self.image.set_data_line(start, end, "#")

        # self.image.extend(["<", ">"], 1)

    def add_floor(self):
        self.image.extend(["v"], 2)
        self.image.set_data_line(
            (self.image.x_min, self.image.y_max),
            (self.image.x_max, self.image.y_max),
            "#",
        )

    def broaden(self, added_width_per_side: int):
        self.image.extend(["<", ">"], added_width_per_side)
        self.image.set_data_line(
            (self.image.x_min, self.image.y_max),
            (self.image.x_max, self.image.y_max),
            "#",
        )


class MainLoop:
    def __init__(self, scan):
        self.scan: Scan = scan
        self.sand_list: list[Sand] = list()

    def step(self) -> bool:
        try:
            self.emit_sand()
        except RuntimeError:
            print(
                f"failed to emit sand, {len(self.sand_list)} sand are present"
            )
            return False
        self.move_sand()
        return True

    def emit_sand(self) -> None:
        try:
            sand: Sand = Sand(self.scan.sand_source_location, self.scan)
            self.sand_list.append(sand)
        except RuntimeError:
            raise RuntimeError("failed to emit sand")

    def move_sand(self) -> None:
        for sand in self.sand_list:
            while not sand.at_rest:
                sand.move()


def main():
    day = 14
    the_file = "test.txt"
    the_file = "input.txt"

    print("=== Part One ===")
    scan: Scan = Scan()

    with open(f"{day}/{the_file}", "r", encoding="utf-8") as input_file:
        for line in input_file.readlines():
            scan.add_rocks(line.replace("\n", ""))
    scan.add_sand_source((500, 0))

    scan.initialise()
    for line in str(scan.image).split("\n"):
        print(line)

    main_loop: MainLoop = MainLoop(scan)
    try:
        while True:
            main_loop.step()
            # for line in str(scan.image).split("\n"):
            #     print(line)
    except IndexError:
        for line in str(scan.image).split("\n"):
            print(line)
        print(f"number {len(main_loop.sand_list)} fell off")

    print("=== Part Two ===")
    scan: Scan = Scan()

    with open(f"{day}/{the_file}", "r", encoding="utf-8") as input_file:
        for line in input_file.readlines():
            scan.add_rocks(line.replace("\n", ""))
    scan.add_sand_source((500, 0))

    scan.initialise()
    scan.add_floor()
    scan.broaden(200)

    for line in str(scan.image).split("\n"):
        print(line)

    main_loop: MainLoop = MainLoop(scan)
    i = 0
    try:
        while main_loop.step():
            # print(i)
            # if i % 500 == 0:
            #     for line in str(scan.image).split("\n"):
            #         print(line)
            i += 1
    except IndexError:
        print(i)
        for line in str(scan.image).split("\n"):
            print(line)
        print(f"number {len(main_loop.sand_list)} fell off")


if __name__ == "__main__":
    main()
