# The amount of processes to exected
import sys
from .random_processes import generate_random_string, generate_random_process
from src.controller import Controller

N = 10
def main():
    """ The main function """
    controller = Controller()

    for i in range(1, N + 1):
        controller.model.processes.add(generate_random_process(i))

    controller.show_view("AnimationView")
    controller.mainloop()
    return 0

if __name__ == "__main__":
    sys.exit(main())
