"""
Displays data and handles user interactions
"""

from abc import abstractmethod
# import pdb
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

from src.configurations import *





class View(Frame):
    """ Base method to build views from it """
    def __init__(self, parent):
        super().__init__(parent)

        # The parent window is the controller
        self.controller = parent

        # Show the view
        self.place(x = 0, y = 0)

        # Set the main title
        self.title_label = Label(self, text = APP_TITLE, font = ("Arial", 25))
        self.title_label.grid(row = 1, column = 1, columnspan = 7)

    @abstractmethod
    def build_widgets(self):
        """ Build the widgets needed for the View """       

    @abstractmethod
    def update_widgets(self):
        """ update the widgets needed for the View """

    def refresh(self):
        """ Refresh the frame """
        self.update()
        self.update_idletasks()


class MainView(View):
    """ MainView The main menu of the application """

    def __init__(self, parent):
        super().__init__(parent)
        self.spin_amount_processes = None
        self.number_processes_label = None

        self.spin_first_operand = None
        self.spin_second_operand = None
        self.combo_operation_sym = None
        self.entry_name = None
        self.spin_execution_time = None
        self.spin_proces_num = None

        # Create the rest of parts of the view
        self.build_widgets()

    def build_widgets(self):
        self.build_entry_number_processes_widget()
        self.build_entry_process()

    def update_widgets(self):
        self.number_processes_label.config(text = f"{self.controller.get_num_processes()}")
        self.refresh()


    def build_entry_number_processes_widget(self):
        """ build the first part of the """
        # Set the input of the amount of processes
        Label(self, text = "No. Processes: ",
              font = ("Arial", 12)).grid(row = 2, column = 1, pady = 50)
        self.spin_amount_processes = Spinbox(self,
                                             from_ = MIN_NUMBER_OF_PROCESS,
                                             to = MAX_NUMBER_OF_PROCESS,
                                             width = 5)
        self.spin_amount_processes.grid(row = 2, column = 2)

        Label(self, text = "Capturated processes: ",
              font = ("Arial", 12)).grid(row = 2, column = 3, pady = 50)
        self.number_processes_label = Label(self, text = "0")
        self.number_processes_label.grid(row = 2, column = 4, pady = 50)

        Button(self, text = "Continue",
               command = self.continue_btn_oncliked_handler).grid(row = 3,
                                                                  column = 1,
                                                                  columnspan = 4)

    def build_entry_process(self):
        """ Build the gui for entry a process """
        Label(self, text = "Process information: ",
              font = ("Arial", 12)).grid(row = 4, column = 1, columnspan = 2, pady = 50)

        Label(self, text = "Programmer name: ").grid(row = 5, column = 1)
        self.entry_name = Entry(self)
        self.entry_name.grid(row = 5, column = 2)

        Label(self, text = "Operation: ").grid(row = 6, column = 1, pady = 50)
        self.spin_first_operand = Spinbox(self, from_ = 0, to = MAX_INT, width = 5)
        self.spin_first_operand.grid(row = 6, column = 2)
        self.combo_operation_sym = Combobox(self, state = "readonly", values = OPERATIONS)
        self.combo_operation_sym.grid(row = 6, column = 3)
        self.spin_second_operand = Spinbox(self, from_ = 0, to = MAX_INT, width = 5)
        self.spin_second_operand.grid(row = 6, column = 4)

        Label(self, text = "Program's Num: ").grid(row = 7, column = 1)
        self.spin_proces_num = Spinbox(self, from_ = 1, to = MAX_INT, width = 5)
        self.spin_proces_num.grid(row = 7, column = 2)

        Label(self, text = "Execution time in seconds: ").grid(row = 7, column = 3)
        self.spin_execution_time = Spinbox(self,
                                           from_ = MIN_NUMBER_OF_PROCESS,
                                           to = MAX_INT, width = 5)
        self.spin_execution_time.grid(row = 7, column = 4)
        Button(self, text = "Add",
               command = self.add_btn_oncliked_handler).grid(row = 8, column = 1,
                                                             columnspan = 4, pady = 50)

    def continue_btn_oncliked_handler(self):
        """ the btn continue handler """
        self.controller.prepare_to_run()

    def add_btn_oncliked_handler(self):
        """ the btn add handler """
        self.controller.add_process()

