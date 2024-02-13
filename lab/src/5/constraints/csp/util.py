from collections.abc import Iterable
from collections import deque
from copy import deepcopy


class alldiff:
    def __call__(self, *variables):
        if len(variables) == 1:
            if not isinstance(variables[0], Iterable):
                return True
            print(variables[0])
            print("something")
            variables = variables[0]
        values = [
            variable.value for variable in variables 
                if variable.is_assigned]
        return len(set(values)) == len(values)


def aslist(npcol):
    return np.array(npcol).ravel().tolist()


def revise(factor, A, B):
    is_revised = False
    if A.is_assigned: return False
    for value in A.domain.copy():
        A.value = value
        is_valid_B = False
        for _value in B.domain:
            B.value = _value
            if factor.is_satisfied:
                is_valid_B = True
            B.value = None
        if not is_valid_B:
            A.domain.remove(value)
            is_revised = True
        A.value = None
    return is_revised


def ac3(csp, log=False, inplace=True):
    if not inplace: csp = deepcopy(csp)
    arcs = deque(csp.arcs)
    while len(arcs) > 0:
        f, A, B = arcs.popleft()  # end of queue
        if log:
            print(f"before: {A.name} in {A.domain}, {B.name} in {B.domain}")
        if revise(f, A, B):
            if log:
                print(f"after: {A.name} in {A.domain}, {B.name} in {B.domain}")
            if len(A.domain) == 0:
                return False if inplace else None
            for constraint in csp.constraints:
                if constraint.is_binary \
                        and A in constraint\
                            and B not in constraint:
                    for arc in constraint.arcs:
                        arcs.push(arc)
        elif log:
            print(f"after: {A.name} in {A.domain}, {B.name} in {B.domain} (no change)")
    return True if inplace else csp


def make_node_consistent(csp, inplace=True):
    if not inplace: csp = deepcopy(csp)
    for variable in csp.variables:
        if variable.is_assigned: continue  # ignore any assigned variables
        domain = variable.domain.copy()  # copy this to avoid set size change errors 
        for value in domain:
            variable.value = value
            for constraint in csp.constraints:
                if constraint.is_unary and variable in constraint:
                    if not constraint.is_satisfied:
                        variable.domain.remove(value)
                        break
            variable.value = None
    if not inplace: return csp