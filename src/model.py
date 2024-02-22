"""
Stores and Manages the data of the App
"""
import math
from time import sleep
from src.configurations import *
from threading import Thread, Event

# Object to represent the process
class Process:
    """ The process class where to stored and instanciet everything"""
    def __init__(self, name : str, program_num : int):
        self.name = name
        self.num = program_num
        self.operation = ""
        self.operation_sym = ""
        self.first_operand = 0
        self.second_operand = 0
        self.time = 0
        self.actual_time = 0
        self.left_time = 0
        self.result = 0
        self.event_interrupt = None
        self.event_pause = None
        self.event_error = None
        self.run_thread = None

    def set_operation(self, operation_sym : str, first_operand : int,
                      second_operand : int, time : int):
        """ set an operation """
        self.operation_sym = operation_sym
        self.first_operand = first_operand
        self.second_operand = second_operand
        self.operation = f"{first_operand} {operation_sym} {second_operand}"
        self.time = time
        self.actual_time = 0
        self.left_time = time


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

    def create_thread(self):
        """Creates a new thread"""
        self.event_pause = Event()
        self.event_interrupt = Event()
        self.event_error = Event()
        self.run_thread = Thread(target = self.run)

    def run(self):
        """Execute the process"""
        # Here run the thread
        try:
            self.do_operation()
        except:
            INFO("Crashing.....")
            self.result = "ERROR"
            sleep(1)
            return

        sleep(1)
        while self.left_time > 0:
            while self.event_pause.is_set():
                INFO("Sleeping.....")
                sleep(1)
            if self.event_interrupt.is_set():
                INFO("Interrupting.....")
                sleep(1)
                break;
            
            if self.event_error.is_set():
                INFO("Crashing.....")
                self.result = "ERROR"
                sleep(1)
                break;
            
            self.actual_time += 1
            self.left_time -= 1
            sleep(1)

    def get_data(self) -> dict:
        """ get the data in a dict from the process """
        data = {
            "num" : self.num,
            "name" : self.name,
            "operation_sym" : self.operation_sym,
            "operation" : self.operation,
            "first_operand" : self.first_operand,
            "second_operand" : self.second_operand,
            "time" : self.time,
            "actual_time" : self.actual_time,
            "left_time" : self.left_time
        }

        if hasattr(self, "result"):
            data["result"] = self.result

        return data

    def __str__(self) -> str:
        return f"<Process({self.num}, {self.name}, {self.operation})>"

class Batch:
    """A queue structure to contain the batch processes to be executed"""
    def __init__(self, capacity : int):
        self._batch = []
        self._capacity = capacity
        self._iter = 0

    def add(self, process : Process):
        """Adds a new process to the queue"""
        assert len(self._batch) + 1 <= MAX_BATCH_CAPACITY, "Can't add more processes"
        self._batch.append(process)

    def pop(self) -> Process:
        """Pops the first pocess to been executed"""
        assert len(self._batch) > 0, "Empty batch"
        return self._batch.pop(0)

    def __len__(self) -> int:
        return len(self._batch)

    def empty(self) -> bool:
        """To know if the batch is currently empty"""
        return len(self._batch) == 0

    def fill(self) -> bool:
        """To know if the batch is currently filled"""
        return len(self._batch) == self._capacity

    def capacity(self) -> int:
        """To know the current capacity"""
        return self._capacity

    def run(self, model):
        """Run each process of the current batch until is empty"""
        while not self.empty():
            model.current_process = self.pop()
            model.current_process.create_thread()
            model.current_process.run_thread.start()
            
            # Wait for finish the thread
            model.current_process.run_thread.join()
            if not model.current_process.event_interrupt.is_set():
                model.finished_processes.add(model.current_process)
                
            model.current_process = None
            sleep(1)

    def __getitem__(self, index : int) -> Process:
        assert index >= 0, "Invalid index"
        assert index < len(self._batch), "Invalid index"
        return self._batch[index]

    def __iter__(self) -> iter:
        self._iter = 0
        return self

    def __next__(self) -> Process:
        if self._iter >= len(self._batch):
            raise StopIteration
        self._iter += 1
        return self._batch[self._iter - 1]


class ListProcesses:
    """A queue structure to contain all the processes"""
    def __init__(self, list_processes : [Process] = None):
        self._list = list_processes if list_processes is not None else []
        self._iter = 0

    def add(self, process : Process):
        """Adds a new process to the be executed"""
        assert len(self._list) + 1 <= MAX_NUMBER_OF_PROCESS, "Cna't add more processes"
        self._list.append(process)

    def pop(self) -> Process:
        """To remove the first element of the list"""
        return self._list.pop(0)

    def top(self) -> Process:
        """To know which is the top of the processes list"""
        assert not self.empty(), "Error empty list"
        return self._list[len(self._list) - 1]

    def fill_batch(self, batch : Batch):
        """To fill the current batch"""
        assert batch.empty(), "The batch must be empty"
        while not self.empty() and not batch.fill():
            batch.add(self.pop())

    def num_batches(self, batch) -> int:
        """The number of necessary batches to be executed to finished"""
        return math.ceil(len(self._list) / batch.capacity())

    def empty(self) -> bool:
        """To know if the batch is currently empty"""
        return len(self._list) == 0

    def __len__(self):
        return len(self._list)

    def __getitem__(self, index : int) -> Process:
        assert index >= 0, "Invalid index"
        assert index < len(self._list), "Invalid index"
        return self._list[index]

    def __iter__(self) -> iter:
        self._iter = 0
        return self

    def __next__(self) -> Process:
        if self._iter >= len(self._list):
            raise StopIteration
        self._iter += 1
        return self._list[self._iter - 1]

    def __str__(self) -> str:
        string = "<ListProcesses(["
        for pro in self._list[:3]:
            string += str(pro)
            if len(self._list) > 2:
                string += ", "
        return string + "])"

class Model:
    """Where to store the genral variables here"""
    def __init__(self):
        # Build the list to handled the process
        self.processes = ListProcesses()
        self.batch = Batch(MAX_BATCH_CAPACITY)
        self.finished_processes = ListProcesses()
        self.total_time = 0.0
        self.current_process = None
        self.batch_counter = 0
