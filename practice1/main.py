"""
The main file for running the main program.
"""

import sys
from controller import Controller

def main():
    """
    main: This function emulates the main c program function
    It will initialized the controller and run the other things
    """
    controller = Controller()
    controller.mainloop()

    return 0

if __name__ == "__main__":
    sys.exit(main())
