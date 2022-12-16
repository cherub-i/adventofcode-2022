import sys, os
import re

sys.path.insert(0, os.path.abspath("."))
from utils.Timer import Timer


def main():
    day = 1
    the_file = "test.txt"
    # the_file = "input.txt"

    # timer = Timer()

    pattern = re.compile(
        r"Sensor at x=(\d+), y=(\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    )
    with open(f"{day}/{the_file}", "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")

        while line != "":
            matches = pattern.findall(line)
            for match in matches:
                pass
            line = input_file.readline().replace("\n", "")
        line = input_file.readline().replace("\n", "")

    print("=== Part One ===")

    print("result")


if __name__ == "__main__":
    main()
