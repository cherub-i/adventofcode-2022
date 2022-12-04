import string

file = "3/input.txt"
#  file = "3/test.txt"


class Rucksack:
    def __init__(self, compartment_one_contents, compartment_two_contents):
        self.compartment_one = compartment_one_contents
        self.compartment_two = compartment_two_contents

    def get_first_wrong_item(self):
        for item in self.compartment_one:
            if item in self.compartment_two:
                return item

    def get_all_compartments(self):
        return self.compartment_one + self.compartment_two


def get_prio_by_char(char):
    if char in string.ascii_lowercase:
        return ord(char) - 96
    elif char in string.ascii_uppercase:
        return ord(char) - 38
    return 0


def main():
    rucksacks = list()

    with open(file, "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")

        while line != "":
            rucksacks.append(
                Rucksack(line[: len(line) // 2], line[len(line) // 2 :])
            )
            line = input_file.readline().replace("\n", "")

    sum_points = 0
    for rucksack in rucksacks:
        wrong_item = rucksack.get_first_wrong_item()
        points = get_prio_by_char(wrong_item)
        print(f"wrong item '{wrong_item}' worth {points}")
        sum_points += points
    print(f"wrong items in total are worth {sum_points}")

    print()
    print("=== Part Two ===")

    sum_points = 0
    for i in range(0, len(rucksacks), 3):
        r1_contents = rucksacks[i].get_all_compartments()
        r2_contents = rucksacks[i + 1].get_all_compartments()
        r3_contents = rucksacks[i + 2].get_all_compartments()

        for char in r1_contents:
            if char in r2_contents and char in r3_contents:
                break
        points = get_prio_by_char(char)
        print(f"first group has the badge '{char}', worth {points}")
        sum_points += points

    print(f"group badges in total are worth {sum_points}")


if __name__ == "__main__":
    main()
