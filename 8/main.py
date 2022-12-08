import numpy

file = "8/test.txt"
file = "8/input.txt"


def main():
    with open(file, "r", encoding="utf-8") as input_file:
        forest = numpy.array(
            [list(line.replace("\n", "")) for line in input_file.readlines()],
            dtype=int,
        )

    print(f"the forest is:\n{forest}")
    print()

    width = forest.shape[0]
    height = forest.shape[1]

    total_visible_trees = height * 2 + width * 2 - 4
    highest_scenic_score = 0

    for row in range(1, height - 1):
        for col in range(1, width - 1):
            tree = forest[row, col]
            north = numpy.flipud(forest[:row, col : col + 1]).transpose()[0]
            west = numpy.fliplr(forest[row : row + 1, :col])[0]
            east = forest[row : row + 1, col + 1 :][0]
            south = forest[row + 1 :, col : col + 1].transpose()[0]

            visibility = "not visible"
            if (
                tree > numpy.amax(west)
                or tree > numpy.amax(east)
                or tree > numpy.amax(north)
                or tree > numpy.amax(south)
            ):
                visibility = "visible"
                total_visible_trees += 1

            scenic_score_north = get_scenic_score(tree, north)
            scenic_score_west = get_scenic_score(tree, west)
            scenic_score_east = get_scenic_score(tree, east)
            scenic_score_south = get_scenic_score(tree, south)
            scenic_score = (
                scenic_score_west
                * scenic_score_east
                * scenic_score_north
                * scenic_score_south
            )
            if scenic_score > highest_scenic_score:
                highest_scenic_score = scenic_score

            # print(
            #     f"tree at {row}, {col} is {visibility:11}, scenic score: {scenic_score} ({tree} W:{west} E:{east} N:{north} S:{south}"
            # )

    print("=== Part One ===")
    print(f"total of visible trees: {total_visible_trees}")

    print()
    print("=== Part Two ===")
    print(f"highest scenic score: {highest_scenic_score}")


def get_scenic_score(vantage_point, view):
    score = 0
    for tree in view:
        score += 1
        if tree >= vantage_point:
            break
    return score


if __name__ == "__main__":
    main()
