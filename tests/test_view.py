"""Testing the actual views"""
import unittest
from src.view import *
from src.configurations import *

import tkinter as tk
from tkinter import ttk

import pdb

class TestCaseProcessTableComponent(unittest.TestCase):
    def test_find_elements(self):
        """Test that elements can be finded in table"""
        # pdb.set_trace()
        root = tk.Tk()
        table = TableGUIComponent(root, columns = ["column1", "column2"])
        table.grid(row = 4, column = 3)
        table.add({"column1": 1, "column2": 2})
        self.assertEqual(table.find({"column1": 1, "column2": 2}), 0)


    def test_find_elements_big_data(self):
        """Test that elements can be finded in table"""
        # pdb.set_trace()
        root = tk.Tk()
        table = TableGUIComponent(root, columns = ["column1", "column2"])
        table.grid(row = 4, column = 3)
        table.add({"column1": 1.234234123521351, "column2": 2})
        self.assertEqual(table.find({"column1": 1.234234123521351, "column2": 2}), 0)
