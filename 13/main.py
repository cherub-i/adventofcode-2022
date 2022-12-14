class Packet:
    def __init__(self, packet: str):
        self.as_string: str = packet
        self.data: list = eval(packet)
        self.iter_current: int = 0

    @property
    def sort_order(self) -> float:
        float_as_string = (
            self.as_string.replace("[", "").replace("]", "").replace(" ", "")
        )

        float_as_string = (
            float_as_string.split(",")[0]
            + "."
            + "".join(float_as_string.split(",")[1:])
        )

        if float_as_string == ".":
            float_as_string = "0"
        return float(float_as_string)

    def __lt__(self, other):
        return self.sort_order < other.sort_order

    # def process_data(self):
    #     result = ""
    #     for elem in self.data:
    #         result += self.process_data_part(elem)
    #     return result

    # def process_data_part(self, data_part) -> str:
    #     result: str = ""
    #     if type(data_part) == int:
    #         return str(data_part)
    #     else:
    #         for elem in data_part:
    #             result += self.process_data_part(elem)
    #     return result

    def __iter__(self):
        return self

    def __next__(self):
        if self.iter_current >= len(self):
            raise StopIteration
        self.iter_current += 1
        return self.data[self.iter_current - 1]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, pos):
        return self.data[pos]

    def __str__(self):
        return f"{self.data}"


class PacketPair:
    def __init__(self, left: Packet, right: Packet):
        self.left = left
        self.right = right
        self.iter_current: int = 0

    def start_check(self):
        return self.check_list(self.left, self.right)

    def check_list(self, left, right):
        for i in range(len(left)):
            if i >= len(right):
                return False
            else:
                result = self.check(left[i], right[i])
                if result is not None:
                    return result
        if len(right) > len(left):
            return True

    def check(self, left, right):
        # print(f"'{left}' vs. '{right}'")
        if type(left) == int and type(right) == int:
            if left < right:
                return True
            elif left > right:
                return False
        elif type(left) == list and type(right) == list:
            return self.check_list(left, right)
        elif type(left) == list or type(right) == list:
            if type(left) == int:
                left = list([left])
            if type(right) == int:
                right = list([right])
            return self.check_list(left, right)

    def __str__(self):
        return f"{self.left}\n{self.right}"


def main():
    day = 13
    the_file = "test.txt"
    the_file = "input.txt"

    packet_pair_list: list = list()
    with open(f"{day}/{the_file}", "r", encoding="utf-8") as input_file:
        file_content = [
            line.replace("\n", "") for line in input_file.readlines()
        ]
        for i in range(0, len(file_content), 3):
            packet_pair_list.append(
                PacketPair(
                    Packet(file_content[i]), Packet(file_content[i + 1])
                )
            )

    print("=== Part One ===")
    check_sum = 0
    for i, packet_pair in enumerate(packet_pair_list):
        print(f"{packet_pair}")
        is_correct = packet_pair.start_check()
        if is_correct:
            check_sum += i + 1
        print(f"correct: {is_correct}")
        print()

    print(f"check sum for correct packet-pairs: {check_sum}")

    print()
    print("=== Part Two ===")
    divider_1 = "[[2]]"
    divider_2 = "[[6]]"
    packet_list = [packet_pair.left for packet_pair in packet_pair_list]
    packet_list += [packet_pair.right for packet_pair in packet_pair_list]
    packet_list.append(Packet(divider_1))
    packet_list.append(Packet(divider_2))
    packet_list.sort()

    found_1 = 0
    found_2 = 0
    for i, packet in enumerate(packet_list):
        print(f"{i+1:4}: {packet.as_string}")
        if packet.as_string == divider_1:
            found_1 = i + 1
        if packet.as_string == divider_2:
            found_2 = i + 1
    print(f"dividers at {found_1} and {found_2}: {found_1 * found_2}")


if __name__ == "__main__":
    main()
