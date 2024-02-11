import numpy as np
import random
from agent.things import Thing, Agent
from collections.abc import Callable


def alldiff(variables):
    values = [
        variable.value for variable in variables 
            if variable.is_assigned]
    return len(set(values)) == len(values)


def aslist(npcol):
    return np.array(npcol).ravel().tolist()

class CSPAgent(Agent):
    def __repr__(self):
        return "🤖"


class ConstraintSatisfactionProblem:
    def __init__(self, variables, constraints):
        self.__variables = variables
        self.__constraints = constraints

    @property
    def variables(self):
        return self.__variables
    
    @property
    def domains(self):
        return {variable: variable.domain for variable in self.variables}

    @property
    def constraints(self):
        return self.__constraints
    

class Variable(Thing):
    def __init__(self, domain, name=None):
        self.__domain = domain
        self.__value = None
        self.name = name
        # self.__hash = name if name else random.random()

    @property
    def is_assigned(self):
        return self.__value is not None

    # def __hash__(self):
    #     return hash(self.__hash)

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, x):
        if x in self.domain or x is None:
            self.__value = x
        else:
            raise ValueError(f"{self.name}: {x} not in domain {self.domain}")

    def __repr__(self):
        return "?"

    @property
    def domain(self):
        return self.__domain
    
    # /def __eq__(self, x):
    #     return self.value == (x.value if isinstance(x, Variable) else x)

    def __repr__(self):
        return str(self.value) if self.is_assigned else super().__repr__()


class Factor(Thing):
    def __init__(self, constraint, variables):
        assert isinstance(constraint, Callable), "constraint must be callable"
        self.__function = constraint
        self.__variables = np.array(variables).ravel().tolist()

    def __call__(self, *args, **kwargs):
        return self.__function(*args, **kwargs)

    def __iter__(self):
        return iter(self.__variables)

    @property
    def is_satisfied(self):
        return self(self.__variables)
    
    def __repr__(self):
        return str(tuple([str(v.name) for v in self.variables]))

    @property
    def variables(self):
        return self.__variables
    


## NOT CURRENTLY VIABLE DO NOT USE
# from agent.environment import Environment 

# class __CSPEnvironment(Environment):
#     def __init__(self, problem, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.__csp = problem

#     @property
#     def csp(self):
#         return self.__csp

#     @property
#     def variables(self):
#         return self.csp.variables
    
#     @property
#     def constraints(self):
#         return self.csp.constraints

#     @property
#     def domains(self):
#         return self.csp.domains

#     @property
#     def is_done(self):
#         return all(variable.is_assigned for variable in self.variables) and \
#                  all(constraint.is_satisfied for constraint in self.constraints)

