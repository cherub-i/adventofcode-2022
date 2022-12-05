import re

# file = "5/test.txt"
file = "5/input.txt"


def main():
    print("=== Part One ===")
    with open(file, "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")

        # read initial stack
        current_stacks = []
        while line != "":
            current_stacks.append(line)

            line = input_file.readline().replace("\n", "")
        stacks_dict = dict()
        stacks_numbers = current_stacks.pop()
        stacks_count = 0
        for stack_number in re.split(" +", stacks_numbers.strip()):
            stacks_dict[int(stack_number)] = list()
            stacks_count += 1

        print(f"working with {stacks_count} stacks")

        while current_stacks:
            stacks_content = current_stacks.pop()
            for i in range(1, len(stacks_dict) + 1):
                string_pos = 1 + (4 * (i - 1))
                content = stacks_content[string_pos : string_pos + 1]
                if content.strip():
                    stacks_dict[i].append(content)

        for name, content in stacks_dict.items():
            print(f"stack {name} contains {content}")

        # read moves
        line = input_file.readline().replace("\n", "")
        while line != "":
            num_contents = int(line.split(" ")[1])
            content_from = int(line.split(" ")[3])
            content_to = int(line.split(" ")[5])

            print(f"moving {num_contents} from {content_from} to {content_to}")

            for i in range(0, num_contents):
                stacks_dict[content_to].append(stacks_dict[content_from].pop())

            line = input_file.readline().replace("\n", "")

    print("finally:")
    solution = ""
    for name, content in stacks_dict.items():
        print(f"stack {name} contains {content}")
        solution += content[-1]
    print()
    print(f"topmost crates are: {solution}")

    print("=== Part Two ===")
    with open(file, "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")

        # read initial stack
        current_stacks = []
        while line != "":
            current_stacks.append(line)

            line = input_file.readline().replace("\n", "")
        stacks_dict = dict()
        stacks_numbers = current_stacks.pop()
        stacks_count = 0
        for stack_number in re.split(" +", stacks_numbers.strip()):
            stacks_dict[int(stack_number)] = list()
            stacks_count += 1

        print(f"working with {stacks_count} stacks")

        while current_stacks:
            stacks_content = current_stacks.pop()
            for i in range(1, len(stacks_dict) + 1):
                string_pos = 1 + (4 * (i - 1))
                content = stacks_content[string_pos : string_pos + 1]
                if content.strip():
                    stacks_dict[i].append(content)

        for name, content in stacks_dict.items():
            print(f"stack {name} contains {content}")

        # read moves
        line = input_file.readline().replace("\n", "")
        while line != "":
            num_contents = int(line.split(" ")[1])
            content_from = int(line.split(" ")[3])
            content_to = int(line.split(" ")[5])

            print(f"moving {num_contents} from {content_from} to {content_to}")

            tmp_stack = list()
            for i in range(0, num_contents):
                tmp_stack.append(stacks_dict[content_from].pop())
            for i in range(0, num_contents):
                stacks_dict[content_to].append(tmp_stack.pop())

            line = input_file.readline().replace("\n", "")

    print("finally:")
    solution = ""
    for name, content in stacks_dict.items():
        print(f"stack {name} contains {content}")
        solution += content[-1]
    print()
    print(f"topmost crates are: {solution}")


if __name__ == "__main__":
    main()
