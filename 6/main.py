# file = "6/test.txt"
file = "6/input.txt"


def main():
    with open(file, "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")

        # print("=== Part One ===")
        # marker_length = 4
        print("=== Part Two ===")
        marker_length = 14

        while line != "":
            for i in range(0, len(line)):
                chars = list()
                if i >= marker_length - 1:
                    for j in range(0, marker_length):
                        chars.append(line[i - j : i - j + 1])
                    if len(set(chars)) == len(chars):
                        print(
                            f"signal found at position {i+1}: {line[i + 1 - marker_length :i + 1]}"
                        )
                        break
            line = input_file.readline().replace("\n", "")


if __name__ == "__main__":
    main()
