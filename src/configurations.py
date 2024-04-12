"""
The configs of the project
"""


MAX_NUMBER_OF_PROCESS = 1024
MIN_NUMBER_OF_PROCESS = 1
MAX_BATCH_CAPACITY = 3
MAX_FCFS_QUEUE_CAPACITY = MAX_BATCH_CAPACITY
MAX_RR_QUEUE_CAPACITY = MAX_BATCH_CAPACITY
APP_TITLE = "OS Simulator in Python"
APP_GEOMETRY = "300x100"
OPERATIONS = ["+", "-", "*", "/", "%", "^"]
MAX_INT = 100
FONT = ("Arial", 12)
SUCCEEDED_PROCESS = 0
INTERRUPTED_PROCESS = 1
CRASHED_PROCESS = 2
COOLDOWN_TIME = 10
MIN_QUANTUM_VAL = 1
MAX_QUANTUM_VAL = 10

# states of the processes
class ProcessState:
    NEW = "new"
    READY = "ready"
    EXECUTING = "executing"
    FINISHED = "finished"
    BLOCKED = "blocked"

def INFO(*args):
    """A simple function to log information"""
    formatted_msg = "[INFO]: " + ' '.join(map(str, args))
    print(formatted_msg)
