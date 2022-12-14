import numpy


class Sand:
    def __init__(self, position, scan):
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
            if self.scan.get_scan_at_position(target_location) == ".":
                self.scan.set_scan_at_position(self.position, ".")
                self.position = target_location
                self.scan.set_scan_at_position(target_location, "o")
                return
        self.scan.set_scan_at_position(self.position, "O")
        self.at_rest = True


class Scan:
    def __init__(self):
        self.rock_formation_list: list[tuple] = list()
        self.sand_source_location: tuple
        self.x_min: int = -1
        self.x_max: int = -1
        self.y_min: int = -1
        self.y_max: int = -1
        self.x_shift: int = 0
        self.data: numpy.ndarray

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

        self.x_shift = self.x_min - 1

        self.data: numpy.ndarray = numpy.chararray(
            (self.y_max + 1, (self.x_max - self.x_min) + 1 + 2)
        )
        self.data[:] = "."

        # sand
        self.set_scan_at_position(self.sand_source_location, "+")

        # rocks
        for start, end in self.rock_formation_list:
            # vertical
            if start[0] == end[0]:
                for i in range(
                    min(start[1], end[1]), max(start[1], end[1]) + 1
                ):
                    self.set_scan_at_position((start[0], i), "#")
            # horizontal
            elif start[1] == end[1]:
                for i in range(
                    min(start[0], end[0]), max(start[0], end[0]) + 1
                ):
                    self.set_scan_at_position((i, start[1]), "#")
            else:
                raise ValueError(f"unknown formation format: {start} - {end}")

    def set_scan_at_position(self, position: tuple, content: str):
        self.data[position[1], position[0] - self.x_shift] = content

    def get_scan_at_position(self, position: tuple):
        return chr(ord((self.data[position[1], position[0] - self.x_shift])))

    def __str__(self) -> str:
        content = ""
        for row in self.data:
            for element in row:
                content += chr(element[0])
            content += "\n"
        return content


class MainLoop:
    def __init__(self, scan):
        self.scan: Scan = scan
        self.sand_list: list[Sand] = list()

    def step(self):
        self.emit_sand()
        self.move_sand()

    def emit_sand(self) -> None:
        self.sand_list.append(Sand(self.scan.sand_source_location, self.scan))

    def move_sand(self) -> None:
        for sand in self.sand_list:
            while not sand.at_rest:
                sand.move()


def main():
    day = 14
    the_file = "test.txt"
    the_file = "input.txt"

    scan: Scan = Scan()

    with open(f"{day}/{the_file}", "r", encoding="utf-8") as input_file:
        for line in input_file.readlines():
            scan.add_rocks(line.replace("\n", ""))
    scan.add_sand_source((500, 0))

    scan.initialise()
    print(scan)

    print("=== Part One ===")
    main_loop: MainLoop = MainLoop(scan)
    try:
        while True:
            main_loop.step()
            # print(scan)
    except IndexError:
        print(scan)
        print(f"number {len(main_loop.sand_list)} fell off")


if __name__ == "__main__":
    main()
