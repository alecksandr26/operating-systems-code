import sys

from view import View, AnimationView
from model import Model, Process
from controller import Controller, INFO
from configurations import *

import random
import string


def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters_and_digits) for _ in range(length))
    return random_string


def generate_random_process() -> Process:
    process = Process(generate_random_string(10), generate_random_string(10))
    process.set_operation(random.choice(OPERATIONS), random.randint(0, MAX_INT),
                          random.randint(0, MAX_INT), random.randint(1, 5))
    return process

N = 10
def main():
    controller = Controller()

    for i in range(0, N):
        controller.model.add_process(generate_random_process())

    controller.show_view("AnimationView")
    controller.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
