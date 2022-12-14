from dataclasses import dataclass
import numpy
import time
import copy


@dataclass
class DirectionToTarget:
    direction: str
    distance: int


class Terrain:
    def __init__(self, terrain_as_lines: list):
        self.landscape: numpy.ndarray = numpy.array(terrain_as_lines)
        self.start: tuple = numpy.where(self.landscape == "S")
        self.destination: tuple = numpy.where(self.landscape == "E")
        self.cells: int = self.landscape.shape[0] * self.landscape.shape[1]
        self.cells_with_4_directions: int = (self.landscape.shape[0] - 1) * (
            self.landscape.shape[1] - 1
        )
        self.cells_with_3_directions: int = (
            (2 * self.landscape.shape[0])
            - 4
            + (2 * self.landscape.shape[1])
            - 4
        )
        self.cells_with_2_directions: int = 4
        self.cell_directions: int = (
            (self.cells_with_2_directions * 2)
            + (self.cells_with_3_directions * 3)
            + (self.cells_with_4_directions * 4)
        )

    def __str__(self):
        content: str = ""
        for row in self.landscape:
            content += "".join(row) + "\n"
        return content

    def get_elevation(self, pos: tuple) -> int:
        return ord(self.landscape[pos][0].replace("S", "a").replace("E", "z"))

    def contains(self, pos: tuple) -> bool:
        if min(pos) < 0:
            return False
        if pos[0] >= self.landscape.shape[0]:
            return False
        if pos[1] >= self.landscape.shape[1]:
            return False
        return True

    def set_cell(self, pos: tuple, char: str):
        self.landscape[pos] = char

    def get_char_count(self, char: str):
        return numpy.count_nonzero(self.landscape == char)


class Route:
    def __init__(self, terrain: Terrain):
        self.terrain: Terrain = terrain
        self.current: tuple = terrain.start
        self.coordinate_list: list = list()
        self.coordinate_list.append(self.current)
        self.elevation_list: list = list()
        self.move_list: list = list()
        self.steps: int = 0
        self.direction_list: list = list()
        self.rate_directions()

    def step(self, routes: list, visited_locations: dict) -> None:
        for direction in [d.direction for d in self.direction_list]:
            next_step = self.move(direction)
            # print(f"trying {direction}: ", end="")
            if self.valid_step(next_step) and not self.been_there(next_step):
                next_step_key = Route.key(direction, next_step)
                next_step_reached_in = visited_locations.get(next_step_key, -1)
                if (
                    next_step_reached_in == -1
                    or self.steps + 1 < next_step_reached_in
                ):
                    visited_locations[next_step_key] = self.steps + 1
                    routes.append(self.branch_off(next_step, direction))

    def been_there(self, pos) -> bool:
        if self.steps >= 2 and pos == self.coordinate_list[-2]:
            return True
        if pos in self.coordinate_list:
            return True
        return False

    def add_step(self, step: tuple, direction_taken: str) -> None:
        self.coordinate_list.append(step)
        self.elevation_list.append(chr(self.terrain.get_elevation(step)))
        self.move_list.append(direction_taken)
        self.steps += 1
        self.current = step
        self.rate_directions()

    def rate_directions(self) -> None:
        self.direction_list = list()
        self.direction_list.append(
            DirectionToTarget(
                "^", -(self.terrain.destination[0][0] - self.current[0][0])
            )
        )
        self.direction_list.append(
            DirectionToTarget(
                ">", self.terrain.destination[1][0] - self.current[1][0]
            )
        )
        self.direction_list.append(
            DirectionToTarget(
                "<", -(self.terrain.destination[1][0] - self.current[1][0])
            )
        )
        self.direction_list.append(
            DirectionToTarget(
                "v", self.terrain.destination[0][0] - self.current[0][0]
            )
        )
        self.direction_list.sort(key=lambda x: x.distance)

    def branch_off(self, next_step, direction) -> "Route":
        branch: Route = Route(self.terrain)
        branch.coordinate_list = self.coordinate_list.copy()
        branch.elevation_list = self.elevation_list.copy()
        branch.move_list = self.move_list.copy()
        branch.steps = self.steps
        branch.add_step(next_step, direction)
        return branch

    def has_arrived(self) -> bool:
        if self.terrain.destination != self.current:
            return False
        return True

    def move(self, direction: str) -> tuple:
        if direction == "^":
            return (self.current[0] - 1, self.current[1])
        elif direction == "v":
            return (self.current[0] + 1, self.current[1])
        elif direction == "<":
            return (self.current[0], self.current[1] - 1)
        elif direction == ">":
            return (self.current[0], self.current[1] + 1)
        else:
            raise NameError(f"unknown direction: '{direction}")

    def valid_step(self, target: tuple) -> bool:
        if not self.terrain.contains(target):
            return False
        if self.terrain.get_elevation(
            self.current
        ) + 1 < self.terrain.get_elevation(target):
            return False
        return True

    def __str__(self) -> str:
        return f"{''.join(self.move_list)} / {''.join(self.elevation_list)} in {self.steps} steps"

    @classmethod
    def key(cls, direction: str, pos: tuple) -> str:
        # return f"{direction}_{pos[0][0]},{pos[1][0]}"
        return f"{pos[0][0]},{pos[1][0]}"


