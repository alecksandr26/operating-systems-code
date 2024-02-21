"""
Testing the app
"""

import sys

from src.view import View, AnimationView
from src.model import Model, Process
from src.controller import Controller, INFO
from src.configurations import *

import random
import string

def generate_random_string(length):
    """ generate random of strings """
    letters_and_digits = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters_and_digits) for _ in range(length))
    return random_string


def generate_random_process(num : int) -> Process:
    """ Will generate a random process"""
    process = Process(generate_random_string(10), num)
    process.set_operation(random.choice(OPERATIONS), random.randint(0, MAX_INT),
                          random.randint(0, MAX_INT), random.randint(1, 5))
    return process

# The amount of processes to exected
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
