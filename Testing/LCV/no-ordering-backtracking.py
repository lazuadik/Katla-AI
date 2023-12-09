import random
import string
from collections import Counter
import time

class TrieNode:
    def __init__(self):
        self.children = {}
        self.numOfLeaf = 0

class Trie:
    def __init__(self, words):
        self.root = TrieNode()
        self.insert(words)

    def insert(self, words):
        for word in words:
            node = self.root
            for char in word:
                node.numOfLeaf += 1
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
    
    def search_node(self, path):
        node = self.root
        for i in range(len(path)):
            if path[i] not in node.children:
                return None
            node = node.children[path[i]]
        return node    

    def count_leaf(self, path, char):
        pos = self.search_node(path)
        if pos == None:
            return 0
        if char not in pos.children:
            return 0
        pos = pos.children[char]
        return pos.numOfLeaf

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

class WordleGuesser:
    def __init__(self, trie):
        self.csp = CSPWordle(string.ascii_uppercase, trie)
        self.firstStep = False
        self.backtrack_called = 0

    def lcv(self, var, assignment):
        # comb = self.csp.domainCombinations(var)
        return self.csp.choices(var)
        # return self.csp.choices(var)
    
    def forward_checking(self, var, value, assignmentPos, removals):
        if var == 4:
            return True
        temp = []
        for domain in self.csp.domains[var+1]:
            if self.csp.is_conflict(domain, assignmentPos.children[value]):
                temp.append(domain)
        
        for i in temp:
            self.csp.prune(var+1, i, removals)

        if not self.csp.domains[var+1]:
            return False
        return True

    def backtrack(self, assignment, assignmentPos):
        self.backtrack_called += 1
        # print(''.join(assignment[i] for i in range(len(assignment))))
        if self.firstStep:
            self.firstStep = False
            return self.first_step_function(assignment, assignmentPos)
        if len(assignment) == 5:
            return ''.join(assignment[i] for i in range(5)) if self.csp.yellow_state_constraints(assignment) else None
        var = len(assignment)
        for value in self.lcv(var, assignment):
            if not self.csp.is_conflict(value, assignmentPos):
                assignment[var] = value
                # removals = []
                # if self.forward_checking(var, value, assignmentPos, removals):
                result = self.backtrack(assignment, assignmentPos.children[value])
                if result is not None:
                    # self.csp.restore(removals)
                    return result
                # self.csp.restore(removals)
        if var in assignment:
            assignment.pop(var)
        return None
    
    def first_step_function(self, assignment, assignmentPos):
        if len(assignment) == 5:
            return ''.join(assignment[i] for i in range(5))
        var = len(assignment)
        dom = self.csp.domains[var]
        random.shuffle(dom)
        for value in dom:
            assignment[var] = value
            removals = []
            if value not in assignment:
                if self.forward_checking(var, value, assignmentPos, removals):
                    result = self.first_step_function(assignment, assignmentPos.children[value])
                    if result is not None:
                        self.csp.restore(removals)
                        return result
                self.csp.restore(removals)
        if var in assignment:
            assignment.pop(var)
        return None
    
    def feedback_processing(self, feedback, word):
        note = {i : (word[i], feedback[i]) for i in range(5)}
        self.csp.update_domain(note)

def get_feedback(word, target, AIfeedback=[-1 for _ in range(5)]):
    feedback = {}
    res = []
    temp = []
    for i in range(5):
        if word[i] == target[i]:
            feedback[i] = 2
            continue

        feedback[i] = 0
        if word[i] in target:
            res.append(i)
        temp.append(i)

    for i in res:
        for j in temp:
            if word[i] == target[j] and feedback[j] != 2 and AIfeedback[j] != 2:
                feedback[i] = 1
                temp.remove(j)
                break
    
    return [feedback[i] for i in range(5)]

def main():
    # words_target = [word.upper() for word in open("Testing/LCV/sample-lcv-3.txt", "r").read().split("\n")]
    words = [word.upper() for word in open("wordle-dictionary.txt", "r").read().split("\n")]
    trie = Trie(words)
    lines = []
    for target in words:
        # try:
            guesser = WordleGuesser(trie)
            # target = random.choice(words)
            # step = 0
            
            row = ""
            while True:
                # step += 1
                assignment = guesser.backtrack({}, guesser.csp.trie.root)
                back = guesser.backtrack_called

                guessed_word = ''.join(assignment)
                
                AIfeedback = get_feedback(guessed_word, target)
                guesser.feedback_processing(AIfeedback, guessed_word)
                if(guessed_word == target):
                    print(guessed_word)
                    lines.append(row+f"{back}\n")
                    break
                row += f"{back};"
                guesser.backtrack_called = 0
        # except:
        #     print("Exception!")
        #     return 0
        # break
    
    open("Testing/LCV/Result/no-ordering-backtracking.txt", "w").writelines(lines)


if __name__ == "__main__":
    main()