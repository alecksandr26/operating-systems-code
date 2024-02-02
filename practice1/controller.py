
# Connets Model and View

from tkinter import *
from configurations import *
from model import Model, Process
from view import MainView, AnimationView, View

class Controller(Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)

        # Create the model and view
        self.model = Model()
        

        self.views = {}
        for F in (MainView, AnimationView, ):
            view_name = F.__name__
            view = F(parent = self)
            self.views[view_name] = view
            view.grid(row = 0, column = 0, sticky = "nsew")
        self.show_view("MainView")
            
    def show_view(self, view_name : View):
        # Show the selected view
        view = self.views[view_name]
        view.tkraise()

    def save_process(self, process_data : dict):
        process = Process(process_data["name"], process_data["id"])
        process.set_operation(process_data["operation_sym"],
                              process_data["first_operand"],
                              process_data["second_operand"],
                              process_data["execution_time"])
        self.model.add_process(process)


    def get_num_processes(self) -> int:
        return self.model.get_num_processes()
