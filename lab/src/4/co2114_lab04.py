"""CO2114_LAB07.PY

Use this file to edit your Python code and 
  try the exercises in Lab 03
"""
import math
import random

from optimisation.planning import *
from optimisation.things import *

## Write your class definitions here


##
def main(graphical=True, steps=100, **kwargs):
    """ Main method for running script code """
    environment = generate_hospital_placement_env(**kwargs)  

    # initialise your agents and add to environment here

    # agent = ...
    # environment.add_agent(agent)

    if graphical:
        # change lps to change simulation loops per second
        environment.run(steps=steps, graphical=graphical, lps=8)
    else:
        environment.run(steps=steps, graphical=graphical)


#########################################################
##        DEMONSTRATION CODE                           ##
##          Generate maze from preset                  ##
def generate_hospital_placement_env(
        preset="0", hospitals=None, houses=None, height=None, width=None):
    """ Generates hospital environment based on arguments """
    if (hospitals and houses) or preset == "empty":
        environment = HospitalPlacement(
                    PRESET_STATES["empty"],
                    height = 10 if not height else height,
                    width = 20 if not width else width)
        for _ in range(8 if not houses else houses):
            environment.add_thing_randomly(House())
        for _ in range(3 if not hospitals else hospitals):
            environment.add_thing_randomly(Hospital())
    else:
        environment = HospitalPlacement(PRESET_STATES[preset])
        match preset:
            case '2':
               for _ in range(2 if not hospitals else hospitals):
                    environment.add_thing_randomly(Hospital())
    return environment

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
    parser.add_argument(
        "--houses", type=int, help="number of houses in environment")
    parser.add_argument(
        "--hospitals", type=int, help="number of hospitals to place")
    parser.add_argument(
        "-y", "--height", type=int, help="number of cells in y axis")
    parser.add_argument(
        "-x", "--width", type=int, help="number of cells in x axis")
    parser.add_argument(
        "--preset", choices=list(PRESET_STATES.keys()))
    parser.add_argument(
        "-t", "--steps", type=int, default=100, help="number of steps")
    args = parser.parse_args()
    if args.test:
        from agent.engine import ClockApp
        print("Running Demo Code")
        ClockApp.run_default()
    elif args.demo:
        NotImplemented
    else:
        if args.hospitals and args.houses:
            main(not args.disable_gui, steps=args.steps,
                hospitals=args.hospitals, 
                houses=args.houses,
                height=args.height,
                width=args.width)
        if args.preset:
            main(not args.disable_gui, steps=args.steps, preset=args.preset, hospitals=args.hospitals)
        else:
            main(not args.disable_gui, args.steps)