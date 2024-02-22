"""
Testing the app
"""

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
                          random.randint(0, MAX_INT), random.randint(7, 18))
    return process
