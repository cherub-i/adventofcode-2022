import re


class MainLoop:
    def __init__(
        self, valve_list: list["Valve"], valve_start: "Valve", time_max: int
    ):
        self.valve_dict: dict[Valve] = valve_list
        self.valve_current: Valve = valve_start
        self.time_max = time_max
        self.valve_target: Valve = None
        self.pressure_release_total: int = 0
        self.time_current = 0

    @property
    def time_left(self) -> int:
        return self.time_max - self.time_current

    def step(self) -> None:
        self.yield_open_valves()
        print(f"== Minute {self.time_current + 1} ==")
        print(
            f"Open valves: {', '.join([valve.name for valve in self.valve_dict.values() if valve.is_open])}"
        )
        print(f"I am at {self.valve_current.name}")

        adjacent_valve_value_list = self.get_adjacent_valve_value_list()
        max_move_value: int = 0
        if len(adjacent_valve_value_list) > 0:
            max_move_value = adjacent_valve_value_list[0][0]
            current_valve_value = self.valve_current.value_over_duration(
                self.time_left - 1
            )
            if current_valve_value > max_move_value:
                print(f"  opening valve: {self.valve_current.name}")
                self.valve_current.is_open = True
            else:
                print(f"  moving to: {adjacent_valve_value_list[0][1].name}")
                self.valve_current = adjacent_valve_value_list[0][1]
        else:
            print(f"nowhere to go")

        self.time_current += 1
        print(f"  pressure release up to now: {self.pressure_release_total}")

    def yield_open_valves(self) -> None:
        pressure_release = 0
        for valve in self.valve_dict.values():
            if valve.is_open:
                pressure_release += valve.flow_rate
        self.pressure_release_total += pressure_release

    def get_adjacent_valve_value_list(self) -> list[tuple[int, "Valve"]]:
        adjacent_valve_value_list: list[tuple[int, Valve]] = list()
        for next_valve_name in self.valve_current.adjacent_valve_list:
            next_valve = self.valve_dict[next_valve_name]
            value: int = next_valve.value_over_duration(self.time_left - 1)
            for next_valve_child_name in next_valve.adjacent_valve_list:
                next_valve_child = self.valve_dict[next_valve_child_name]
                if next_valve_child != self.valve_current:
                    value_incl_child = (
                        value
                        + next_valve_child.value_over_duration(
                            self.time_left - 1 - 2
                        )
                    )
                    if value_incl_child > value:
                        value = value_incl_child
            adjacent_valve_value_list.append((value, next_valve))
        adjacent_valve_value_list.sort(key=lambda x: x[0], reverse=True)
        return adjacent_valve_value_list


class Valve:
    def __init__(self, name: str, flow_rate: int):
        self.name: str = name
        self.flow_rate: int = flow_rate
        self.adjacent_valve_list: list[Valve] = list()
        self.is_open: bool = False

    def add_adjacent_valve(self, valve: "Valve"):
        self.adjacent_valve_list.append(valve)

    def value_over_duration(self, duration: int) -> int:
        if self.is_open:
            return 0
        return self.flow_rate * duration


def main():
    day = 16
    the_file = "test.txt"
    # the_file = "input.txt"

    valve_dict: dict[str, Valve] = dict()
    connection_list: list[tuple] = list()

    pattern = re.compile(
        r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)"
    )
    with open(f"{day}/{the_file}", "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")

        while line != "":
            matches = pattern.findall(line)
            for match in matches:
                valve_dict[match[0]] = Valve(match[0], int(match[1]))
                for target_valve_name in match[2].split(", "):
                    connection_list.append((match[0], target_valve_name))
            line = input_file.readline().replace("\n", "")

    for connection in connection_list:
        valve_dict[connection[0]].add_adjacent_valve(connection[1])

    print("=== Part One ===")
    main_loop: MainLoop = MainLoop(valve_dict, valve_dict["AA"], 30)

    while main_loop.time_left > 0:
        main_loop.step()

    print(f"total pressure drop is {main_loop.pressure_release_total}")


if __name__ == "__main__":
    main()