class Navi:
    def __init__(self, terrain: Terrain):
        self.terrain: Terrain = terrain
        self.covered_terrain: Terrain = copy.deepcopy(terrain)
        self.route_list: list = list()
        self.route_to_destination_list: list = list()
        self.visited_location_dict: dict = dict()
        self.least_moves: int = -1
        self.iterations: int = 0
        self.reduced_by_longer_than_shortest: int = 0
        self.status_interval: int = 500

        self.time_start = time.process_time()

        self.route_list.append(Route(terrain))

    def has_routes(self) -> bool:
        return len(self.route_list) > 0

    def process_routes(self):
        self.iterations += 1

        route_processing_list: list = list()
        while self.route_list:
            route_processing_list.append(self.route_list.pop())

        while route_processing_list:
            route_processing_list.pop().step(
                self.route_list, self.visited_location_dict
            )

        for route in self.route_list:
            self.covered_terrain.set_cell(route.current, ".")

            # remove route, if it has reached its destination
            if route.has_arrived():
                self.least_moves = route.steps
                self.route_to_destination_list.append(route)
                self.route_list.remove(route)
            # remove route, if it is already longer than the best solution
            elif self.is_longer_or_equal_than_solution(route):
                self.route_list.remove(route)

        if self.iterations == 1 or self.iterations % self.status_interval == 0:
            self.print_status()

    def print_status(self) -> None:
        visited_cells = self.covered_terrain.get_char_count(".")
        visited_locations = len(self.visited_location_dict)
        print(f"# {Navi.pretty_time(time.process_time() - self.time_start)}")
        print(
            f"Iteration {self.iterations:6}: {len(self.route_list):4} routes are active. ",
            end="",
        )
        print(
            f"Visited {visited_cells:4} cells, out of {self.terrain.cells:4} ({visited_cells/self.terrain.cells*100:.1f}%). ",
            end="",
        )
        print(
            f"Learned {visited_locations:5} shortest routes, out of {self.terrain.cell_directions:5} ({visited_locations/self.terrain.cell_directions*100:.1f}%)",
            end="",
        )
        print()
        if self.route_to_destination_list:
            print(
                f"⭐ Found {len(self.route_to_destination_list):2} to destination, shortest is {self.least_moves}."
            )
            print()
        print(self.covered_terrain)
        print()

    def print_solutions(self) -> None:
        print("Shortest routes: ")
        self.route_to_destination_list.sort(key=lambda x: (x.steps))
        for route in self.route_to_destination_list:
            print(f"{route}")

    def is_longer_or_equal_than_solution(self, route: Route) -> bool:
        return self.least_moves != -1 and route.steps >= self.least_moves

    @classmethod
    def pretty_time(cls, the_time) -> str:
        return f"{the_time:.4f}"


def main():
    the_file = "12/test.txt"
    the_file = "12/test2.txt"
    the_file = "12/input.txt"

    print("=== Part One ===")
    with open(the_file, "r", encoding="utf-8") as input_file:
        terrain: Terrain = Terrain(
            [list(line.replace("\n", "")) for line in input_file.readlines()]
        )

    navi: Navi = Navi(terrain)
    navi.status_interval = 10

    while navi.has_routes():
        navi.process_routes()

    print("--- done ----")
    navi.print_status()
    print()
    navi.print_solutions()


if __name__ == "__main__":
    main()
