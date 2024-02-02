
# Displays data and handles user interactions

from tkinter import *
from configurations import *

class View(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Show the view 
        self.place(x = 0, y = 0)

        # Create the rest of parts of the view
        self.__create_widgets()

    def __create_widgets(self):

        # Set all the things to be displayed

        # Set the main title
        self.title_label = Label(self, text = APP_TITLE, font = ("Arial", 25))
        self.title_label.grid(row = 1, column = 1, columnspan = 3)

        self.__create_enter_number_processes_widget()
        
        
    def __create_enter_number_processes_widget(self):
        # Set the input of the amount of processes
        Label(self, text = "No Processes: ").grid(row = 2, column = 1)
        self.spinbox = Spinbox(self, from_ = 0, to = MAX_AMOUNT_OF_PROCESS, width = 5)
        self.spinbox.grid(row = 2, column = 2)
        self.run_btn = Button(self, text = "Run!!", command = self.__run_btn_oncliked_handler)
        self.run_btn.grid(row = 3, column = 1)

    def __create_entry_process(self):
        pass
    

    def __run_btn_oncliked_handler(self):
        pass
    
        
    def set_controller(self, controller):
        self.controller = controller



