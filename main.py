"""
The main file for running the main program.
"""
import sys
from src.controller import create_controller

def main() -> int:
    """
    main: This function emulates the main c program function
    It will initialized the controller and run the other things
    """
    controller = create_controller("FCFS")
    controller.mainloop()

    return 0

if __name__ == "__main__":
    sys.exit(main())
