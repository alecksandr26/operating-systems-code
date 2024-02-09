"""
The controller which controls the Model and the View part of the app
"""

from time import sleep
from model import Model, Process
from view import MainView, AnimationView
from tkinter import *
from tkinter import messagebox
from configurations import *



class Controller(Tk):
    """ The Controller where all the app is managed """
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)

        # Create the model and view
        self.model = Model()
        self.view = None
        self.current_process = None
        self.views = {}
        for F in (MainView, AnimationView, ):
            view_name = F.__name__
            view = F(parent = self)
            self.views[view_name] = view
            view.grid(row = 0, column = 0, sticky = "nsew")
        self.show_view("MainView")

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
        self.model.add_process(process)


    def get_num_processes(self) -> int:
        """ get the number of processes to be executed  """
        return self.model.get_num_processes()

    def get_num_batches(self) -> int:
        """ get the number of batches """
        return self.model.get_num_batches()

    def get_processes(self) -> [Process]:
        """ get the list of processes """
        return self.model.get_processes()

    def get_cur_process(self) -> Process or None:
        """ get current processes been executed """
        return self.current_process

    def get_batch(self) -> [Process]:
        """ get the actual batch """
        assert len(self.model.get_batch()) <= BATCH_SIZE
        return self.model.get_batch()

    def get_finshed_processes(self) -> [Process]:
        """ get the finished processes """
        return self.model.get_finshed_processes()

    def get_total_time(self) -> int:
        """ get the total time of the processed """
        return self.model.total_time

    def add_process(self):
        """add a new process to the list of processes."""
        process_data = {}
        try:
            process_data["name"] = self.view.entry_name.get()
            process_data["num"] = int(self.view.spin_proces_num.get())
            for pro in self.get_processes():
                if pro.num == process_data["num"]:
                    raise ValueError("Name or Id is not unique")
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


    def run(self):
        """ Executes all  the processes batch by batch  """

        # Until finshed with the pending batches
        while self.get_num_processes() > 0:
            # Load the batch
            i = 0
            while i < BATCH_SIZE and self.get_num_processes() > 0:
                self.model.batch.append(self.model.processes.pop(0))
                i += 1

            self.view.update_num_pending_batches()
            self.view.update_batch_listbox()
            sleep(1)

            # Execute processes one by one
            while len(self.model.batch) > 0:
                self.current_process = self.model.batch.pop(0)
                self.view.update_batch_listbox()
                self.view.update_current_process_execution()

                self.current_process.do_operation()

                self.current_process.actual_time = 0
                self.current_process.left_time = self.current_process.execution_time
                while self.current_process.left_time > 0:
                    self.view.update_current_process_execution()
                    self.current_process.actual_time += 1
                    self.current_process.left_time -= 1
                    sleep(1)

                self.view.update_current_process_execution()
                sleep(1)

                self.model.total_time += self.current_process.execution_time
                self.view.update_counting_time()

                # Append the process to the finsihed processes
                self.model.finished_processes.append(self.current_process)

                self.current_process = None
                self.view.update_current_process_execution()
                self.view.update_finished_list()

                sleep(1)
