"""CO2114_LAB07.PY

Use this file to edit your Python code and 
  try the exercises in Lab 03
"""
from optimisation.planning import *
from optimisation.things import *

import math
import random


## Write your class definitions here
class HillClimbOptimiser(HospitalOptimiser):
        
    def program(self, percepts):
        state, neighbours = percepts
        objective = self.utility(state)

        print(f"{self}: current distance {-objective}")
        print(f"{self}: possible new objectives {[-self.utility(n) for n in neighbours]}")
        
        choice = self.maximise_utility(neighbours)

        if self.utility(choice) > objective:
            return ("explore", choice)
        return ("done", None)


class SimulatedAnnealingOptimiser(HospitalOptimiser):
    def __init__(self, num_steps=100):
        super().__init__()
        self.t, self.tmax = 0, num_steps

    
    def temperature(self, t):
        return 1 - t/self.tmax
    
    def probability(self, delta, T):
        # delta < 0
        return math.exp(delta/T) if T > 0 else 0

    def program(self, percepts):
        state, neighbours = percepts
        if self.t == self.tmax:
            return ("done", self.global_maxima)

        T = self.temperature(self.t)
        self.t += 1

        candidate = random.choice(neighbours)
        value = self.utility(candidate)
        delta = value - self.utility(state)
        
        if not hasattr(self, "global_maxima"):
            self.global_maxima = state

        print(f"{self}: (t{self.t}) considering candidate with distance {-value} and Δ={delta} (global minima {-self.utility(self.global_maxima)})")

        P = self.probability(delta, T)
        if delta > 0:
            if value > self.utility(self.global_maxima):
                self.global_maxima = candidate
            return ("explore", candidate)
        elif random.uniform(0, 1) < P:
            print(f"{self}: accepted candidate with probability {P}")
            return ("explore", candidate)
        else:
            print(f"{self}: rejected candidate (P={P})")
        return ("explore", None)


##
def main(graphical=True, steps=100, **kwargs):
    """ Main method for running script code """
    
    environment = generate_hospital_placement_env(**kwargs) 
    # initialise your agents and add to environment here
    
    agent = HillClimbOptimiser()
    agent = SimulatedAnnealingOptimiser(steps)

    environment.add_agent(agent)
    environment.run(steps=steps, graphical=graphical, lps=8)


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
            case '0':
               pass  # already has hospitals
            case '1':
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
        if args.preset:
            main(not args.disable_gui, steps=args.steps, preset=args.preset)
        elif args.hospitals and args.houses:
            main(not args.disable_gui, steps=args.steps,
                hospitals=args.hospitals, 
                houses=args.houses,
                height=args.height,
                width=args.width)
        else:
            main(not args.disable_gui, args.steps)