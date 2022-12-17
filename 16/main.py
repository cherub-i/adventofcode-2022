import sys, os
import re

sys.path.insert(0, os.path.abspath("."))
from utils.Timer import Timer
from datastructures.Net import Net, Node, Edge


def main():
    day = 16
    the_file = "test.txt"
    # the_file = "input.txt"

    timer: Timer = Timer()
    # valve_list: dict[str, Valve] = dict()
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
    timer.max_no_iterations = 30
    current_position = "AA"

    time_left = 30
    pressure_drop = 0
    while time_left > 0:
        action_value_list: list[tuple[str, int, int]] = list()
        for node in net.node_list.values():
            time_to_node: int = (
                net.distance_dict[current_position][node.name] + 1
            )
            value: int = (time_left - time_to_node) * node.value
            if value > 0:
                action_value_list.append((node.name, value, time_to_node))
        action_value_list.sort(key=lambda x: x[1], reverse=True)
        if action_value_list:
            target_node_name = action_value_list[0][0]
            target_node_pressure_drop = action_value_list[0][1]
            target_node_time_taken = action_value_list[0][2]
            print(
                f"minute {30 - time_left}: moving to valve {target_node_name} and opening it, which takes {target_node_time_taken} minutes and yields {target_node_pressure_drop} pressure drop"
            )
            current_position = target_node_name
            net.get_node(target_node_name).value = 0
            time_left -= target_node_time_taken
            pressure_drop += target_node_pressure_drop
        else:
            time_left = 0
            print(
                f"minute {30 - time_left}: nothing more to be done in the remaining time"
            )

    print(f"total pressure drop is {pressure_drop}")


if __name__ == "__main__":
    main()
