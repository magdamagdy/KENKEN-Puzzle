from collections import defaultdict
from functools import reduce
import itertools
import re
import random

curr_domains = None
nassigns = 0

def empty_curr_domains():
    global curr_domains
    global nassigns
    curr_domains = None
    nassigns=0

def conflicting(A, a, B, b):
# To check that there is no conflicting for any two variables that that every member of variable A
    # which shares the same row or column with a member of variable B must not have the same value

    for i in range(len(A)):
        for j in range(len(B)):
            mA = A[i]
            mB = B[j]

            ma = a[i]
            mb = b[j]
            if ((mA[0] == mB[0]) != (mA[1] == mB[1])) and ma == mb:
                return True

    return False

def constraint( A, a, B, b):
    # This function to satisfy the constraint of the game to every two variable that every member of variable A
        # which shares the same row or column with a member of variable B must not have the same value 
    return A == B or not conflicting(A, a, B, b)

def count(seq):
    """Count the number of items in sequence that are interpreted as true."""
    return sum(bool(x) for x in seq)

def nconflicts(var, val, assignment,neighbors):
    """Return the number of conflicts var=val has with other variables."""
    # Subclasses may implement this more efficiently
    def conflict(var2):
        return (var2 in assignment and
                not constraint(var, val, var2, assignment[var2]))
    return count(conflict(v) for v in neighbors[var])

def support_pruning(domains,variables):
    global curr_domains
    """Make sure we can prune values from domains. (We want to pay
    for this only if we use it.)"""
    if curr_domains is None:
        curr_domains = {v: list(domains[v]) for v in variables}

def suppose(var, value,domains,variables):
    global curr_domains
    """Start accumulating inferences from assuming var=value."""
    support_pruning(domains,variables)
    removals = [(var, a) for a in curr_domains[var] if a != value]
    curr_domains[var] = [value]
    return removals

def choices(var,domains):
    global curr_domains
    """Return all values for var that aren't currently ruled out."""
    return (curr_domains or domains)[var]

def unordered_domain_values(var, assignment,domains):
    """The default value order."""
    return choices(var,domains)

def assign(var, val, assignment):
    global nassigns
    """Add {var: val} to assignment; Discard the old value if any."""
    assignment[var] = val
    nassigns += 1

def first(iterable, default=None):
    """Return the first element of an iterable or the next element of a generator; or default."""
    try:
        return iterable[0]
    except IndexError:
        return default
    except TypeError:
        return next(iterable, default)

def first_unassigned_variable(assignment, variables):
    """The default variable order."""
    return first([var for var in variables if var not in assignment])

def prune(var, value, removals):
    global curr_domains
    """Rule out var=value."""
    curr_domains[var].remove(value)
    if removals is not None:
        removals.append((var, value))

def forward_checking(var, value, assignment, removals,domains,variables,neighbors):
    global curr_domains
    """Prune neighbor values inconsistent with var=value."""
    support_pruning(domains,variables)
    for B in neighbors[var]:
        if B not in assignment:
            for b in curr_domains[B][:]:
                if not constraint(var, value, B, b):
                    prune(B, b, removals)
            if not curr_domains[B]:
                return False
    return True

def revise(Xi, Xj, removals):
    global curr_domains
    """Return true if we remove a value."""
    revised = False
    for x in curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if all(not constraint(Xi, x, Xj, y) for y in curr_domains[Xj]):
            prune(Xi, x, removals)
            revised = True
    return revised

def AC3(variables,neighbors,domains, queue=None, removals=None):
    global curr_domains

    if queue is None:
        queue = [(Xi, Xk) for Xi in variables for Xk in neighbors[Xi]]
    support_pruning(domains,variables)
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(Xi, Xj, removals):
            if not curr_domains[Xi]:
                return False
            for Xk in neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True

def mac(var, value, assignment, removals,domains,variables,neighbors):
    global curr_domains
    """Maintain arc consistency."""
    return AC3(variables,neighbors,domains,[(X, var) for X in neighbors[var]], removals)

def restore(removals):
    global curr_domains
    """Undo a supposition and all inferences from it."""
    for B, b in removals:
        curr_domains[B].append(b)

def unassign(var, assignment):
    """Remove {var: val} from assignment.
    DO NOT call this if you are changing a variable to a new value;
    just call assign for that."""
    if var in assignment:
        del assignment[var]

def goal_test(state,variables,neighbors):
    """The goal is to assign all variables, with all constraints satisfied."""
    assignment = dict(state)
    return (len(assignment) == len(variables) and all(nconflicts(variables, assignment[variables], assignment,neighbors) == 0 for variables in variables))

def backtracking_search(variables,domains,neighbors,inference="bk"):
    empty_curr_domains()
    
    def backtrack(assignment):
        if len(assignment) == len(variables):
            return assignment
        var = first_unassigned_variable(assignment, variables)
        for value in unordered_domain_values(var, assignment, domains):
            if 0 == nconflicts(var, value, assignment,neighbors):
                assign(var, value, assignment)
                removals = suppose(var, value ,domains,variables)
                if (inference == "bk"):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                elif(inference == "fc"):
                    if(forward_checking( var, value, assignment, removals,domains,variables,neighbors)):
                        result = backtrack(assignment)
                        if result is not None:
                            return result
                elif(inference == "arc"):
                    if(mac( var, value, assignment, removals,domains,variables,neighbors)):
                        result = backtrack(assignment)
                        if result is not None:
                            return result
                restore(removals)
        unassign(var, assignment)
        return None

    result = backtrack({})
    assert result is None or goal_test(result,variables,neighbors)
    return result
