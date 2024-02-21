"""
The configs of the project
"""

MAX_NUMBER_OF_PROCESS = 64
MIN_NUMBER_OF_PROCESS = 1
MAX_BATCH_CAPACITY = 4
APP_TITLE = "Batch Processing Simulator in Python"
APP_GEOMETRY = "300x100"
OPERATIONS = ["+", "-", "*", "/", "%", "^"]
MAX_INT = 100
FONT = ("Arial", 12)

def INFO(*args):
    """A simple function to log information"""
    formatted_msg = "[INFO]: " + ' '.join(map(str, args))
    print(formatted_msg)