class AnimationView(View):
    """ The view with the animation """

    def __init__(self, parent):
        super().__init__(parent)
        self.n_pending_processes_label = None
        self.batch_listbox = None
        self.current_process_listbox = None
        self.finished_processes_listbox = None
        self.counting_time_label = None
        self.vsb = None

        # Create the rest of parts of the view
        self.build_widgets()

    def build_widgets(self):
        self.build_num_pending_batches()
        # List box of batch
        self.build_batch_listbox()

        # Print the data of the process in execution
        self.build_the_current_process_execution()

        # Show another two lists with the actual processes and the finished ones
        self.build_finished_list()

        # Show the counter  and the button
        self.build_counting_time()
        self.build_the_run_button()

    def build_num_pending_batches(self):
        """ build the label of pending batches """
        self.n_pending_processes_label = Label(
            self,
            text = f"No. Of pending batches:\t {self.controller.get_num_batches()}",
            font = ("Arial", 12)
        )
        self.n_pending_processes_label.grid(row = 2, column = 1, pady = 20)


    def build_batch_listbox(self):
        """ build the batch list box """
        Label(self, text = "Batch: ",
              font = ("Arial", 12)).grid(row = 3, column = 1, pady = 20)
        self.batch_listbox = Treeview(self, column = ("c1", "c2"), show = "headings", height = 8)
        self.batch_listbox.column("# 1", anchor = CENTER)
        self.batch_listbox.heading("# 1", text = "Num")
        self.batch_listbox.column("# 2", anchor = CENTER)
        self.batch_listbox.heading("# 2", text = "Time")
        self.batch_listbox.grid(row = 4, column = 1, rowspan = 3)

    def build_the_current_process_execution(self):
        """ build the gui of the process execution """
        Label(self, text = "Executing process: ",
              font = ("Arial", 12)).grid(row = 3, column = 2, pady = 20)

        self.current_process_listbox = Treeview(self, column = ("c1", "c2"),
                                                show = "headings", height = 8)
        self.current_process_listbox.column("# 1", anchor = CENTER, stretch=NO, width=100)
        self.current_process_listbox.heading("# 1", text = "Info")
        self.current_process_listbox.column("# 2", anchor = CENTER)
        self.current_process_listbox.heading("# 2", text = "Data")

        self.current_process_listbox.grid(row = 4, column = 2, rowspan = 2, padx = 50)

    def build_finished_list(self):
        """ build  the gui of the finished list """
        Label(self, text = "Finished: ",
              font = ("Arial", 12)).grid(row = 3, column = 3, pady = 20)

        self.finished_processes_listbox = Treeview(self, column = ("c1", "c2", "c3"),
                                                   show = "headings", height = 8)
        self.finished_processes_listbox.column("# 1", anchor = CENTER,stretch=NO, width=180)
        self.finished_processes_listbox.heading("# 1", text = "Num")
        self.finished_processes_listbox.column("# 2", anchor = CENTER,stretch=NO, width=180)
        self.finished_processes_listbox.heading("# 2", text = "Operation")
        self.finished_processes_listbox.column("# 3", anchor = CENTER,stretch=NO, width=180)
        self.finished_processes_listbox.heading("# 3", text = "Result")
        self.finished_processes_listbox.grid(row = 4, column = 3, rowspan = 3)

        self.vsb = Scrollbar(
            self, orient="vertical", command = self.finished_processes_listbox.yview
        )
        self.vsb.place(relx=0.995, rely=0.444, anchor='center', height=160)
        self.finished_processes_listbox.configure(yscrollcommand = self.vsb.set)

    def build_counting_time(self):
        """ build the counting time gui """
        self.counting_time_label = Label(
            self, text = f"Total time:\t {self.controller.get_total_time()}",
            font = ("Arial", 12)
        )
        self.counting_time_label.grid(row = 7, column = 1, pady = 20)

    def build_the_run_button(self):
        """ The gui of the run button """
        Button(self, text = "Run",
               command = self.run_btn_oncliked_handler).grid(row = 8, column = 1)


    def run_btn_oncliked_handler(self):
        """ The handler on clicked run button """
        self.controller.run()

    def update_widgets(self):
        self.update_num_pending_batches()
        self.update_batch_listbox()
        self.update_current_process_execution()
        self.update_finished_list()
        self.update_counting_time()
        self.refresh()

    def update_num_pending_batches(self):
        """ Update the pending batches """
        self.n_pending_processes_label.configure(
            text = f"No. Of pending batches:\t {self.controller.get_num_batches()}"
        )
        self.refresh()

    def update_batch_listbox(self):
        """ Update the batch listbox """
        batch = self.controller.get_batch()
        for item in self.batch_listbox.get_children():
            item_vals = self.batch_listbox.item(item)["values"]
            finded = False
            for pro in batch:
                if pro.num == item_vals[0]:
                    finded = True
            if not finded:
                self.batch_listbox.delete(item)

        # Add the new ones
        for pro in batch:
            finded = False
            for item in self.batch_listbox.get_children():
                item_vals = self.batch_listbox.item(item)["values"]
                if pro.num == item_vals[0]:
                    finded = True
            if not finded:
                pro_data = pro.get_data()
                self.batch_listbox.insert("", "end",
                                          values = (pro_data["num"], pro_data["execution_time"]))
        self.refresh()

    def update_current_process_execution(self):
        """ update the current process execution """
        curr_pro = self.controller.get_cur_process()
        process_fields = ["num", "name", "operation_sym", "first_operand",
                          "second_operand", "execution_time",
                          "actual_time", "left_time"]
        for item in self.current_process_listbox.get_children():
            self.current_process_listbox.delete(item)

        if not curr_pro is None:
            data = curr_pro.get_data()
            for key in process_fields:
                self.current_process_listbox.insert("", "end", values = (key, data[key]))
        else:
            for key in process_fields:
                self.current_process_listbox.insert("", "end", values = (key, ""))
        self.refresh()


    def update_finished_list(self):
        """ update the finished list """
        for pro in self.controller.get_finshed_processes():
            finded = False
            for item in self.finished_processes_listbox.get_children():
                item_vals = self.finished_processes_listbox.item(item)["values"]
                if item_vals[0] == pro.num:
                    finded = True
            if not finded:
                pro_data = pro.get_data()
                self.finished_processes_listbox.insert(
                    "", "end",
                    values = (pro_data["num"],
                              str(pro_data["first_operand"])
                              + pro_data["operation_sym"]
                              + str(pro_data["second_operand"]),
                              pro_data["result"])
                )
            self.refresh()

    def update_counting_time(self):
        """ update counting time """
        self.counting_time_label.configure(
            text = f"Total time:\t {self.controller.get_total_time()}"
        )
        self.refresh()
