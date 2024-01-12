"""CO2114_LAB02.PY

Use this file to edit your Python code and 
  try the exercises in Lab 02
"""
from agent.environment import *
from agent.things import *
from agent.colors import *

## Write your class definitions here


## 
def main(graphical=False):
    """ Main method for running script code """
    # write your non-class code here
    NotImplemented


#################################
## DO NOT EDIT BELOW THIS LINE ##
##   UNLESS YOU KNOW WHAT YOU  ##
##     ARE DOING               ##
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="co2114_lab02")
    parser.add_argument("-d","--demo", action="store_true")
    parser.add_argument("-g", "--graphical", action="store_true")
    args = parser.parse_args()
    if args.demo:
        from agent.engine import ClockApp
        print("Running Demo Code")
        ClockApp.run_default()
    else:
        main(args.graphical)