import sys, os
import re

sys.path.insert(0, os.path.abspath("."))
from utils.Timer import Timer
from datastructures.Net import *


class MainLoop:
    def __init__(self, net: Net):
        self.net: Net = net
        self.node_name_current: str = ""
        self.node_name_target: str = ""
        self.open_valve_list: list[tuple[str, int]] = list()
        self.pressure_drop_total = 0

    def step(self):
        self.calculate_pressure_drop()
        if self.node_name_target == "":
            self.find_target()
            path_finder = PathFinder(
                self.net.get_node(self.node_name_current),
                self.net.get_node(self.node_name_target),
            )
            path_finder.build_routes_to_target()
            self.path: Path = path_finder.path_list[0]
            self.path_at = 0
            print(f"determined path {self.path}, currently at {self.path_at}")

        if self.node_name_current == self.node_name_target:
            # at target, open valve
            self.open_valve_list.append(
                (
                    self.node_name_current,
                    self.net.get_node(self.node_name_target).value,
                )
            )
            print(
                f"opening valve {self.open_valve_list[-1][0]} will yield {self.open_valve_list[-1][1]}"
            )
            self.net.get_node(self.node_name_target).value = 0
            self.node_name_target = ""
        else:
            # move to target
            node_name_next = self.path.node_traveled_list[
                self.path_at + 1
            ].name
            print(f"moving from {self.node_name_current} to {node_name_next}")

            self.node_name_current = node_name_next
            self.path_at += 1
        print(f"pressure drop now is: {self.pressure_drop_total}")

    def find_target(self):
        node_list = self.get_node_list_by_value()
        self.node_name_target = node_list[0].name

    def calculate_pressure_drop(self):
        for valve_name, valve_pressure_drop in self.open_valve_list:
            self.pressure_drop_total += valve_pressure_drop

    def get_node_list_by_value(self) -> list[Node]:
        node_list_by_value: list[Node] = list()
        for node in self.net.node_list.values():
            node_list_by_value.append(node)
        node_list_by_value.sort(key=lambda x: x.value, reverse=True)
        return node_list_by_value


def main():
    day = 16
    the_file = "test.txt"
    # the_file = "input.txt"

    timer: Timer = Timer()
    net: Net = Net()
    connection_list: list[tuple] = list()

    pattern = re.compile(
        r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)"
    )
    with open(f"{day}/{the_file}", "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")

        while line != "":
            matches = pattern.findall(line)
            for match in matches:
                net.add_node(Node(match[0], int(match[1]), 0))
                for target_valve_name in match[2].split(", "):
                    connection_list.append((match[0], target_valve_name))
            line = input_file.readline().replace("\n", "")

    for connection in connection_list:
        net.add_edge(connection[0], connection[1], 0, 1)

    main_loop: MainLoop = MainLoop(net)
    main_loop.node_name_current = "AA"

    timer.max_no_iterations = 30
    for time in range(0, 30):
        timer.print_iteration(time)
        main_loop.step()

    print("=== Part One ===")

    print("result")


if __name__ == "__main__":
    main()
