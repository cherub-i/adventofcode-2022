import string

file = "4/input.txt"
# file = "4/test.txt"


class SectionRange:
    def __init__(self, start, end):
        self.start = int(start)
        self.end = int(end)

    def contains(self, other):
        if self.start <= other.start and self.end >= other.end:
            return True
        return False

    def overlaps(self, other):
        for n in range(self.start, self.end + 1):
            if n in range(other.start, other.end + 1):
                return True
        return False

    def __str__(self):
        return f"from {self.start} to {self.end}"


def main():
    print("=== Part One ===")
    with open(file, "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")

        range_count = 0
        while line != "":
            elf_one_range = SectionRange(
                line.split(",")[0].split("-")[0],
                line.split(",")[0].split("-")[1],
            )
            elf_two_range = SectionRange(
                line.split(",")[1].split("-")[0],
                line.split(",")[1].split("-")[1],
            )
            if elf_one_range.contains(elf_two_range):
                print(f"{elf_one_range} contains {elf_two_range}")
                range_count += 1
            elif elf_two_range.contains(elf_one_range):
                print(f"{elf_two_range} contains {elf_one_range}")
                range_count += 1
            line = input_file.readline().replace("\n", "")

    print(f"range-pairs where one fully contains the other: {range_count}")

    print("=== Part Two ===")
    with open(file, "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")

        overlap_sum = 0
        while line != "":
            elf_one_range = SectionRange(
                line.split(",")[0].split("-")[0],
                line.split(",")[0].split("-")[1],
            )
            elf_two_range = SectionRange(
                line.split(",")[1].split("-")[0],
                line.split(",")[1].split("-")[1],
            )
            if elf_one_range.overlaps(elf_two_range):
                print(f"{elf_one_range} and {elf_two_range} have overlap")
                overlap_sum += 1
            line = input_file.readline().replace("\n", "")

    print(f"range-pairs with overlap: {overlap_sum}")


if __name__ == "__main__":
    main()
