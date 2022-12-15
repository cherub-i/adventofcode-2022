import sys, os
import numpy as np
import re

sys.path.insert(0, os.path.abspath("."))
from utils.DataStructures import XYMatrix


class Sensor:
    def __init__(self, position, position_closest_beacon):
        self.position: tuple = position
        self.position_closest_beacon: tuple = position_closest_beacon
        self.distance_to_closest_beacon = XYMatrix.manhatten_distance(
            self.position, self.position_closest_beacon
        )
        self.covered_area: list[tuple] = list()
        # self.calculate_covered_area()

    def calculate_covered_area(self):
        for x in range(
            self.position[0] - self.distance_to_closest_beacon,
            self.position[0] + self.distance_to_closest_beacon + 1,
        ):
            for y in range(
                self.position[1] - self.distance_to_closest_beacon,
                self.position[1] + self.distance_to_closest_beacon + 1,
            ):
                if (
                    XYMatrix.manhatten_distance(self.position, (x, y))
                    <= self.distance_to_closest_beacon
                ):
                    self.covered_area.append((x, y))

    def __str__(self):
        return f"Sensor at {self.position}, capped in {self.distance_to_closest_beacon}, by beacon at {self.position_closest_beacon}"


def main():
    day = 15
    the_file = "test.txt"
    y_requested: int = 10
    xy_min = 0
    xy_max = 20

    the_file = "input.txt"
    y_requested: int = 2000000
    xy_min = 0
    xy_max = 4000000

    pattern = re.compile(
        r"Sensor at x=(\d+), y=(\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    )

    sensor_list: list[Sensor] = list()

    with open(f"{day}/{the_file}", "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")
        while line != "":
            matches = pattern.findall(line)
            for match in matches:
                sensor_list.append(
                    Sensor(
                        (int(match[0]), int(match[1])),
                        (int(match[2]), int(match[3])),
                    )
                )
            line = input_file.readline().replace("\n", "")

    if False:
        print("=== Part One ===")
        relevant_sensor_list: list[Sensor] = list()
        for sensor in sensor_list:
            if (
                sensor.position[1] - sensor.distance_to_closest_beacon
                <= y_requested
                <= sensor.position[1] + sensor.distance_to_closest_beacon
            ):
                relevant_sensor_list.append(sensor)
        print(f"found {len(relevant_sensor_list)} relevant sensors:")
        for sensor in relevant_sensor_list:
            print(sensor)

        x_min = min(
            [
                sensor.position[0] - sensor.distance_to_closest_beacon
                for sensor in relevant_sensor_list
            ]
        )
        x_max = max(
            [
                sensor.position[0] + sensor.distance_to_closest_beacon
                for sensor in relevant_sensor_list
            ]
        )

        print(f"checking in line {y_requested} from {x_min} to {x_max}")
        x_covered_count: int = 0
        x_sensor_count: int = 0
        x_beacon_count: int = 0
        for x in range(x_min, x_max + 1):
            for sensor in relevant_sensor_list:
                if (
                    XYMatrix.manhatten_distance(
                        sensor.position, (x, y_requested)
                    )
                    <= sensor.distance_to_closest_beacon
                ):
                    x_covered_count += 1
                    if (x, y_requested) == sensor.position:
                        x_sensor_count += 1
                    if (x, y_requested) == sensor.position_closest_beacon:
                        x_beacon_count += 1
                    break

        print(
            f"{x_covered_count} covered by sensors (thereof {x_sensor_count} sensors and {x_beacon_count} beacons)"
        )

    print("=== Part Two ===")
    relevant_sensor_list: list[Sensor] = list()
    for sensor in sensor_list:
        if (
            sensor.position[1] - sensor.distance_to_closest_beacon >= xy_min
            or sensor.position[1] + sensor.distance_to_closest_beacon <= xy_max
        ) and (
            sensor.position[0] - sensor.distance_to_closest_beacon >= xy_min
            or sensor.position[0] + sensor.distance_to_closest_beacon <= xy_max
        ):
            relevant_sensor_list.append(sensor)
    print(f"found {len(relevant_sensor_list)} relevant sensors:")
    for sensor in relevant_sensor_list:
        print(sensor)

    x = 0
    y = 0
    found = False
    for y in range(xy_min, xy_max + 1):
        if y % 100 == 0:
            print(f"{y/xy_max:.2f}%")
        for x in range(xy_min, xy_max + 1):
            found = True
            for sensor in relevant_sensor_list:
                distance_to_sensor = XYMatrix.manhatten_distance(
                    sensor.position, (x, y)
                )
                if distance_to_sensor <= sensor.distance_to_closest_beacon:
                    found = False
                    break
            if found:
                break
        if found:
            break

    print(f"uncovered spot at ({x}, {y})")
    print(f"tune to {x * 4000000 + y}")


if __name__ == "__main__":
    main()
