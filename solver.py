import string

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self, words):
        self.root = TrieNode()
        self.insert(words)

    def insert(self, words):
        for word in words:
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_end_of_word = True
    
    def search_node(self, path):
        node = self.root
        for i in range(len(path)):
            node = node.children[path[i]]
            if node == None:
                return None
        return node
        
    def count_child(self, path, char):
        pos = self.search_node(path)
        if pos == None:
            return 0
        if char not in pos.children:
            return 0
        pos = pos.children[char]
        return len(pos.children)

class CSP:
    def __init__(self, domains, trie):
        self.trie = trie
        self.domains = {v: list(domains) for v in range(5)}
        self.yellow_state = []
    
    def choices(self, var):
        return self.domains[var]

    def prune(self, var, value, removals):
        self.domains[var].remove(value)
        removals.append((var, value))
    
    def restore(self, removals):
        for var, val in removals:
            self.domains[var].append(val)
        
    def yellow_constraints(self, assignment):
        for i in self.yellow_state:
            if i not in assignment:
                return False
        return True
    
    def is_conflict(self, var, value, assignment, pos):        
        if var == 4 and self.yellow_constraints(assignment):
            return False
        elif value in pos.children:
            return False
        else:
            return True

    def update_domain(self, note):
        for i in range(5):
            if note[i][1] == 0:
                for v in range(5):
                    if note[i][0] in self.domains[v]:
                        self.domains[v].remove(note[i][0])
            elif note[i][1] == 1:
                if note[i][0] in self.domains[i]:
                    self.domains[i].remove(note[i][0])
                self.yellow_state.append(note[i][0])
            elif note[i][1] == 2:
                del self.domains[i]
                self.domains[i] = [note[i][0]]
                if note[i][0] in self.yellow_state:
                    self.yellow_state.remove(note[i][0])
    
class WordleGuesser:
    def __init__(self, words):
        self.csp = CSP(string.ascii_uppercase, Trie(words))

    def lcv(self, var, assignment):
        return sorted(self.csp.choices(var), key=lambda val: self.csp.trie.count_child(assignment, val), reverse=True)
    
    def forward_checking(self, var, value, assignment, assignment_pos, removals):
        if var == 4:
            return True
        for d in self.csp.domains[var+1]:
            if self.csp.is_conflict(var, d, assignment, assignment_pos.children[value]):
                # print(removals, value, assignment)
                # print(''.join(assignment[i] for i in range(var+1)), d, assignment_pos.children[value].children.keys())
                self.csp.prune(var+1, d, removals)
        print(''.join(assignment[i] for i in range(var+1)), assignment_pos.children[value].children.keys(), self.csp.domains[var+1])
        if not self.csp.domains[var+1]:
            return False
        return True

    def backtrack(self, assignment, assignment_pos):
        if len(assignment) == 5:
            return ''.join(assignment[i] for i in range(5))
        var = len(assignment)
        for value in self.lcv(var, assignment):
            print(self.csp.domains[var])
            if not self.csp.is_conflict(var, value, assignment, assignment_pos):
                # print(value)
                assignment[var] = value
                removals = []
                if self.forward_checking(var, value, assignment, assignment_pos, removals):
                    result = self.backtrack(assignment, assignment_pos.children[value])
                    # print(self.csp.domains)
                    if result is not None:
                        return result
                self.csp.restore(removals)
        if var in assignment:
            assignment.pop(var)
        return None
    
    def feedback_process(self, feedback, word):
        note = {i : (word[i], feedback[i]) for i in range(5)}
        self.csp.update_domain(note)

def get_feedback(word, target):
    feedback = []
    for i in range(5):
            if word[i] == target[i]:
                feedback.append(2)
            elif word[i] in target:
                feedback.append(1)
            else:
                feedback.append(0)
    return feedback

def main():
    target = "ANCUR"
    words = [word.upper() for word in open("dictionary5.txt", "r").read().split("\n")]

    guesser = WordleGuesser(words)
    
    while True:
        assignment = guesser.backtrack({}, guesser.csp.trie.root)
        
        guessed_word = ''.join(assignment[i] for i in range(5))
        
        AIfeedback = get_feedback(guessed_word, target)
        guesser.feedback_process(AIfeedback, guessed_word)

        while True:
            user_input = input("Tebak kata: ")
            if user_input not in words:
                print("Kata tidak ada di KBBI!")
                continue
            break
        userfeedback = get_feedback(user_input, target)
        guesser.feedback_process(userfeedback, user_input)

        print(guessed_word)
        print(AIfeedback)
        print(userfeedback)
        if guessed_word == target:
            print("You Lose")
            break
        elif user_input == target:
            print("You Win")
            break

if __name__ == "__main__":
    main()