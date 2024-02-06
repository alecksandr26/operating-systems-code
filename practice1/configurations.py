
MAX_AMOUNT_OF_PROCESS = 64
MIN_AMOUNT_OF_PROCESS = 1
BATCH_SIZE = 4
APP_TITLE = "Batch Processing Simulator in Python"
APP_GEOMETRY = "300x100"
OPERATIONS = ["+", "-", "*", "/", "%", "^"]

MAX_INT = 100

def INFO(*args):
    formatted_msg = "[INFO]: " + ' '.join(map(str, args))
    print(formatted_msg)

