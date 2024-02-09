"""
Stores and Manages the data of the App
"""

import math
from configurations import *
from time import sleep

# Object to represent the process
class Process:
    """ Process model """
    def __init__(self, name : str, program_num : int):
        self.name = name
        self.num = program_num
        self.operation_sym = ""
        self.first_operand = 0
        self.second_operand = 0
        self.execution_time = 0
        self.actual_time = 0
        self.left_time = 0
        self.result = 0

    def set_operation(self, operation_sym : str, first_operand : int,
                      second_operand : int, execution_time : int):
        """ set an operation """
        self.operation_sym = operation_sym
        self.first_operand = first_operand
        self.second_operand = second_operand
        self.execution_time = execution_time
        self.actual_time = 0
        self.left_time = execution_time


    def do_operation(self):
        """ do the math genius """

        if self.operation_sym == "+":
            self.result = self.first_operand + self.second_operand
        elif self.operation_sym == "-":
            self.result = self.first_operand - self.second_operand
        elif self.operation_sym == "*":
            self.result = self.first_operand * self.second_operand
        elif self.operation_sym == "/":
            self.result = self.first_operand / self.second_operand
        elif self.operation_sym == "%":
            self.result = self.first_operand % self.second_operand
        elif self.operation_sym == "^":
            self.result = self.first_operand ** self.second_operand
        else:
            assert 0, "Invalid operation genius chrashing.... XP"

    def get_data(self) -> dict:
        """ get the data in a dict from the process """
        data = {
            "num" : self.num,
            "name" : self.name,
            "operation_sym" : self.operation_sym,
            "first_operand" : self.first_operand,
            "second_operand" : self.second_operand,
            "execution_time" : self.execution_time,
            "actual_time" : self.actual_time,
            "left_time" : self.left_time
        }

        if hasattr(self, "result"):
            data["result"] = self.result

        return data



class Model:
    def __init__(self):
        # Build the list to handled the process
        self.processes = []
        self.batch = []
        self.finished_processes = []
        self.total_time = 0

    def get_num_processes(self) -> int:
        """ get num processes loaded """
        return len(self.processes)

    def add_process(self, process : Process):
        """ add a new process to model """
        assert self.get_num_processes() < MAX_AMOUNT_OF_PROCESS, \
            "Too much processes huuhhh dying... XP"
        self.processes.append(process)

    def get_num_batches(self) -> int:
        """ get number of batches it will round to inf """
        return math.ceil(self.get_num_processes() / BATCH_SIZE)

    def get_processes(self) -> [Process]:
        """ get the list of proceses """
        return self.processes

    def get_batch(self) -> [Process]:
        """ get batch current batch """
        return self.batch

    def get_finshed_processes(self) -> [Process]:
        """ get the finished processes """
        return self.finished_processes
