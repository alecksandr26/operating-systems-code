
# Connets Model and View

from tkinter import *
from configurations import *
import model
import view

class Controller(Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)

        # Create the model and view
        self.model = model.Model()
        self.view = view.View(self)
        
        

