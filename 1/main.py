class Elf:
    def __init__(self, number):
        self.number = number
        self.calories = list()
        self.calories_sum = 0

    def add_calory(self, calory):
        self.calories.append(calory)
        self.calories_sum += calory


def main():
    elfs = list()
    elf_count = 0

    with open("1/input.txt", "r", encoding="utf-8") as input_file:
        line = input_file.readline()
        elf_count += 1
        elf = Elf(elf_count)
        while line != "":
            if line != "\n":
                elf.add_calory(int(line.strip()))
            else:
                elfs.append(elf)
                elf_count += 1
                elf = Elf(elf_count)
            line = input_file.readline()
        elfs.append(elf)

    print("all elfs:")
    for elf in elfs:
        print(f"elf {elf.number:3}: {elf.calories_sum:5}")

    print()
    elfs.sort(key=lambda x: x.calories_sum, reverse=True)
    print("most calories")
    print(f"elf {elfs[0].number:3}: {elfs[0].calories_sum:5}")

    print()
    print("sum of top 3 calories")
    print(f"elf {elfs[0].number:3}: {elfs[0].calories_sum:5}")
    print(f"elf {elfs[1].number:3}: {elfs[1].calories_sum:5}")
    print(f"elf {elfs[2].number:3}: {elfs[2].calories_sum:5}")
    top_3_calories_sum = (
        elfs[0].calories_sum + elfs[1].calories_sum + elfs[2].calories_sum
    )
    print(f"{top_3_calories_sum}")


if __name__ == "__main__":
    main()
