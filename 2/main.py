from dataclasses import dataclass
from functools import total_ordering

file = "2/input.txt"
# file = "2/test.txt"


@dataclass
class OutcomeElement:
    name: str
    value: int
    desired_result_key: str


@dataclass
class Outcomes:
    win = OutcomeElement("win", 6, "Z")
    draw = OutcomeElement("draw", 3, "Y")
    loose = OutcomeElement("loose", 0, "X")
    possibilities = [win, draw, loose]

    @classmethod
    def get_by_desired_result_key(cls, desired_result_key):
        return next(
            (
                x
                for x in cls.possibilities
                if x.desired_result_key == desired_result_key
            ),
            None,
        )


@dataclass
@total_ordering
class RpsElement:
    name: str
    value: int
    key_as_challenge: str
    key_as_response: str

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return (
            (self.name == "Rock" and other.name == "Scissors")
            or (self.name == "Scissors" and other.name == "Paper")
            or (self.name == "Paper" and other.name == "Rock")
        )


class Rps:
    r = RpsElement("Rock", 1, "A", "X")
    p = RpsElement("Paper", 2, "B", "Y")
    s = RpsElement("Scissors", 3, "C", "Z")
    options = [r, p, s]

    @classmethod
    def get_by_challenge(cls, challenge):
        return next(
            (x for x in cls.options if x.key_as_challenge == challenge), None
        )

    @classmethod
    def get_by_response(cls, response):
        return next(
            (x for x in cls.options if x.key_as_response == response), None
        )

    @classmethod
    def find_response(cls, desired_outcome, challenge):
        if desired_outcome.name == "win":
            if challenge.name == "Rock":
                return cls.p
            elif challenge.name == "Paper":
                return cls.s
            elif challenge.name == "Scissors":
                return cls.r
            else:
                raise ValueError("unknown element name: ", challenge.name)
        elif desired_outcome.name == "loose":
            if challenge.name == "Rock":
                return cls.s
            elif challenge.name == "Paper":
                return cls.r
            elif challenge.name == "Scissors":
                return cls.p
            else:
                raise ValueError("unknown element name: ", challenge.name)

        elif desired_outcome.name == "draw":
            return challenge
        else:
            raise ValueError("unknown outcome name: ", desired_outcome.name)


def main():
    with open(file, "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")
        point_sum = 0

        while line != "":
            challenge = Rps.get_by_challenge(line.split(" ")[0])
            response = Rps.get_by_response(line.split(" ")[1])
            if response == challenge:
                result = Outcomes.draw
            elif response > challenge:
                result = Outcomes.win
            else:
                result = Outcomes.loose

            points = response.value + result.value
            point_sum += points

            print(
                f"opponent plays {challenge.name}, you answer {response.name} and {result.name}, yielding {points} points"
            )

            line = input_file.readline().replace("\n", "")
    print(f"total: {point_sum}")

    print()
    print("=== Part Two ===")
    with open(file, "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")
        point_sum = 0

        while line != "":
            challenge = Rps.get_by_challenge(line.split(" ")[0])
            desired_outcome = Outcomes.get_by_desired_result_key(
                line.split(" ")[1]
            )
            response = Rps.find_response(desired_outcome, challenge)

            points = desired_outcome.value + response.value
            point_sum += points

            print(
                f"opponent plays {challenge.name}, you want to {desired_outcome.name} and therefore answer {response.name}, yielding {points} points"
            )

            line = input_file.readline().replace("\n", "")
    print(f"total: {point_sum}")


if __name__ == "__main__":
    main()
