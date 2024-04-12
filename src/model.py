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
        self.operation_res = ""
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
        self.operation_res = f"{self.first_operand} {self.operation_sym} {self.second_operand} = {self.result}"


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
            self.operation_res = "ERROR"
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
                self.operation_res = "ERROR"
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
            "left_time" : self.left_time,
            "operation_res" : self.operation_res
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
        self.arrive = -1
        self.finish = -1
        self.return_time = -1
        self.ans_time = -1
        self.wait_time = -1
        self.service_time = 0
        self.cooldown_status = False
        self.cooldown_thread = None
        self.state = ProcessState.NEW
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
        dic["arrive"] = self.arrive
        dic["finish"] = self.finish
        dic["return"] = self.return_time
        dic["answer"] = self.ans_time
        dic["wait"] = self.wait_time
        dic["service"] = self.service_time
        dic["state"] = self.state
        return dic

    def set_arrive(self, time):
        """To set teh arrive time of the process"""
        self.arrive = time

    def set_finish(self, time):
        """To set the ending time of the process"""
        self.finish = time
        self.set_return_time(self.finish - self.arrive)

    def set_return_time(self, time):
        """To set the amount of time that takes the process on the system"""
        self.return_time = time

    def set_ans_time(self, time):
        """To set the time that takes the system to attend the process"""
        self.ans_time = time
        
    def set_wait_time(self, time):
        """To set the waiting time until the process is attend"""
        self.wait_time = time

    def set_service_time(self, time):
        """Set the service time the time that takes in the processor """
        self.service_time += time

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
                model.fcfs_mem.add(model.fcfs_mem.pop(model.fcfs_mem.index(self)))

        self.set_state(ProcessState.READY)
        self.cooldown_status = False

    def set_cooldown(self):
        """Sets the process in a cooldown"""
        self.cooldown_time = COOLDOWN_TIME
        self.cooldown_status = True
        self.cooldown_thread = Thread(target = self.cooldown)
        self.cooldown_thread.start()

    def set_state(self, state):
        """To set the state to the process"""
        self.state = state

    def get_state(self):
        """To set an state to the process"""
        return self.state


class RRProcess(FCFSProcess):
    """The RR process algorithm with a quantum"""
    def __init__(self, name : str, program_num : int, quantum : int = MIN_QUANTUM_VAL):
        self.quantum = quantum
        self.elapsed_quantum = 0
        super().__init__(name, program_num)

    def get_quantum(self) -> int:
        """To get the value of the quantum"""
        return self.quantum
    
    def set_quantum(self, new_quantum):
        """To set a new value of quantum"""
        self.quantum = new_quantum

    def get_data(self) -> dict:
        """Gets the data from the process with the quantum"""
        dic = super().get_data()
        dic["quantum"] = self.quantum
        dic["elapsed_quantum"] = self.elapsed_quantum
        return dic

        # Overide the run function
    def run(self) -> int:
        """Execute the process"""
        # Here run the thread
        model = Model()
        try:
            self.do_operation()
        except:
            INFO("Crashing.....")
            self.result = "ERROR"
            self.operation_res = "ERROR"
            sleep(1)
            return CRASHED_PROCESS
        
        self.elapsed_quantum = 0
        sleep(1)
        while self.left_time > 0 and self.quantum > self.elapsed_quantum:
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
                self.operation_res = "ERROR"
                sleep(1)
                return CRASHED_PROCESS

            self.actual_time += 1
            self.elapsed_quantum += 1
            self.left_time -= 1
            sleep(1)

        return SUCCEEDED_PROCESS


class ListProcesses:
    """A queue structure to contain all the processes"""
    def __init__(self, list_processes : [Process] = None, capacity : int = MAX_NUMBER_OF_PROCESS):
        self._list = list_processes if list_processes is not None else []
        self._iter = 0
        self._capacity = capacity

    def add(self, process : Process):
        """Adds a new process to the be executed"""
        assert len(self._list) + 1 <= self._capacity, "Can't add more processes"
        self._list.append(process)

    def pop(self, i = 0) -> Process:
        """To remove the first element of the list"""
        return self._list.pop(i)

    def index(self, pro : Process):
        """Get the index of the process"""
        return self._list.index(pro)

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
    """A queue structure to contain and to simulates the execution of processes"""
    def __init__(self, capacity : int = MAX_FCFS_QUEUE_CAPACITY):
        super().__init__(capacity = capacity)

    def run(self):
        """Run each process until it is empty"""
        model = Model()
        while not self.empty():
            # Take the first element
            model.current_process = self[0]
            if not model.current_process.cooldown_is_set():
                model.current_process.set_state(ProcessState.EXECUTING)
                model.current_process.prepare_to_run()
                time_arrive_in_cpu = model.total_time
                if model.current_process.wait_time == -1:
                    model.current_process.set_wait_time(model.total_time)
                if model.current_process.ans_time == -1:
                    model.current_process.set_ans_time(model.total_time
                                                       - model.current_process.arrive)                

                model.current_process.thread.start()

                # Wait for finish the thread
                ret = model.current_process.thread.join()
                if (ret == SUCCEEDED_PROCESS and model.current_process.left_time == 0) \
                   or ret == CRASHED_PROCESS:
                    model.current_process.set_finish(model.total_time)
                    model.current_process.set_state(ProcessState.FINISHED)
                    model.finished_processes.add(model.current_process)               
                    # Remove the first element to be able to set another element
                    self.pop()
                elif ret == INTERRUPTED_PROCESS:
                    # Set the process in cooldown and push it back
                    model.current_process.set_state(ProcessState.BLOCKED)
                    model.current_process.set_cooldown()
                    self.add(self.pop())
                else:
                    # Put it back
                    self.add(self.pop())
                model.current_process.set_service_time(model.total_time - time_arrive_in_cpu)
            model.current_process = None
            # Wait to add a new element if thats possible
            sleep(1)
        

class Model:
    """Where to store the values and datastructures and things"""
    
    # Making it a singleton class
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
        self.new_processes = ListProcesses()
        self.finished_processes = ListProcesses()
        self.batch = Batch()
        self.fcfs_mem = FCFSMem()
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
        while not self.new_processes.empty() and not self.fcfs_mem.fill():
            INFO(self.new_processes.empty())
            pro = self.new_processes.pop()
            pro.set_state(ProcessState.READY)
            pro.set_arrive(self.total_time)
            self.fcfs_mem.add(pro)
