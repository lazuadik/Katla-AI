import random
import string
from trie import Trie
from cspwordle import CSPWordle
    
class WordleGuesser:
    def __init__(self, trie):
        self.csp = CSPWordle(string.ascii_uppercase, trie)
        self.firstStep = True

    def lcv(self, var, assignment):
        return sorted(self.csp.choices(var), key=lambda val: self.csp.trie.count_leaf(assignment, val), reverse=True)
    
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
        if self.firstStep:
            self.firstStep = False
            return self.first_step_function(assignment, assignmentPos)
        if len(assignment) == 5:
            return ''.join(assignment[i] for i in range(5)) if self.csp.yellow_state_constraints(assignment) else None
        var = len(assignment)
        for value in self.lcv(var, assignment):
            assignment[var] = value
            removals = []
            if self.forward_checking(var, value, assignmentPos, removals):
                result = self.backtrack(assignment, assignmentPos.children[value])
                if result is not None:
                    self.csp.restore(removals)
                    return result
            self.csp.restore(removals)
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
    words = [word.upper() for word in open("wordle-dictionary.txt", "r").read().split("\n")]
    trie = Trie(words)
    isDraw = False
    try:
        guesser = WordleGuesser(trie)
        target = random.choice(words)
        for t in range(8):
            assignment = guesser.backtrack({}, guesser.csp.trie.root)

            guessed_word = ''.join(assignment)

            AIfeedback = get_feedback(guessed_word, target)
            guesser.feedback_processing(AIfeedback, guessed_word)

            while True:
                user_input = input("Tebak kata: ").upper()
                if len(user_input) != 5:
                    print("Kata harus terdiri dari 5 huruf!")
                    continue
                if user_input not in words:
                    print("Kata tidak ada di KBBI!")
                    continue
                break

            userfeedback = get_feedback(user_input, target, AIfeedback)
            guesser.feedback_processing(userfeedback, user_input)
            print(guessed_word, end=" => ")
            for i in AIfeedback:
                if i == 0:
                    print("|  gray  ", end="")
                elif i == 1:
                    print("| yellow ", end="")
                else:
                    print("| green  ", end="")
            print("|")
            print(user_input, end=" => ")
            for i in get_feedback(user_input, target):
                if i == 0:
                    print("|  gray  ", end="")
                elif i == 1:
                    print("| yellow ", end="")
                else:
                    print("| green  ", end="")
            print("|")
            if (guessed_word == target and user_input == target):
                isDraw = True
                break
            elif guessed_word == target:
                print("You Lose")
                break
            elif user_input == target:
                print("You Win")
                break
            elif t == 7:
                isDraw = True
                break
        if isDraw:
            print("Draw!")
        print("Target: "+target)
        print(f"Lihat di KBBI! => https://kbbi.kemdikbud.go.id/entri/{target.lower()}")
    except:
        print("Exception!")
        return 0

if __name__ == "__main__":
    main()