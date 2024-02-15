import math

from .csp import *
from .csp.util import *

SUDOKU_TEMPLATES = {}
SUDOKU_TEMPLATES['SIMPLE'] = {
    '0': [[0, 3, 4, 0],
          [4, 0, 0, 2],
          [1, 0, 0, 3],
          [0, 2, 1, 0]],
    '1': [[0, 0, 4, 0],
          [4, 0, 3, 0],
          [0, 4, 0, 3],
          [0, 1, 0, 0]],
    '2': [[0, 0, 1, 0],
          [4, 0, 0, 0],
          [0, 0, 0, 2],
          [0, 3, 0, 0]],
    '3': [[2, 0, 0, 0],
          [0, 0, 3, 0],
          [0, 4, 0, 0],
          [0, 0, 0, 1]],
    '4': [[1, 0, 4, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 1, 0, 2]],
    '5': [[0, 0, 0, 3],
          [3, 2, 4, 0],
          [0, 4, 3, 2],
          [2, 0, 0, 0]],
    '6': [[3, 4, 1, 0],
          [0, 2, 0, 0],
          [0, 0, 2, 0],
          [0, 1, 4, 3]],
    '7': [[0, 1, 3, 0],
          [2, 0, 0, 0],
          [0, 0, 0, 3],
          [0, 2, 1, 0]],
    '8': [[0, 0, 1, 0],
          [4, 0, 0, 0],
          [0, 0, 0, 2],
          [0, 3, 0, 0]]    
}
SUDOKU_TEMPLATES['EASY'] = {
      '0': [[3, 0, 5, 0, 0, 9, 0, 0, 2],
            [7, 0, 0, 8, 0, 5, 1, 9, 0],
            [0, 1, 9, 4, 7, 0, 0, 3, 0],
          [1, 0, 6, 0, 2, 4, 0, 0, 3],
          [0, 0, 8, 3, 5, 7, 0, 1, 9],
          [9, 5, 3, 0, 0, 0, 2, 7, 0],
          [0, 9, 1, 2, 4, 0, 3, 0, 0],
          [0, 3, 0, 7, 0, 6, 9, 0, 5],
          [2, 6, 0, 0, 9, 0, 4, 8, 0]]

}

SUDOKU_TEMPLATES['HARD'] = {
      '0': [[0, 0, 1, 8, 0, 0, 0, 0, 0],
            [6, 7, 0, 2, 0, 3, 0, 1, 0],
            [2, 0, 5, 7, 0, 0, 6, 0, 3],
            [3, 5, 0, 6, 2, 0, 8, 0, 0],
            [7, 6, 2, 0, 5, 8, 3, 0, 0],
            [0, 0, 0, 0, 0, 4, 0, 5, 0],
            [0, 9, 0, 5, 8, 6, 0, 0, 0],
            [5, 0, 0, 9, 0, 0, 7, 0, 0],
            [0, 2, 6, 4, 3, 0, 5, 9, 0]],
      '1': [[0, 0, 0, 9, 0, 0, 6, 7, 2],
            [0, 0, 2, 0, 0, 1, 0, 4, 3],
            [0, 3, 0, 0, 2, 6, 0, 0, 0],
            [4, 0, 0, 0, 0, 2, 0, 0, 9],
            [0, 0, 7, 3, 0, 9, 8, 0, 0],
            [5, 0, 0, 6, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 6, 0, 0, 9, 0],
            [0, 1, 0, 4, 0, 0, 3, 0, 0],
            [0, 7, 8, 0, 0, 5, 0, 0, 0]]
}

SUDOKU_SOLUTIONS = {}
SUDOKU_SOLUTIONS['SIMPLE'] = {}
SUDOKU_SOLUTIONS['EASY'] = {
      '0': [[3, 8, 5, 1, 6, 9, 7, 4, 2],
            [7, 4, 2, 8, 3, 5, 1, 9, 6],
            [6, 1, 9, 4, 7, 2, 5, 3, 8],
            [1, 7, 6, 9, 2, 4, 8, 5, 3],
            [4, 2, 8, 3, 5, 7, 6, 1, 9],
            [9, 5, 3, 6, 8, 1, 2, 7, 4],
            [5, 9, 1, 2, 4, 8, 3, 6, 7],
            [8, 3, 4, 7, 1, 6, 9, 2, 5],
            [2, 6, 7, 5, 9, 3, 4, 8, 1]]
}
SUDOKU_SOLUTIONS['HARD'] = {
    '0': [[9, 3, 1, 8, 6, 5, 4, 2, 7],
          [6, 7, 8, 2, 4, 3, 9, 1, 5],
          [2, 4, 5, 7, 9, 1, 6, 8, 3],
          [3, 5, 4, 6, 2, 9, 8, 7, 1],
          [7, 6, 2, 1, 5, 8, 3, 4, 9],
          [8, 1, 9, 3, 7, 4, 2, 5, 6],
          [4, 9, 7, 5, 8, 6, 1, 3, 2],
          [5, 8, 3, 9, 1, 2, 7, 6, 4],
          [1, 2, 6, 4, 3, 7, 5, 9, 8]],    
    '1': [[8, 5, 1, 9, 4, 3, 6, 7, 2],
          [6, 9, 2, 7, 8, 1, 5, 4, 3],
          [7, 3, 4, 5, 2, 6, 9, 1, 8],
          [4, 6, 3, 8, 1, 2, 7, 5, 9],
          [1, 2, 7, 3, 5, 9, 8, 6, 4],
          [5, 8, 9, 6, 7, 4, 2, 3, 1],
          [3, 4, 5, 2, 6, 8, 1, 9, 7],
          [2, 1, 6, 4, 9, 7, 3, 8, 5],
          [9, 7, 8, 1, 3, 5, 4, 2, 6]]
}


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