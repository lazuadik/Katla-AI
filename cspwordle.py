from collections import Counter

class CSPWordle:
    def __init__(self, domains, trie):
        self.trie = trie
        self.domains = {v: list(domains) for v in range(5)}
        self.yellow_state = []
        self.green_state = [-1 for _ in range(5)]
    
    def choices(self, var):
        return self.domains[var]

    def prune(self, var, value, removals):
        self.domains[var].remove(value)
        removals.append((var, value))
    
    def restore(self, removals):
        for var, val in removals:
            self.domains[var].append(val)
        
    def yellow_state_constraints(self, assignment):
        counter = Counter(self.yellow_state)
        counter_val = Counter(list(''.join(assignment[i] for i in range(5))))
        for i in self.yellow_state:
            if counter[i] > counter_val[i]:
                return False
        return True
    
    def is_conflict(self, value, varPos):
        if value in varPos.children:
            return False
        else:
            return True

    def domainCombinations(self, var):
        res = len(self.domains[var])
        for i in range(var+1, 5):
            res *= len(self.domains[i])
        return res

    def update_domain(self, note):
        dup_yellow = []
        for i in range(5):
            if note[i][1] == 0:
                if note[i][0] in self.domains[i] and note[i][0] in self.yellow_state:
                    self.domains[i].remove(note[i][0])
                elif note[i][0] not in self.yellow_state:
                    for v in range(5):
                        if note[i][0] in self.domains[v] and self.green_state[v] != note[i][0]:
                            self.domains[v].remove(note[i][0])
            elif note[i][1] == 1:
                if note[i][0] in self.domains[i]:
                    self.domains[i].remove(note[i][0])
                if note[i][0] not in self.yellow_state or note[i][0] in dup_yellow:
                    dup_yellow.append(note[i][0])
                    self.yellow_state.append(note[i][0])
            elif note[i][1] == 2:
                del self.domains[i]
                self.domains[i] = [note[i][0]]
                if note[i][0] in self.yellow_state and self.green_state[i] == -1:
                    self.yellow_state.remove(note[i][0])
                self.green_state[i] = note[i][0]