
# Stores and Manages the data of the App

import math
from configurations import *
from time import sleep

# Object to represent the process
class Process:
    def __init__(self, name : str, process_id : int):
        self.name = name
        self.id = process_id

    def set_operation(self, operation_sym : str, first_operand : int,
                      second_operand : int, execution_time : int):
        self.operation_sym = operation_sym
        self.first_operand = first_operand
        self.second_operand = second_operand
        self.execution_time = execution_time
        self.actual_time = 0
        self.left_time = execution_time

    def do_operation(self):
        # Do the math genius
        try:
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
        except:
            self.result = "error"
            
    def get_data(self) -> dict:
        data = {
            "id" : self.id,
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
        return len(self.processes)
    
    def add_process(self, process : Process):
        assert self.get_num_processes() < MAX_AMOUNT_OF_PROCESS, "Too much processes huuhhh dying... XP"
        self.processes.append(process)

    def get_num_batches(self) -> int:
        return math.ceil(self.get_num_processes() / BATCH_SIZE)

    def get_processes(self) -> [Process]:
        return self.processes

    def get_batch(self) -> [Process]:
        return self.batch

    def get_finshed_processes(self) -> [Process]:
        return self.finished_processes


