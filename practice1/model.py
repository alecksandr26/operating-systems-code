
# Stores and Manages the data of the App

from configurations import *
from time import sleep

# Object to represent the process
class Process:
    def __init__(self, name : str, process_id : int):
        self.name = name
        self.id = process_id
        self.time = time

    def set_operation(operaton_sym : str, first_operand : int, second_operand : int, execution_time : int):
        self.operation_sym = operation_sym
        self.first_operand = first_operand
        self.second_operand = second_operand
        self.execution_time = execution_time

    def run_process(self):
        # Simulating the execution of the process
        sleep(self.execution_time)

        # Do the math genius

        if self.operation_sym == "+":
            self.result = self.first_operand + self.second_operand
        elif self.operation_sym == "-":
            self.result = self.first_operand - self.second_operand
        elif self.operation_sym == "*":
            self.result = self.first_operand * self.second_operand 
        elif self.operation_sym == "/":
            self.result = self.first_operand / self.second_operand

        else:
            assert 0, "Invalid operation genius chrashing.... XP"

            
        
class Model:
    def __init__(self):
        
        # Build the list to handled the process
        self.processes = []

    def get_num_processes(self):
        return len(self.processes)
        
    def add_process(self, process : Process):
        assert self.get_num_processes() < MAX_AMOUNT_OF_PROCESS, "Too much processes huuhhh dying... XP"
        
        self.processes.append(process)

    
