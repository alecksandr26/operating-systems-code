"""
The controller which controls the Model and the View part of the app
"""

from time import sleep

from src.model import Model, Process, Batch, ListProcesses
from src.view import MainView, AnimationView

from threading import Thread
from tkinter import *
from tkinter import messagebox
from src.configurations import *

class Controller(Tk):
    """ The Controller where all the app is managed """
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)

        # Create the model and view
        self.model = Model()
        self.view = None
        self.views = {}
        for F in (MainView, AnimationView, ):
            view_name = F.__name__
            view = F(parent = self)
            self.views[view_name] = view
            view.grid(row = 0, column = 0, sticky = "nsew")
        self.show_view("MainView")

        # Where to stored the thread
        self.run_thread = Thread(target = self.run)
        
        # Keyboard events
        self.bind("I", self._interruption_io_handler)
        self.bind("P", self._pause_handler)
        self.bind("C", self._continue_handler)
        self.bind("E", self._error_hanlder)

    def _error_hanlder(self, event):
        """The hanlder of simulating an error"""
        INFO("Error has been ocurred in the current process!!!")
        if self.model.current_process is not None:
            self.model.current_process.event_error.set()

    def _interruption_io_handler(self, event):
        """A handler of the interruption"""
        INFO("Interrupting the current process!!!")
        if self.model.current_process is not None:
            self.model.current_process.event_interrupt.set()
            self.model.batch.add(self.model.current_process)
        
    def _pause_handler(self, event):
        """A handler of the interruption"""
        INFO("Pausing the current process!!!")
        if self.model.current_process is not None:
            self.model.current_process.event_pause.set()
            
    def _continue_handler(self, event):
        """A handler of the interruption"""
        INFO("Continuing the current process!!!")
        if self.model.current_process is not None and self.model.current_process.event_pause.is_set():
            self.model.current_process.event_pause.clear()

    def show_view(self, view_name : str):
        """ Show the actual view """
        self.view = self.views[view_name]
        self.view.update_widgets()
        self.view.tkraise()

    def save_process(self, process_data : dict):
        """ Saving the process from data  """
        process = Process(process_data["name"], process_data["num"])
        process.set_operation(process_data["operation_sym"],
                              process_data["first_operand"],
                              process_data["second_operand"],
                              process_data["execution_time"])
        self.model.processes.add(process)

    def get_num_processes(self) -> int:
        """ get the number of processes to be executed  """
        return len(self.model.processes)

    def get_num_batches(self) -> int:
        """ get the number of batches """
        return self.model.processes.num_batches(self.model.batch)

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


    def _run(self):
        """ Old version of the code Method to be executed in an thread"""
        self.model.batch_counter = 1
        # Until finshed with the pending batches
        while not self.model.processes.empty():
            # Load the batch
            self.view.finished_processes_table.add_message(f"Batch: {self.model.batch_counter}")
            self.model.batch_counter += 1
            self.model.processes.fill_batch(self.model.batch)

            self.view.update_num_pending_batches()
            self.view.update_batch()
            sleep(1)

            # Execute processes one by one
            while not self.model.batch.empty():
                self.model.current_process = self.model.batch.pop()
                process = self.model.current_process
                self.view.update_batch()
                self.view.update_current_process_execution()
                sleep(1)

                process.do_operation()
                process.actual_time = 0
                process.left_time = process.time
                while process.left_time > 0:
                    self.model.current_process.actual_time += 1
                    self.model.current_process.left_time -= 1
                    self.view.update_current_process_execution()
                    sleep(1)
                    
                self.model.total_time += process.time
                self.view.update_counting_time()

                # Append the process to the finsihed processes
                self.model.finished_processes.add(process)

                self.model.current_process = None
                self.view.update_current_process_execution()
                self.view.update_finished_list()

                sleep(1)

    def run(self):
        """Run all batches"""
        self.model.batch_counter = 1
        while not self.model.processes.empty():
            # Load the batch
            self.view.finished_processes_table.add_message(f"Batch: {self.model.batch_counter}")
            self.model.batch_counter += 1
            self.model.processes.fill_batch(self.model.batch)
            sleep(1.5)
            self.model.batch.run(self.model)
            

    def run_onclick(self):
        """ Executes all  the processes batch by batch  """
        self.run_thread.start()

        while True:
            sleep(1)
            self.view.update_widgets()
            # Wait until the thread is dead
            if not self.run_thread.is_alive():
                break
            self.model.total_time += 1
