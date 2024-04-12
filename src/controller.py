"""
The controller which controls the Model and the View part of the app
"""

from time import sleep
from abc import abstractmethod

from .model import Model, Process, Batch, ListProcesses, FCFSMem, FCFSProcess, RRProcess
from .view import VIEWS_CLASSES
from .utils import generate_random_process

from threading import Thread
from tkinter import *
from tkinter import messagebox
from src.configurations import *

class Controller(Tk):
    """A simple abstract class where to use as base to create new backends"""
    def __init__(self, controller_name : str, default_view = "MainView"):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)
        self.controller_name = controller_name
        
        INFO(default_view)

        # Create the model and view
        self.model = Model()
        self.view = None
        self.views = {}
        self.show_view(default_view)

        # Where to stored the thread
        self.thread = None
        self.thread_timer = None
        
        # Keyboard events
        self.bind("E", self._interruption_io_handler)
        self.bind("P", self._pause_handler)
        self.bind("C", self._resume_handler)
        self.bind("W", self._error_hanlder)
        self.bind("B", self._show_processes_table)
        self.bind("N", self._add_new_rand_process);
        
    @abstractmethod
    def _error_hanlder(self, event):
        """The hanlder of simulating an error"""
    @abstractmethod
    def _interruption_io_handler(self, event):
        """A handler of the interruption"""
    @abstractmethod
    def _pause_handler(self, event):
        """A handler of the pause"""
    @abstractmethod
    def _resume_handler(self, event):
        """A handler of the interruption"""

    @abstractmethod
    def _show_processes_table(self, event):
        """A handler of the shoing process of procesor"""

    @abstractmethod
    def _add_new_rand_process(self, event):
        """Adds a new random process to the list of processes"""

    @abstractmethod
    def run(self):
        """To run the selected simulation"""

    def show_view(self, view_name : str):
        """ Show the actual view """
        for VIEW in VIEWS_CLASSES:
            if VIEW.__name__ == view_name and view_name not in self.views.keys():
                self.view = VIEW(parent = self)
                self.views[view_name] = self.view
                self.view.grid(row = 0, column = 0, sticky = "nsew")
                break

        assert view_name in self.views.keys(), "The selected view doesn't exist"

        self.view = self.views[view_name]
        self.view.update_widgets()
        self.view.tkraise()

    def get_num_processes(self) -> int:
        """ get the number of processes to be executed  """
        return len(self.model.processes)

    def get_processes(self) -> ListProcesses:
        """ get the list of processes """
        return self.model.processes

    def get_cur_process(self) -> Process or None:
        """ get current processes been executed """
        return self.model.current_process

    def get_batch(self) -> Batch:
        """ get the actual batch """
        return self.model.batch

    def get_finshed_processes(self) -> ListProcesses:
        """ get the finished processes """
        return self.model.finished_processes

    def get_total_time(self) -> int:
        """ get the total time of the processed """
        return self.model.total_time
    
    def get_controller_name(self) -> str:
        """Retruns the controller name"""
        return self.controller_name

    def save_process(self, process_data : dict):
        """ Saving the process from data  """
        process = Process(process_data["name"], process_data["num"])
        process.set_operation(process_data["operation_sym"],
                              process_data["first_operand"],
                              process_data["second_operand"],
                              process_data["execution_time"])
        self.model.processes.add(process)

    def run_the_clock(self):
        """Run the timer"""
        while True:
            self.view.update_widgets()

            # Wait until the thread is dead
            if not self.thread.is_alive():
                break
            
            if not self.model.event_pause.is_set():
                self.model.total_time += 1
                
            sleep(1)

    def run_onclick(self):
        """ Executes all  the processes batch by batch  """
        self.thread = Thread(target = self.run)
        self.thread.start()
        
        self.thread_timer = Thread(target = self.run_the_clock)
        self.thread_timer.start()

        

