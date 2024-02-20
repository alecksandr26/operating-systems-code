"""Testing the actual models"""
import unittest
from src.model import *
from src.configurations import *

class TestCaseProcessModel(unittest.TestCase):
    """Testing the model process and check if it works"""
    def test_run_process(self):
        """Test the correct result of the model"""
        process = Process("Pedrito", 1)
        process.set_operation("+", 1, 2, 1)
        process.do_operation()
        self.assertEqual(process.result, 3)
        
class TestCaseBatchModel(unittest.TestCase):
    """Testing the batch model"""
    def test_batch_limit(self):
        """Testing the limit of the batch capacity"""
        batch = Batch(MAX_BATCH_CAPACITY)
        self.assertEqual(batch.capacity(), MAX_BATCH_CAPACITY)
        assertion_executed = False
        try:
            while not batch.fill():
                batch.add(Process("Pedrito", 1))
        except AssertionError:
            assertion_executed = True
        self.assertFalse(assertion_executed)



class TestCaseListProcesses(unittest.TestCase):
    """Testing the list processes"""
    def test_listprocesses_fill_batch(self):
        """Testing the list processes"""
        batch = Batch(MAX_BATCH_CAPACITY)
        processes = ListProcesses([Process("pedrito", 1), Process("pedrito", 1),
                                   Process("pedrito", 1), Process("pedrito", 1)])
        processes.fill_batch(batch)

        self.assertEqual(len(processes), 0)
        self.assertEqual(len(batch), 4)
