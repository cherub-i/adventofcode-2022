import time
import locale


class Timer:
    def __init__(self, mode="processor"):
        self.mode = mode
        self.time_init = self.take_time()
        self.time_start = self.take_time()
        self.time_previous_iteration = self.take_time()
        self.print_iteration_interval: int = 1
        self.max_no_iterations: int = -1
        locale.setlocale(
            locale.LC_ALL, ""
        )  # Use '' for auto, or force e.g. to 'en_US.UTF-8'

    def set_max_iteration(self, max_iteration: int):
        self.max_no_iterations: int = max_iteration

    def print_start(self):
        self.time_start = self.take_time()
        content = "Starting"
        if self.max_no_iterations != -1:
            content += f", target is {self.max_no_iterations} iterations"
        print(content)

    def print_iteration(self, iteration: int):
        iteration_no = iteration + 1
        if (
            iteration_no == 1
            or iteration_no % self.print_iteration_interval == 0
        ):
            time_current_iteration = self.take_time()
            time_since_start = time_current_iteration - self.time_start
            time_since_previous_iteration = (
                time_current_iteration - self.time_previous_iteration
            )
            done_percentage: float = 0
            content = ""

            if self.max_no_iterations != -1 and iteration_no != 0:
                iteration_max_as_string = f"{self.max_no_iterations:n}"
                iteration_as_string = f"{iteration_no:n}".rjust(
                    len(iteration_max_as_string)
                )
                done_percentage = iteration_no / self.max_no_iterations
                content += f"{iteration_as_string}/{iteration_max_as_string} ({done_percentage * 100:5.1f}%)"
            else:
                content = f"{iteration_no:4n}"
            content += f": {Timer.pretty_time(time_since_previous_iteration)} this iteration / {Timer.pretty_time(time_since_start)} since start"
            if self.max_no_iterations != -1 and iteration_no != 0:
                total_expected_time = (
                    time_since_start
                    / iteration_no
                    * (self.max_no_iterations - iteration_no)
                )
                content += f" / {Timer.pretty_time(total_expected_time)} expected total"
            print(content)
            self.time_previous_iteration = time_current_iteration

    def take_time(self):
        allowed_modes = ["processor", "wall"]
        if self.mode not in allowed_modes:
            raise ValueError(
                f"unknown mode: {self.mode}, expected: {allowed_modes}"
            )
        if self.mode == "processor":
            return time.process_time()
        else:
            return time.time()

    @staticmethod
    def pretty_time(the_time: float) -> str:
        content = ""
        if the_time < 60:
            # below minute: 59.9999s
            content = f"{the_time:7.4f}s"
        elif the_time < 60 * 60:
            # below hour:   59:59.2m
            content = f"{the_time//60:2.0f}:{the_time%60:04.1f}m"
        else:
            # above hour:   9:59:59h
            content = f"{the_time//60*60:.0f}:{the_time//60:02.0f}:{the_time%60:02.0f}h"
        return content


def main():
    timer: Timer = Timer()

    timer.print_start()
    x = 123 ^ 123456

    timer.print_start()
    x = 123 ^ 123456
    for i in range(3):
        x = 123 ^ (123456789 + i * 10)
        timer.print_iteration(i)


if __name__ == "__main__":
    main()
