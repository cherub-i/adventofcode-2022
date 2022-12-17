import sys, os
import re

sys.path.insert(0, os.path.abspath("."))
from utils.Timer import Timer
from datastructures.Net import Net, Node, Edge, Path


class MainLoop:
    def __init__(self, net: Net, node_name_start: str, time_max: int):
        self.net: Net = net
        self.node_name_current: str = node_name_start
        self.time_max = time_max
        self.node_name_target: str = ""
        self.path_to_target: Path = None
        self.open_valve_list: list[int] = list()
        self.pressure_release_total: int = 0
        self.time_current = 0

    @property
    def time_left(self) -> int:
        return self.time_max - self.time_current

    def step(self) -> None:
        self.yield_open_valves()
        print(
            f"minute {self.time_current:2}: I am at {self.node_name_current}"
        )
        if self.node_name_target == "":
            path_to_target = self.find_target()
            if path_to_target is not None:
                self.path_to_target = self.find_target()
                self.node_name_target = self.path_to_target.end().name
                print(f"  set new target path: {self.path_to_target}")
            else:
                self.node_name_target = "STOP"
                print(f"  no new targets")

        node_current: Node = self.net.get_node(self.node_name_current)
        if self.node_name_target == "STOP":
            print(f"  waiting for end")
        elif node_current.name == self.node_name_target:
            # at target
            print(f"  opening valve at target: {self.node_name_current}")
            self.node_name_target = ""
            self.path_to_target = None

            self.open_valve_list.append(node_current.value)
            node_current.value = 0
        elif node_current.value > 0:
            # I am at a position with a closed valve, which yields
            print(f"  opening valve at: {self.node_name_current}")
            self.open_valve_list.append(node_current.value)
            node_current.value = 0
        else:
            # nothing to do here, move to next node
            node_name_next = "unknown"
            for i, node in enumerate(self.path_to_target.node_list):
                if node == node_current:
                    node_name_next = self.path_to_target.node_list[i + 1].name
                    break
            print(f"  moving to: {node_name_next}")
            self.node_name_current = node_name_next

        self.time_current += 1
        print(f"  pressure release up to now: {self.pressure_release_total}")

    def yield_open_valves(self) -> None:
        for pressure_release in self.open_valve_list:
            self.pressure_release_total += pressure_release

    def find_target(self) -> Path:
        node_value_list: list[tuple[int, Path]] = list()
        for node in self.net.node_list.values():
            if node.name in self.net.distance_dict[self.node_name_current]:
                path_to_node: Path = self.net.distance_dict[
                    self.node_name_current
                ][node.name]
                value_of_node: int = (
                    self.time_left - path_to_node.cost - 1
                ) * node.value
                if value_of_node > 0:
                    node_value_list.append((value_of_node, path_to_node))
        node_value_list.sort(key=lambda x: x[0], reverse=True)
        if len(node_value_list) == 0:
            return None
        return node_value_list[0][1]


def main():
    day = 16
    the_file = "test.txt"
    # the_file = "input.txt"

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
                net.add_node(Node(match[0], int(match[1])))
                for target_valve_name in match[2].split(", "):
                    connection_list.append((match[0], target_valve_name))
            line = input_file.readline().replace("\n", "")

    for connection in connection_list:
        net.add_edge(connection[0], connection[1], 0, 1)

    net.calculate_path_list()

    print("=== Part One ===")
    main_loop: MainLoop = MainLoop(net, "AA", 30)

    while main_loop.time_left > 0:
        main_loop.step()

    print(f"total pressure drop is {main_loop.pressure_release_total}")


if __name__ == "__main__":
    main()
