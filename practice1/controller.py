
# Connets Model and View

from tkinter import *
from tkinter import messagebox 
from configurations import *
from model import Model, Process
from view import MainView, AnimationView, View
from time import sleep


class Controller(Tk):
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
        # Show the selected view
        self.view = self.views[view_name]
        self.view.update_widgets()
        self.view.tkraise()

    def save_process(self, process_data : dict):
        process = Process(process_data["name"], process_data["id"])
        process.set_operation(process_data["operation_sym"],
                              process_data["first_operand"],
                              process_data["second_operand"],
                              process_data["execution_time"])
        self.model.add_process(process)


    def get_num_processes(self) -> int:
        return self.model.get_num_processes()

    def get_num_batches(self) -> int:
        return self.model.get_num_batches()

    def get_processes(self) -> [Process]:
        return self.model.get_processes()
    
    def get_cur_process(self) -> Process:
        return self.current_process

    def get_batch(self) -> [Process]:
        # The batches Can't have more data
        assert len(self.model.get_batch()) <= BATCH_SIZE
        return self.model.get_batch()

    def get_finshed_processes(self) -> [Process]:
        return self.model.get_finshed_processes()

    def get_total_time(self) -> int:
        return self.model.total_time

    def add_process(self):
        # Build The process and send it to the controller
        # TODO: Validate the input user in a real way
        process_data = {}
        
        try:
            process_data["name"] = self.view.entry_name.get()
            process_data["operation_sym"] = self.view.combo_operation_sym.get()
            process_data["first_operand"] = int(self.view.spin_first_operand.get())
            process_data["second_operand"] = int(self.view.spin_second_operand.get())
            # TODO: Check if that id alreay exist
            process_data["id"] = self.view.entry_id.get()
            process_data["execution_time"] = int(self.view.spin_execution_time.get())
        except ValueError as Error:
            messagebox.showerror("showerror", f"Invalid introduced Process: {Error}")
            return

        self.save_process(process_data)
        self.view.update_widgets()
    

    def prepare_to_run(self):
        try:
            amount_processes = int(self.view.spin_amount_processes.get())
        except ValueError as Error:
            messagebox.showerror("showerror", f"Invalid number of introduced processes: {Error}")
            return
        
        if self.get_num_processes() != amount_processes:
            messagebox.showerror("showerror", "Invalid number of introduced processes")
            return
        
        # Move to the next view
        self.show_view("AnimationView")


    def run_btn(self):
        # Until finshed with the pending batches
        while self.get_num_processes() > 0:
            # Load the batch
            
            i = 0
            while i < BATCH_SIZE and self.get_num_processes() > 0:
                self.model.batch.append(self.model.processes.pop())                
                i += 1
                
            self.view.update_num_pending_batches()
            self.view.update_batch_listbox()
            sleep(1)
            
            # Execute the one by one
            while len(self.model.batch) > 0:
                self.current_process = self.model.batch.pop()
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
                
            
