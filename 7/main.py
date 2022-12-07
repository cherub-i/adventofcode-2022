file = "7/test.txt"
file = "7/input.txt"


class Directory:
    def __init__(self, name, parent):
        self.name = name
        self._parentdirectory = parent
        self.files = dict()
        self.subdirectories = dict()
        self._filessize = 0
        self.totalsize = 0

    def parent(self):
        return self._parentdirectory

    def has_directory(self, name):
        return name in self.subdirectories

    def add_subdirectory(self, name):
        new_subdirectory = Directory(name, self)
        self.subdirectories[name] = new_subdirectory
        return new_subdirectory

    def get_subdirectory(self, name):
        return self.subdirectories[name]

    def print_directory(self):
        Directory.calculate_totalsize_recursive(self)
        Directory.print_directory_recursive(self, 0)

    def add_file(self, name, size):
        self.files[name] = size
        self._filessize += size

    def visit_subdirectories(self, func):
        Directory.visit_subdirectories_recursive(self, func)

    @classmethod
    def visit_subdirectories_recursive(cls, directory, func):
        for name, subdirectory in directory.subdirectories.items():
            Directory.visit_subdirectories_recursive(subdirectory, func)

        func(directory)

    @classmethod
    def print_directory_recursive(cls, directory, level):
        directory_prefix = "-" * (level + 1) + " "
        file_prefix = " " * (level + 1) + " -"
        print(
            f"{directory_prefix}{directory.name} size of files: {directory._filessize}, total size: {directory.totalsize}"
        )
        for name, size in directory.files.items():
            print(f"{file_prefix}{name} ({size})")
        for name, subdirectory in directory.subdirectories.items():
            Directory.print_directory_recursive(subdirectory, level + 1)

    @classmethod
    def calculate_totalsize_recursive(cls, directory):
        for name, subdirectory in directory.subdirectories.items():
            Directory.calculate_totalsize_recursive(subdirectory)

        subdir_size = 0
        for name, subdirectory in directory.subdirectories.items():
            subdir_size += subdirectory.totalsize
        directory.totalsize = directory._filessize + subdir_size


def main():
    root = Directory("/", None)
    current_directory = root

    with open(file, "r", encoding="utf-8") as input_file:
        line = input_file.readline().replace("\n", "")

        while line != "":
            if line.startswith("$"):
                ls_mode = False
                command = line.split(" ")[1]
                if command == "cd":
                    cd_argument = line.split(" ")[2]
                    if cd_argument == "/":
                        current_directory = root
                    elif cd_argument == "..":
                        current_directory = current_directory.parent()
                    else:
                        if current_directory.has_directory(cd_argument):
                            current_directory = (
                                current_directory.get_subdirectory(cd_argument)
                            )

                        else:
                            current_directory = (
                                current_directory.add_subdirectory(cd_argument)
                            )

                elif command == "ls":
                    ls_mode = True
            else:
                if ls_mode and not line.startswith("dir"):
                    size = int(line.split(" ")[0])
                    filename = "".join(line.split(" ")[1:])
                    current_directory.add_file(filename, size)

            line = input_file.readline().replace("\n", "")

    print("=== Part One ===")
    root.print_directory()

    found_directories = list()
    root.visit_subdirectories(
        lambda dir: collect_directories_part1(dir, found_directories)
    )

    print("small directories")
    all_small_size = 0
    for directory in found_directories:
        print(f"{directory.name}: {directory.totalsize}")
        all_small_size += directory.totalsize
    print(f"total: {all_small_size}")

    print("=== Part Two ===")
    disk_size = 70000000
    required_size = 30000000
    free_space = disk_size - root.totalsize
    missing_free_space = required_size - free_space
    print(f"missing free space {missing_free_space}")

    best_directory = list()
    root.visit_subdirectories(
        lambda dir: find_directory_part2(
            dir, missing_free_space, best_directory
        )
    )
    print(
        f"best fit is {best_directory[0].name} with size {best_directory[0].totalsize}"
    )


def collect_directories_part1(directory, small_directories):
    if directory.totalsize <= 100000:
        small_directories.append(directory)


def find_directory_part2(directory, missing_free_space, best_yet):
    if directory.totalsize >= missing_free_space:
        if len(best_yet) == 0:
            best_yet.append(directory)
        elif best_yet[0].totalsize > directory.totalsize:
            best_yet.pop()
            best_yet.append(directory)


if __name__ == "__main__":
    main()
