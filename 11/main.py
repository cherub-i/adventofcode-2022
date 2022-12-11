class Monkey:
    def __init__(self, name):
        self.name = name
        self.inspect_operation = ""
        self.modulo = 1
        self.target_if_true = 0
        self.target_if_false = 0
        self.inspections = 0

    def set_items(self, worry_levels_as_comma_separated):
        self.items = [
            int(worry_level.strip())
            for worry_level in worry_levels_as_comma_separated.split(",")
        ]

    def set_inspect_operation(self, op_as_text):
        self.inspect_operation = lambda old: eval(op_as_text)

    def start_round(self):
        self.items_in_round = self.items.copy()
        self.items = list()

    def process_item(self, item_index, reduce_op="item // 3"):
        reduce_function = lambda item: eval(reduce_op)
        self.inspections += 1
        item = self.items_in_round[item_index]
        item = self.inspect_operation(item)
        item = reduce_function(item)
        if item % self.modulo == 0:
            return item, self.target_if_true
        else:
            return item, self.target_if_false

    def __str__(self):
        return f"Monkey {self.name:2}: {', '.join([str(item) for item in self.items])}"


def main():
    the_file = "11/test.txt"
    the_file = "11/input.txt"

    monkeys = list()

    with open(the_file, "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")

        while line != "":
            if line.startswith("Monkey "):
                current_monkey = Monkey(line.split(" ")[1].replace(":", ""))
                monkeys.append(current_monkey)
                line = input_file.readline().replace("\n", "")
                current_monkey.set_items(line.split(": ")[1])
                line = input_file.readline().replace("\n", "")
                current_monkey.set_inspect_operation(line.split("new = ")[1])
                line = input_file.readline().replace("\n", "")
                current_monkey.modulo = int(line.split("divisible by")[1])
                line = input_file.readline().replace("\n", "")
                current_monkey.target_if_true = int(
                    line.split("throw to monkey ")[1]
                )
                line = input_file.readline().replace("\n", "")
                current_monkey.target_if_false = int(
                    line.split("throw to monkey ")[1]
                )
                line = input_file.readline().replace("\n", "")
            elif line == "":
                pass
            else:
                raise ValueError(f"line not parsable: '{line}'")

            line = input_file.readline().replace("\n", "")

    if False:
        print("=== Part One ===")
        for round in range(1, 21):
            print(f"Round {round}")
            for monkey in monkeys:
                monkey.start_round()
                for i in range(len(monkey.items_in_round)):
                    item, target = monkey.process_item(i)
                    monkeys[target].items.append(item)
                    # print(
                    #     f"monkey {monkey.name}, item {i}: throws item with {item} worry points to monkey {target}."
                    # )
            for monkey in monkeys:
                print(monkey)
            print()

        inspections = list()
        for monkey in monkeys:
            inspections.append(monkey.inspections)
            print(f"Monkey {monkey.name}: {monkey.inspections} inspections")

        inspections.sort(reverse=True)
        print(f"Monkey Business is {inspections[0] * inspections[1]}")

    print("=== Part Two ===")
    safe_modulo = 1
    for monkey in monkeys:
        safe_modulo *= monkey.modulo
    print(f"safe modulo is {safe_modulo}")
    print()

    for round in range(1, 10001):
        for monkey in monkeys:
            monkey.start_round()
            for i in range(len(monkey.items_in_round)):
                item, target = monkey.process_item(i, f"item % {safe_modulo}")
                monkeys[target].items.append(item)
        if round == 1 or round == 20 or (round) % 1000 == 0:
            print(f"Round {round}")
            for monkey in monkeys:
                print(
                    f"Monkey {monkey.name}: {monkey.inspections} inspections"
                )
            print()

    print("Finally")
    inspections = list()
    for monkey in monkeys:
        inspections.append(monkey.inspections)
        print(f"Monkey {monkey.name}: {monkey.inspections} inspections")

    inspections.sort(reverse=True)
    print(f"Monkey Business is {inspections[0] * inspections[1]}")


if __name__ == "__main__":
    main()
