"""CO2114_LAB05.PY

Use this file to edit your Python code and 
  try the exercises in Lab 05
"""
import math
import random
import numpy as np
from copy import deepcopy

from constraints.csp import *
from constraints.csp.util import *
from constraints.sudoku import *


def define_timetabling_csp():
    NotImplemented


class Sudoku(ConstraintSatisfactionProblem):
    """ For exercise 3 """
    def __init__(self, init=None):
        if not init:
            init = SUDOKU_TEMPLATES['EASY']['0']
        
        template = self.validate_template(init)

        self.create_variables(template)
        variables = aslist(self.grid)

        constraints = self.create_constraints(grid)

        super().__init__(variables, constraints)
    
    def validate_template(self, init):
        template = np.matrix(init)
        n = template.shape[0]
        assert n in [4,9], f"Sudoku template must be 4x4 or 9x9"
        assert template.shape==(n,n), f"Sudoku template invalid: {template}"
        
        self.n = n
        return template
    
    
    def create_variables(self, template):
        domain = set(range(1,self.n+1))
        self.grid = np.matrix([[Variable(domain, name=str((i,j))) 
                                    for j in range(n)]
                                for i in range(n)])
        for i in range(n):
            for j in range(n):
                if template[i,j] != 0: self.grid[i,j].value = template[i,j]

    def __repr__(self):
        return str(self.grid)

    def create_constraints(self):
        NotImplemented



def main(problem="timetable", difficulty="SIMPLE"):
    """ Main method for running script code """
    match problem:
        case "timetable":
            csp, solution = define_timetabling_csp(), None
        case "sudoku":
            csp, solution = generate_sudoku_csp(difficulty)
    environment = CSPRunnerEnvironment(csp, solution)

    # initialise your agents and add to environment here

    ## agent = ...
    ## environment.add_agent(agent)

    environment.run()


#########################################################
##        DEMONSTRATION CODE                           ##
##          Generate CSPRunner environment             ##
from agent.environment import Environment

class CSPRunnerEnvironment(Environment):
    def __init__(self, csp, solution=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csp = csp
        self.solution = solution
        self.__done = False

    @property
    def is_done(self):
        return self.__done

    def execute_action(self, agent, action):
        
        print(f"initial state:\n{self.csp}")
        input("Press enter to start solver")

        solution = agent.solve(self.csp)
        if solution:
            print(f"final solution:\n{solution}")
            if self.solution is not None:
                print(f"correct solution:\n{self.solution}")
        else:
            print("no solution found")
        self.__done = True

    def run(self, steps=None, pause_for_user=False):
        if pause_for_user:
            input("Press enter to start simulation")
        print(f"{self}: Running for {steps} iterations.")
        for i in range(steps if steps else 1):
            if self.is_done:
                if steps:
                    print(f"{self}: Simulation complete after {i} of {steps} iterations.")
                return
            self.step()
        if steps:
            print(f"{self}: Simulation complete after {steps} of {steps} iterations.")


def generate_sudoku_csp(difficulty="SIMPLE"):
    templates = SUDOKU_TEMPLATES[difficulty]
    solutions = SUDOKU_SOLUTIONS[difficulty]

    key = random.choice(list(templates.keys()))
    
    problem = templates[key]
    solution = np.matrix(solutions[key]) if key in solutions else None
    return Sudoku(problem), solution


#########################################################
## DO NOT EDIT BELOW THIS LINE                         ##
##             UNLESS YOU KNOW WHAT YOU                ##
##                       ARE DOING                     ##
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog="co2114_lab03")
    parser.add_argument("--test", action="store_true")
    # parser.add_argument("-g", "--disable_gui", action="store_true")
    parser.add_argument("-n", "--size", type=int, default=3)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("-d", "--sudoku", type=str, default="EASY",
                        choices=list(SUDOKU_TEMPLATES.keys()))
    parser.add_argument(
        "-t", "--steps", type=int, default=1000, help="number of steps")
    args = parser.parse_args()
    if args.test:
        from agent.engine import ClockApp
        print("Running Demo Code")
        ClockApp.run_default()
    elif args.demo:
        main(problem="timetable")
    else:
        main(difficulty=args.sudoku, problem="sudoku")