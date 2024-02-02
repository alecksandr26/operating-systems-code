
# Displays data and handles user interactions

from tkinter import *
from tkinter import messagebox 
from tkinter.ttk import *
from configurations import *

from abc import ABC, abstractmethod
    
# Base method to build views from it 
class View(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # The parent window is the controller
        self.controller = parent

        # Show the view
        self.place(x = 0, y = 0)

        # Set the main title
        self.title_label = Label(self, text = APP_TITLE, font = ("Arial", 25))
        self.title_label.grid(row = 1, column = 1, columnspan = 7)

        # Create the rest of parts of the view
        self._build_widgets()

    @abstractmethod
    def _build_widgets(self):
        pass


class MainView(View):
    def __init__(self, parent):
        super().__init__(parent)

    def _build_widgets(self):
        # Set all the things to be displayed
        self.__build_entry_number_processes_widget()
        self.__build_entry_process()
        
    def __build_entry_number_processes_widget(self):
        # Set the input of the amount of processes
        Label(self, text = "No Processes: ").grid(row = 2, column = 1)
        self.spin_amount_processes = Spinbox(self,
                                             from_ = MIN_AMOUNT_OF_PROCESS, to = MAX_AMOUNT_OF_PROCESS,
                                             width = 5)
        self.spin_amount_processes.grid(row = 2, column = 2)
        
        Label(self, text = "Capturated processes: ").grid(row = 2, column = 3)
        self.number_processes_label = Label(self, text = "0")
        self.number_processes_label.grid(row = 2, column = 4)

        Button(self, text = "Run",
               command = self.__run_btn_oncliked_handler).grid(row = 3, column = 1, columnspan = 4)

        
    def __build_entry_process(self):
        Label(self, text = "Process information: ",
              font = ("Arial", 12)).grid(row = 4, column = 1, columnspan = 2, pady = 50)

        Label(self, text = "Name: ").grid(row = 5, column = 1)
        self.entry_name = Entry(self)
        self.entry_name.grid(row = 5, column = 2)
        
        Label(self, text = "Operation: ").grid(row = 6, column = 1, pady = 50)
        self.spin_first_operand = Spinbox(self, from_ = 0, to = MAX_INT, width = 5)
        self.spin_first_operand.grid(row = 6, column = 2)
        self.combo_operation_sym = Combobox(self, state = "readonly", values = ["+", "-", "*", "/"])
        self.combo_operation_sym.grid(row = 6, column = 3)
        self.spin_second_operand = Spinbox(self, from_ = 0, to = MAX_INT, width = 5)
        self.spin_second_operand.grid(row = 6, column = 4)

        Label(self, text = "ID: ").grid(row = 7, column = 1)
        self.entry_id = Entry(self)
        self.entry_id.grid(row = 7, column = 2)

        Label(self, text = "Execution time in seconds: ").grid(row = 7, column = 3)
        self.spin_execution_time = Spinbox(self, from_ = 0, to = MAX_INT, width = 5)
        self.spin_execution_time.grid(row = 7, column = 4)
        
        Button(self, text = "Add",
               command = self.__add_btn_oncliked_handler).grid(row = 8, column = 1, columnspan = 4, pady = 50)

    def __run_btn_oncliked_handler(self):
        # Evaluate the input
        try:
            amount_processes = int(self.spin_amount_processes.get())
        except ValueError:
            messagebox.showerror("showerror", "Invalid number of introduced processes")
            return
        
        if self.controller.get_num_processes() != amount_processes:
            messagebox.showerror("showerror", "Invalid number of introduced processes")
            return
        
        # Move to the next view
        self.controller.show_view(AnimationView.__name__)


    def __add_btn_oncliked_handler(self):
        # Build The process and send it to the controller
        # TODO: Validate the input user in a real way
        process_data = {}
        
        try:
            process_data["name"] = self.entry_name.get()
            process_data["operation_sym"] = self.combo_operation_sym.get()
            process_data["first_operand"] = int(self.spin_first_operand.get())
            process_data["second_operand"] = int(self.spin_second_operand.get())
            process_data["id"] = self.entry_id.get()
            process_data["execution_time"] = int(self.spin_execution_time.get())
        except ValueError:
            messagebox.showerror("showerror", "Invalid introduced Process")
            return

        self.controller.save_process(process_data)

        self.number_processes_label.config(text = f"{self.controller.get_num_processes()}")
        
class AnimationView(View):
    def __init__(self, parent):
        super().__init__(parent)
        
    def _build_widgets(self):
        pass
