
class kenken_solver():
    def __init__(self):
        self.curr_domains = None
        self.nassigns = 0

    def empty_curr_domains(self):
        self.curr_domains = None
        self.nassigns=0

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
        return A == B or not kenken_solver.conflicting(A, a, B, b)

    def count(seq):
        """Count the number of items in sequence that are interpreted as true."""
        return sum(bool(x) for x in seq)

    def nconflicts(var, val, assignment,neighbors):
        """Return the number of conflicts var=val has with other variables."""
        # Subclasses may implement this more efficiently
        def conflict(var2):
            return (var2 in assignment and
                    not kenken_solver.constraint(var, val, var2, assignment[var2]))
        return kenken_solver.count(conflict(v) for v in neighbors[var])

    def support_pruning(self,domains,variables):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(domains[v]) for v in variables}

    def suppose(self,var, value,domains,variables):
        """Start accumulating inferences from assuming var=value."""
        kenken_solver.support_pruning(self,domains,variables)
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def choices(self,var,domains):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or domains)[var]

    def unordered_domain_values(self,var, assignment,domains):
        """The default value order."""
        return kenken_solver.choices(self,var,domains)

    def assign(self,var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1

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
        return kenken_solver.first([var for var in variables if var not in assignment])

    def prune(self,var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def forward_checking(self,var, value, assignment, removals,domains,variables,neighbors):
        """Prune neighbor values inconsistent with var=value."""
        kenken_solver.support_pruning(self,domains,variables)
        for B in neighbors[var]:
            if B not in assignment:
                for b in self.curr_domains[B][:]:
                    if not kenken_solver.constraint(var, value, B, b):
                        kenken_solver.prune(self,B, b, removals)
                if not self.curr_domains[B]:
                    return False
        return True

    def revise(self,Xi, Xj, removals):
        """Return true if we remove a value."""
        revised = False
        for x in self.curr_domains[Xi][:]:
            # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
            if all(not kenken_solver.constraint(Xi, x, Xj, y) for y in self.curr_domains[Xj]):
                kenken_solver.prune(self,Xi, x, removals)
                revised = True
        return revised

    def AC3(self,variables,neighbors,domains, queue=None, removals=None):

        if queue is None:
            queue = [(Xi, Xk) for Xi in variables for Xk in neighbors[Xi]]
        kenken_solver.support_pruning(self,domains,variables)
        while queue:
            (Xi, Xj) = queue.pop()
            if kenken_solver.revise(self,Xi, Xj, removals):
                if not self.curr_domains[Xi]:
                    return False
                for Xk in neighbors[Xi]:
                    if Xk != Xj:
                        queue.append((Xk, Xi))
        return True

    def mac(self,var, value, assignment, removals,domains,variables,neighbors):
        """Maintain arc consistency."""
        return kenken_solver.AC3(self,variables,neighbors,domains,[(X, var) for X in neighbors[var]], removals)

    def restore(self,removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)

    def unassign(var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]

    def goal_test(state,variables,neighbors):
        """The goal is to assign all variables, with all constraints satisfied."""
        assignment = dict(state)
        return (len(assignment) == len(variables) and all(kenken_solver.nconflicts(variables, assignment[variables], assignment,neighbors) == 0 for variables in variables))

    def backtracking_search(self,variables,domains,neighbors,inference="bk"):
        kenken_solver.empty_curr_domains(self)
        
        def backtrack(assignment):
            if len(assignment) == len(variables):
                return assignment
            var = kenken_solver.first_unassigned_variable(assignment, variables)
            for value in kenken_solver.unordered_domain_values(self,var, assignment, domains):
                if 0 == kenken_solver.nconflicts(var, value, assignment,neighbors):
                    kenken_solver.assign(self,var, value, assignment)
                    removals = kenken_solver.suppose(self,var, value ,domains,variables)
                    #suppose=> change curr_domains to make the car variable domain 
                    # contain only the assigned value and put other values in removals in case we needed to backtrack
                    if (inference == "bk"):
                        result = backtrack(assignment)
                        if result is not None:
                            return result
                    elif(inference == "fc"):
                        if(kenken_solver.forward_checking(self, var, value, assignment, removals,domains,variables,neighbors)):
                            result = backtrack(assignment)
                            if result is not None:
                                return result
                    elif(inference == "arc"):
                        if(kenken_solver.mac( self,var, value, assignment, removals,domains,variables,neighbors)):
                            result = backtrack(assignment)
                            if result is not None:
                                return result
                    kenken_solver.restore(self,removals)
            kenken_solver.unassign(var, assignment)
            return None

        result = backtrack({})
        assert result is None or kenken_solver.goal_test(result,variables,neighbors)
        return result
