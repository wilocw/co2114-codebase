"""CO2114_LAB03.PY

Use this file to edit your Python code and 
  try the exercises in Lab 03
"""
from search.things import *
from search.maze import *
from search.util import queue, stack, manhattan

## Write your class definitions here



##
def main(graphical=False, maze_preset=0):
    """ Main method for running script code """
    # write your non-class code here
    NotImplemented  # remove this line

#########################################################
##        DEMONSTRATION CODE                           ##
##                                                     ##


#########################################################
## DO NOT EDIT BELOW THIS LINE                         ##
##             UNLESS YOU KNOW WHAT YOU                ##
##                       ARE DOING                     ##

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog="co2114_lab03")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("-d", "--demo", action="store_true")
    parser.add_argument("-g", "--disable_gui", action="store_true")
    parser.add_argument("-m", "--preset", type=int, default=0)
    args = parser.parse_args()
    if args.test:
        from agent.engine import ClockApp
        print("Running Demo Code")
        ClockApp.run_default()
    elif args.demo:
        NotImplemented
    else:
        main(not args.disable_gui, args.preset)