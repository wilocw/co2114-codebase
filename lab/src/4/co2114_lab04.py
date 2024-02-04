"""CO2114_LAB07.PY

Use this file to edit your Python code and 
  try the exercises in Lab 03
"""
from optimisation.planning import *

## Write your class definitions here



##
def main(graphical=True):
    """ Main method for running script code """
    
    # initialise your agents and add to environment here





#########################################################
##        DEMONSTRATION CODE                           ##
##          Generate maze from preset                  ##


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
    args = parser.parse_args()
    if args.test:
        from agent.engine import ClockApp
        print("Running Demo Code")
        ClockApp.run_default()
    elif args.demo:
        NotImplemented
    else:
        main(not args.disable_gui)