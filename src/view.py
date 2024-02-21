"""
Displays data and handles user interactions
"""

from abc import abstractmethod
# import pdb
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

from src.configurations import *

class TableGUIComponent:
    """A simple useful table component"""
    def __init__(self, parent, columns : [str], height : int = 8, anchor = CENTER):
        self._columns = [col.lower() for col in columns]
        self._height = height
        
        self._listbox = Treeview(
            parent, column = tuple([f"c{i}" for i in range(1, len(columns) + 1)]),
            show = "headings", height = height
        )
        for i in range(1, len(columns) + 1):
            self._listbox.column(f"# {i}", anchor = anchor)
            self._listbox.heading(f"# {i}", text = columns[i - 1])

        self._scroll = Scrollbar(
            parent, orient = "vertical", command = self._listbox.yview
        )
        self._listbox.configure(yscrollcommand = self._scroll.set)
        self._changed = False
        self._number_elements = 0
        self._iter = 0

    def grid(self, row, column, rowspan = 1, columnspan = 1, pady = 0, padx = 0):
        """To set the component"""
        self._listbox.grid(row = row, column = column, rowspan = rowspan,
                           columnspan = columnspan, pady = pady, padx = padx)
        self._scroll.grid(row=row, column= column + columnspan - 1, rowspan=rowspan, pady=pady, padx=padx,
                          sticky="nse")


    def add(self, element : dict):
        """add a new element to the table """
        self._listbox.insert("", "end", f"{self._number_elements}",
                             values = tuple([element[key] for key in self._columns]))
        self._number_elements += 1

    def add_message(self, msg : str):
        """add a message in the current box"""
        self._listbox.insert("", "end", f"{self._number_elements}",
                             values = msg)
        self._number_elements += 1

    def find(self, element : dict) -> int:
        """trys to find an element"""
        vals = [element[key] for key in self._columns]
        for item in self._listbox.get_children(""):
            item_vals = self._listbox.item(item)["values"]
            if vals == item_vals:
                return int(item)
        return -1

    def delete(self, element : dict) -> int:
        """Trys to delete an element"""
        index = self.find(element)
        if index >= 0:
            self._listbox.delete(f"{index}")

    def delete_all(self):
        """deletes all the elements in the table"""
        for item in self._listbox.get_children(""):
            self._listbox.delete(item)

    def set_list(self, dict_list : [dict]):
        """sets a new list deleting the previous one"""
        self.delete_all()
        for dic in dict_list:
            self.add(dic)

    def empty(self) -> bool:
        """Checks if the table is empty"""
        return self._number_elements == 0

    def __getitem__(self, index : int) -> dict:
        assert index >= 0, "Invalid index"
        assert index < self._number_elements, "Invalid index"
        return self._listbox.item(f"{index}")["values"]

    def __iter__(self) -> iter:
        self._iter = 0
        return self

    def __next__(self) -> dict:
        if self._iter >= self._number_elements:
            raise StopAsyncIteration
        return self._listbox.item(f"{self._iter}")["values"]


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
               command = self.controller.prepare_to_run).grid(row = 3,
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
               command = self.controller.capture_process).grid(row = 8, column = 1,
                                                               columnspan = 4, pady = 50)

class AnimationView(View):
    """ The view with the animation """

    def __init__(self, parent):
        super().__init__(parent)
        self.n_pending_processes_label = None
        self.batch_table = None
        self.current_process_table = None
        self.finished_processes_table = None
        self.counting_time_label = None
        self.vsb = None

        # Create the rest of parts of the view
        self.build_widgets()

    def build_widgets(self):
        self.build_num_pending_batches()
        # List box of batch
        self.build_batch()

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


    def build_batch(self):
        """ build the batch list box """
        Label(self, text = "Batch: ",
              font = ("Arial", 12)).grid(row = 3, column = 1, pady = 20)
        self.batch_table = TableGUIComponent(
            self, columns = ["Num", "Time"]
        )
        self.batch_table.grid(row = 4, column = 1, rowspan = 3)

    def build_the_current_process_execution(self):
        """ build the gui of the process execution """
        Label(self, text = "Executing process: ",
              font = ("Arial", 12)).grid(row = 3, column = 2, pady = 20)
        self.current_process_table = TableGUIComponent(
            self, columns = ["Info", "Data"]
        )
        self.current_process_table.grid(row = 4, column = 2, rowspan = 2, padx = 50)

    def build_finished_list(self):
        """ build  the gui of the finished list """
        Label(self, text = "Finished: ",
              font = ("Arial", 12)).grid(row = 3, column = 3, pady = 20)
        self.finished_processes_table = TableGUIComponent(
            self, columns = ["Num", "Operation", "Result"]
        )
        self.finished_processes_table.grid(row = 4, column = 3, rowspan = 3)

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
               command = self.controller.run_onclick).grid(row = 8, column = 1)

    def update_widgets(self):
        self.update_num_pending_batches()
        self.update_batch()
        self.update_current_process_execution()
        self.update_finished_list()
        self.update_counting_time()

    def update_num_pending_batches(self):
        """ Update the pending batches """
        self.n_pending_processes_label.configure(
            text = f"No. Of pending batches:\t {self.controller.get_num_batches()}"
        )
        self.refresh()

    def update_batch(self):
        """ Update the batch listbox """
        self.batch_table.set_list([pro.get_data() for pro in self.controller.get_batch()])
        self.refresh()

    def update_current_process_execution(self):
        """ update the current process execution """
        curr_pro = self.controller.get_cur_process()
        process_fields = ["num", "name", "operation", "first_operand",
                          "second_operand", "time",
                          "actual_time", "left_time"]
        if not curr_pro is None:
            self.current_process_table.set_list(
                [{"info": key, "data": data} for key, data in curr_pro.get_data().items()]
            )
        else:
            self.current_process_table.delete_all()
            for key in process_fields:
                self.current_process_table.add({"info": key, "data": ""})
        self.refresh()


    def update_finished_list(self):
        """ update the finished list """
        finished_processes = self.controller.get_finshed_processes()
        if not finished_processes.empty():
            top_process = self.controller.get_finshed_processes().top()
            if self.finished_processes_table.find(top_process.get_data()) == -1:
                self.finished_processes_table.add(top_process.get_data())
        self.refresh()

    def update_counting_time(self):
        """ update counting time """
        self.counting_time_label.configure(
            text = f"Total time:\t {self.controller.get_total_time()}"
        )
        self.refresh()
