import sys, os
import re

sys.path.insert(0, os.path.abspath("."))
from utils.Timer import Timer


class Valve:
    def __init__(self, name: str, flow_rate: int):
        self.name: str = name
        self.flow_rate: int = flow_rate
        self.adjacent_valve_list: list[Valve] = list()
        self.is_open: bool = False

    def add_adjacent_valve(self, valve: "Valve"):
        self.adjacent_valve_list.append(valve)


def main():
    day = 16
    the_file = "test.txt"
    # the_file = "input.txt"

    timer = Timer()
    valve_list: dict[str, Valve] = dict()
    connection_list: list[tuple] = list()

    pattern = re.compile(
        r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels lead to valves (.+)"
    )
    with open(f"{day}/{the_file}", "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")

        while line != "":
            matches = pattern.findall(line)
            for match in matches:
                valve_list[match[0]] = Valve(match[0], match[1])
                for target_valve_name in match[2].split(", "):
                    connection_list.append((match[0], target_valve_name))
            line = input_file.readline().replace("\n", "")

    for connection in connection_list:
        valve_list[connection[0]].add_adjacent_valve(connection[1])

    pressure_drop_total = 0
    timer.max_no_iterations = 30
    for time in range(0, 30):

        pressure_drop = 0
        for valve in valve_list.values():
            if valve.is_open:
                pressure_drop += valve.flow_rate
        pressure_drop_total += pressure_drop
        timer.print_iteration(time)
        print(
            f"      {pressure_drop} pressure drop in this minute / {pressure_drop_total} total pressure drop"
        )
        print()

    print("=== Part One ===")

    print("result")


if __name__ == "__main__":
    main()
