"""
Stores and Manages the data of the App
"""
import math
from time import sleep
from src.configurations import *
from threading import Thread, Event


class ThreadWithReturnValue(Thread):    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


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
        self.thread = None

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

    def prepare_to_run(self):
        """creates a new thread, and preperes to execute"""
        self.thread = ThreadWithReturnValue(target = self.run)

    def run(self) -> int:
        """Execute the process"""
        # Here run the thread
        model = Model()
        try:
            self.do_operation()
        except:
            INFO("Crashing.....")
            self.result = "ERROR"
            sleep(1)
            return CRASHED_PROCESS

        sleep(1)
        while self.left_time > 0:
            while model.event_pause.is_set():
                INFO("Sleeping.....")
                sleep(1)

            if model.event_interrupt.is_set():
                INFO("Interrupting.....")
                sleep(1)
                return INTERRUPTED_PROCESS

            if model.event_error.is_set():
                INFO("Crashing.....")
                self.result = "ERROR"
                sleep(1)
                return CRASHED_PROCESS

            self.actual_time += 1
            self.left_time -= 1
            sleep(1)

        return SUCCEEDED_PROCESS

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

class FCFSProcess(Process):
    """An FCFS process super important"""
    def __init__(self, name : str, program_num : int):
        self.cooldown_time = 0
        self.cooldown_status = False
        self.cooldown_thread = None
        super().__init__(name, program_num)

    def set_process(self, process : Process):
        """Copies a process variables"""
        self.name = process.name
        self.num = process.num
        self.operation = process.operation
        self.operation_sym = process.operation_sym
        self.first_operand = process.first_operand
        self.second_operand = process.second_operand
        self.time = process.time
        self.actual_time = process.actual_time
        self.left_time = process.left_time
        self.result = process.result
        self.thread = process.thread

    def get_data(self) -> dict:
        """Get the data from the process"""
        dic = super().get_data()
        dic["cooldown_time"] = self.cooldown_time
        dic["cooldown_status"] = self.cooldown_status
        return dic

    def cooldown_is_set(self):
        """Retrns the satte of the cooldown"""
        return self.cooldown_status

    def cooldown(self):
        """Waits until the cooldown is zero"""
        model = Model()
        while self.cooldown_time >= 0:
            sleep(1)
            
            if not model.event_pause.is_set():
                self.cooldown_time -= 1

        self.cooldown_status = False

    def set_cooldown(self):
        """Sets the process in a cooldown"""
        self.cooldown_time = COOLDOWN_TIME
        self.cooldown_status = True
        self.cooldown_thread = Thread(target = self.cooldown)
        self.cooldown_thread.start()


class ListProcesses:
    """A queue structure to contain all the processes"""
    def __init__(self, list_processes : [Process] = None, capacity : int = MAX_NUMBER_OF_PROCESS):
        self._list = list_processes if list_processes is not None else []
        self._iter = 0
        self._capacity = capacity

    def add(self, process : Process):
        """Adds a new process to the be executed"""
        assert len(self._list) + 1 <= self._capacity, "Cna't add more processes"
        self._list.append(process)

    def pop(self) -> Process:
        """To remove the first element of the list"""
        return self._list.pop(0)

    def top(self) -> Process:
        """To know which is the top of the processes list"""
        assert not self.empty(), "Error empty list"
        return self._list[len(self._list) - 1]

    def fill(self) -> bool:
        """To know if the list if filled"""
        return len(self._list) == self._capacity

    def num_batches(self, batch) -> int:
        """The number of necessary batches to be executed to finished"""
        return math.ceil(len(self._list) / batch.capacity())

    def empty(self) -> bool:
        """To know if the batch is currently empty"""
        return len(self._list) == 0

    def capacity(self) -> int:
        """Returns the capacity of the list"""
        return self._capacity

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
                string += ", ..."
        return string + "])"

class Batch(ListProcesses):
    """A queue structure to contain the batch processes to be executed"""
    def __init__(self, capacity : int = MAX_BATCH_CAPACITY):
        super().__init__(capacity = capacity)

    def run(self):
        """Run each process of the current batch until is empty"""
        model = Model()
        while not self.empty():
            model.current_process = self.pop()
            model.current_process.prepare_to_run()
            model.current_process.thread.start()

            # Wait for finish the thread
            ret = model.current_process.thread.join()
            if not ret == INTERRUPTED_PROCESS:
                model.finished_processes.add(model.current_process)

            model.current_process = None
            sleep(1)

class FCFSMem(ListProcesses):
    """A que structure to contain and to simulates the execution of processes"""
    def __init__(self, capacity : int = MAX_FCFS_QUEUE_CAPACITY):
        super().__init__(capacity = capacity)

    def run(self):
        """Run each process until it is empty"""
        model = Model()
        while not self.empty():
            # Take the first element
            model.current_process = self[0]
            if not model.current_process.cooldown_is_set():
                model.current_process.prepare_to_run()
                model.current_process.thread.start()

                # Wait for finish the thread
                ret = model.current_process.thread.join()
                if not ret == INTERRUPTED_PROCESS:
                    model.finished_processes.add(model.current_process)

                    # Remove the first element to be able to set another element
                    self.pop()
                else:
                    # Set the process in cooldown and push it back
                    model.current_process.set_cooldown()
                    self.add(self.pop())

            model.current_process = None
            # Wait to add a new element if thats possible
            sleep(1)

class Model:
    """Where to store the values and datastructures and things"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        # Build the list to handle the process
        self.processes = ListProcesses()
        self.batch = Batch()
        self.fcfs_mem = FCFSMem()
        self.finished_processes = ListProcesses()
        self.total_time = 0.0
        self.current_process = None
        self.batch_counter = 0
        self.event_pause = Event()
        self.event_interrupt = Event()
        self.event_error = Event()
        self.initialized = True

    def fill_batch(self):
        """To fill the current batch"""
        assert self.batch.empty(), "The batch must be empty"
        while not self.processes.empty() and not self.batch.fill():
            self.batch.add(self.processes.pop())

    def load_fcfs_mem(self):
        """Load the fcfs """
        while not self.processes.empty() and not self.fcfs_mem.fill():
            self.fcfs_mem.add(self.processes.pop())