class ControllerBatches(Controller):
    """ The Controller where the initial backend will be managed"""
    def __init__(self, default_view = "MainView"):
        super().__init__("Batch", default_view)

    def _error_hanlder(self, event):
        """The hanlder of simulating an error"""
        if self.model.current_process is not None:
            self.model.event_error.set()
            sleep(1)
            self.model.event_error.clear()

    def _interruption_io_handler(self, event):
        """A handler of the interruption"""
        if self.model.current_process is not None:
            self.model.event_interrupt.set()
            sleep(1)
            self.model.batch.add(self.model.current_process)
            self.model.event_interrupt.clear()

    def _pause_handler(self, event):
        """A handler of the interruption"""
        if self.model.current_process is not None:
            self.model.event_pause.set()

    def _resume_handler(self, event):
        """A handler of the interruption"""
        if self.model.current_process is not None and self.model.event_pause.is_set():
            self.model.event_pause.clear()

    def capture_process(self):
        """capture a new process to the list of processes."""
        process_data = {}
        try:
            process_data["name"] = self.view.entry_name.get()
            process_data["num"] = int(self.view.spin_proces_num.get())
            for pro in self.get_processes():
                if pro.num == process_data["num"]:
                    raise ValueError("Number is not unique")
            process_data["operation_sym"] = self.view.combo_operation_sym.get()
            process_data["first_operand"] = int(self.view.spin_first_operand.get())
            process_data["second_operand"] = int(self.view.spin_second_operand.get())
            process_data["execution_time"] = int(self.view.spin_execution_time.get())

            if process_data["operation_sym"] == "/" and process_data["second_operand"] == 0:
                raise ZeroDivisionError("Can't divide by zero")
        except ValueError as error:
            messagebox.showerror("showerror", f"Invalid introduced Process: {error}")
            return

        except ZeroDivisionError as error:
            messagebox.showerror("showerror", f"Division by zero: {error}")
            return

        self.save_process(process_data)
        self.view.update_widgets()

    def get_num_batches(self) -> int:
        """ get the number of batches """
        return self.model.processes.num_batches(self.model.batch)

    def prepare_to_run(self):
        """ checks the last things before running the simulation """
        try:
            amount_processes = int(self.view.spin_amount_processes.get())
        except ValueError as error:
            messagebox.showerror("showerror", f"Invalid number of introduced processes: {error}")
            return

        if self.get_num_processes() != amount_processes:
            messagebox.showerror("showerror", "Invalid number of introduced processes")
            return

        # Move to the next view
        self.show_view("AnimationView")

    def run(self):
        """Run all batches"""
        self.model.batch_counter = 1
        while not self.model.processes.empty():
            # Load the batch
            self.view.finished_processes_table.\
                add_message(f"{self.controller.get_controller_name()}: {self.model.batch_counter}")
            self.model.batch_counter += 1
            self.model.fill_batch()
            sleep(1.5)
            self.model.batch.run()


class ControllerRandom(ControllerBatches):
    """The Controller that will generate random processes"""
    def __init__(self):
        super().__init__("RandomNumView")
        
    def gen_random_processes(self):
        """It will genreate random processes"""
        try:
            amount_processes = int(self.view.spin_amount_processes.get())
        except ValueError as error:
            messagebox.showerror("showerror", f"Invalid number of introduced processes: {error}")
            return

        if amount_processes <= 0:
            messagebox.showerror("showerror",
                                 "Invalid number of introduced processes: can't be lesser or equal to zero")
            return

        for i in range(1, amount_processes + 1):
            self.model.processes.add(generate_random_process(i))
        INFO(self.model.processes)
        # Move to the next view
        self.show_view("AnimationView")

