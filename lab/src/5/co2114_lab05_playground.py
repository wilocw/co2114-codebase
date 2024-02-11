"""CO2114_LAB05.PY

Use this file to edit your Python code and 
  try the exercises in Lab 05
"""
import math
import random
import numpy as np
from copy import deepcopy

from constraints.csp import *
from constraints.magic import *
from constraints.sudoku import *


class Timetabling(ConstraintSatisfactionProblem):
    def __init__(self):
        domain = [11, 13, 15]
        variables = {
            id: Variable(domain, name=id)
                for id in ['A','B','C','D','E','F','G']}

        neq = lambda x: x[0] != x[1]

        edges = [
            ('A','B'), ('A','C'), ('B','C'),
            ('B','D'), ('D','E'), ('B','E'),
            ('C','F'), ('E','F'), ('C','E'),
            ('E','G'), ('F','G')]

        constraints = {
            Factor(neq, (variables[x],variables[y]))
                for x,y in edges
        }
        super().__init__(list(variables.values()), constraints)


    def __repr__(self):
        return str({v.name: v.value for v in self.variables})
    

class Sudoku(ConstraintSatisfactionProblem):
    def __init__(self, init=None):
        if not init:
            init = SUDOKU_TEMPLATES['EASY']['0']
        
        template = np.matrix(init)
        n = template.shape[0]
        assert n in [4,9], f"Sudoku template must be 4x4 or 9x9"
        assert template.shape == (n,n), f"Sudoku template not valid: {template}"

        domain = set(range(1, n+1))
        self.grid = np.matrix([
            [Variable(domain, name=str((i,j))) for j in range(n)]
                for i in range(n)])
        for i in range(n):
            for j in range(n):
                if template[i,j] != 0: self.grid[i,j].value = template[i,j]

        constraints = set()
        m = int(math.sqrt(n))
        for i in range(m):
            for j in range(m):
                subgrid = self.grid[m*i:m*(i+1),m*j:m*(j+1)]
                constraints.add(
                    Factor(alldiff, aslist(subgrid)))
        for i in range(n):
            constraints.add(
                Factor(alldiff, aslist(self.grid[i,:])))
            constraints.add(
                Factor(alldiff, aslist(self.grid[:,i])))

        variables = aslist(self.grid)
        super().__init__(variables, constraints)

    def __repr__(self):
        return str(self.grid)


class BackTrackingAgent(CSPAgent):
    def solve(self, csp):
        return self.backtrack(csp)

    def choice(self, variables):
        return random.choice(variables)

    def backtrack(self, csp):
        if all(variable.is_assigned for variable in csp.variables):
            return csp
        
        variable = self.choice([
            variable for variable in csp.variables if not variable.is_assigned])

        for value in variable.domain:
            # print(f"{self}: trying {variable.name}={value}")
            variable.value = value
            if all(constraint.is_satisfied 
                    for constraint in csp.constraints 
                      if variable in constraint):
                print(f"{self}: \n{csp}")
                result = self.backtrack(deepcopy(csp))
                if result:
                    return result
            # print(f"{self}: backtracking")
            variable.value = None
        print(f"{self}: backtracking")
        return None

##
def main(
        graphical=True, problem="timetable",
        n=3, difficulty=None, **kwargs):
    """ Main method for running script code """
     
    # environment = MagicSquareEnvironment(n)
    # initialise your agents and add to environment here



    agent = BackTrackingAgent()

    match problem:
        case "timetable":
            csp = Timetabling()
        case "magic":
            csp = MagicSquare(n)
        case "sudoku":
            templates = SUDOKU_TEMPLATES[difficulty]

            key = random.choice(list(templates.keys()))
            csp = Sudoku(templates[key])

    solution = agent.solve(csp)
    print(f"final solution:\n{solution}")
    
    if problem == "sudoku":
        answers = SUDOKU_SOLUTIONS[difficulty]
        if key in answers:
            print("correct solution:")
            print(np.matrix(answers[key]))
    
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
    parser.add_argument("-g", "--disable_gui", action="store_true")
    parser.add_argument("-n", "--size", type=int, default=3)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--magic", action="store_true")
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
        main(not args.disable_gui, problem="timetable")
    elif args.magic:
        main(not args.disable_gui, args.steps, args.size, problem="magic")
    else:
        main(not args.disable_gui, difficulty=args.sudoku, problem="sudoku")