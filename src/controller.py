"""
The controller which controls the Model and the View part of the app
"""

from time import sleep
from abc import abstractmethod

from .model import Model, Process, Batch, ListProcesses, FCFSMem, FCFSProcess
from .view import VIEWS_CLASSES
from .utils import generate_random_process

from threading import Thread
from tkinter import *
from tkinter import messagebox
from src.configurations import *

class Controller(Tk):
    """A simple abstract class where to use as base to create new backends"""
    def __init__(self, default_view = "MainView"):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)
        
        INFO(default_view)

        # Create the model and view
        self.model = Model()
        self.view = None
        self.views = {}
        self.show_view(default_view)

        # Where to stored the thread
        self.thread = Thread(target = self.run)
        
        # Keyboard events
        self.bind("I", self._interruption_io_handler)
        self.bind("P", self._pause_handler)
        self.bind("C", self._resume_handler)
        self.bind("E", self._error_hanlder)

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

    def save_process(self, process_data : dict):
        """ Saving the process from data  """
        process = Process(process_data["name"], process_data["num"])
        process.set_operation(process_data["operation_sym"],
                              process_data["first_operand"],
                              process_data["second_operand"],
                              process_data["execution_time"])
        self.model.processes.add(process)

    def run_onclick(self):
        """ Executes all  the processes batch by batch  """
        self.thread.start()

        while True:
            self.view.update_widgets()

            # Wait until the thread is dead
            if not self.thread.is_alive():
                break
            
            if not self.model.event_pause.is_set():
                self.model.total_time += 1
                
            sleep(1)

class ControllerBatches(Controller):
    """ The Controller where the initial backend will be managed"""
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
            self.view.finished_processes_table.add_message(f"Batch: {self.model.batch_counter}")
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
    def __init__(self):
        super().__init__("RandomNumView")

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
            process = generate_random_process(i)
            fcfs_process = FCFSProcess(process.name, process.num)
            fcfs_process.set_process(process)
            self.model.processes.add(fcfs_process)

        INFO(self.model.processes)

        # Move to the next view
        self.show_view("FCFSAnimationView")
        
    def get_fcfs_mem(self) -> FCFSMem:
        """Returns the list of proceses of the queue"""
        return self.model.fcfs_mem
    
    def move_to_finishing_table(self):
        """Move to the finishing table"""
        if self.model.processes.empty():
            self.show_view("FCFSFinishingView")

    def run(self):
        """Runs the fcfs simulation"""
        self.model.load_fcfs_mem()

        # Run the memory in another thread
        Thread(target = self.model.fcfs_mem.run).start()
        sleep(1)
        
        while not self.model.processes.empty() or not self.model.fcfs_mem.empty():
            self.model.load_fcfs_mem()
            sleep(1)
            

def create_controller(controller = "Batches") -> Controller:
    """To create an specific controller to deal with the view"""
    if controller == "Batches":
        return ControllerBatches()
    elif controller == "RandomBatches":
        return ControllerRandom()
    elif controller == "FCFS":
        return ControllerFCFS()
    
    assert 0, "Unknown controller my friend"