class ControllerFCFS(Controller):
    """This is the controller builds the simulation"""
    def __init__(self, controller_name : str = "FCFS", default_init_view_name : str = "RandomNumView"):
        super().__init__(controller_name, default_init_view_name)
        self.amount_processes = -1

    def _error_hanlder(self, event):
        """The hanlder of simulating an error"""
        if self.model.current_process is not None:
            self.model.event_error.set()
            sleep(1)
            self.model.event_error.clear()

    def _interruption_io_handler(self, event):
        """A handler of the interruption"""
        if self.model.current_process is not None:
            self.model.event_interrupt.set()
            sleep(1)
            self.model.event_interrupt.clear()

    def _pause_handler(self, event):
        """A handler of the interruption"""
        if self.model.current_process is not None:
            self.model.event_pause.set()

    def _resume_handler(self, event):
        """A handler of the interruption"""
        if self.model.current_process is not None and self.model.event_pause.is_set():
            self.model.event_pause.clear()

    def _show_processes_table(self, event):
        """A handler of the shoing process of procesor"""
        self.move_to_bcp_table()

    def _add_new_rand_process(self, event):
        """Adds a new random process to the list of processes"""
        self.amount_processes += 1
        process = generate_random_process(self.amount_processes)
        fcfs_process = FCFSProcess(process.name, process.num)
        fcfs_process.set_process(process)
        self.model.processes.add(fcfs_process)
        self.model.new_processes.add(fcfs_process)
        self.view.update_widgets()
        INFO("Added a new random process")

    def gen_random_processes(self):
        """It will genreate random processes"""
        try:
            self.amount_processes = int(self.view.spin_amount_processes.get())
        except ValueError as error:
            messagebox.showerror("showerror", f"Invalid number of introduced processes: {error}")
            return

        if self.amount_processes <= 0:
            messagebox.showerror("showerror",
                                 "Invalid number of introduced processes: can't be lesser or equal to zero")
            return

        for i in range(1, self.amount_processes + 1):
            process = generate_random_process(i)
            fcfs_process = FCFSProcess(process.name, process.num)
            fcfs_process.set_process(process)
            self.model.processes.add(fcfs_process)
            self.model.new_processes.add(fcfs_process)

        INFO(self.model.processes)
        INFO(self.model.new_processes)

        # Move to the next view
        self.show_view("FCFSAnimationView")
        
    def get_fcfs_mem(self) -> FCFSMem:
        """Returns the list of proceses of the queue"""
        return self.model.fcfs_mem

    def get_num_processes(self) -> int:
        """ get the number of processes to be executed  """
        return len(self.model.new_processes)
    
    def move_to_bcp_table(self):
        """Move to the bcp  table and pause the simulation"""

        # Pause the simulation
        if self.model.current_process is not None:
            self.model.event_pause.set()
        self.show_view("FCFSBCPView")

    def get_total_process(self) -> ListProcesses:
        """Get processes all processes"""
        return self.model.processes

    def move_to_animation(self):
        """Move to the finishing table"""

        # Unpaused the simulaion
        if self.model.current_process is not None and self.model.event_pause.is_set():
            self.model.event_pause.clear()

        self.show_view("FCFSAnimationView")

    def run(self):
        """Runs the fcfs simulation"""
        self.model.load_fcfs_mem()

        # Run the memory in another thread
        Thread(target = self.model.fcfs_mem.run).start()
        sleep(1)

        while not self.model.new_processes.empty() or not self.model.fcfs_mem.empty():
            self.model.load_fcfs_mem()
            sleep(1)


class ControllerRR(ControllerFCFS):
    """The controller for the simulation of Round Robin algorithm"""
    def __init__(self):        
        self.quantum_val = MIN_QUANTUM_VAL
        super().__init__("RR", default_init_view_name = "RandomNumViewAndQuantum")

    def get_quantum(self):
        """Get quantum value"""
        return self.quantum_val

    def _add_new_rand_process(self, event):
        """Adds a new random process to the list of processes"""
        self.amount_processes += 1
        process = generate_random_process(self.amount_processes)
        rr_process = RRProcess(process.name, process.num)
        rr_process.set_process(process)
        self.model.processes.add(rr_process)
        self.model.new_processes.add(rr_process)
        self.view.update_widgets()
        INFO("Added a new random process")

    def move_to_animation(self):
        """Overides the previous move to the animation"""
        
        # Unpaused the simulaion
        if self.model.current_process is not None and self.model.event_pause.is_set():
            self.model.event_pause.clear()

        self.show_view("RRAnimationView")


    def gen_random_processes(self):
        """It will genreate random processes"""
        try:
            self.amount_processes = int(self.view.spin_amount_processes.get())
            self.quantum_val = int(self.view.spin_quantum.get())
        except ValueError as error:
            messagebox.showerror("showerror", f"Invalid number of introduced processes: {error}")
            return

        if self.amount_processes <= 0:
            messagebox.showerror("showerror",
                                 "Invalid number of introduced processes: can't be lesser or equal to zero")
            return

        for i in range(1, self.amount_processes + 1):
            process = generate_random_process(i)
            rr_process = RRProcess(process.name, process.num, self.quantum_val)
            rr_process.set_process(process)
            self.model.processes.add(rr_process)
            self.model.new_processes.add(rr_process)

        INFO(self.model.processes)
        INFO(self.model.new_processes)

        # Move to the next view
        self.show_view("RRAnimationView")
        
        

def create_controller(controller = "Batches") -> Controller:
    """To create an specific controller to deal with the view"""
    if controller == "Batches":
        return ControllerBatches()
    elif controller == "RandomBatches":
        return ControllerRandom()
    elif controller == "FCFS":
        return ControllerFCFS()
    elif controller == "RR":
        return ControllerRR()
    
    assert 0, "Unknown controller my friend"
