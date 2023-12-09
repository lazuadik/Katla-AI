import random
import time

class WordleGuesserBrute:
    def __init__(self, words):
        self.domains = [i for i in words]
        self.yellow_state = {}
        self.gray_state = []
        self.green_state = [-1, -1, -1, -1, -1]
        self.guessed = []
    
    def guess(self):
        self.guessed.append(self.domains[0])
        return self.domains[0]

    def check(self, word):
        if word in self.guessed:
            return False
        
        for i in range(len(word)):
            if word[i] in self.gray_state and self.green_state[i] != word[i]:
                return False
            if word[i] in self.yellow_state and i in self.yellow_state[word[i]]:
                return False

        for i in self.yellow_state:
            if i[0] not in word:
                return False

        for i in range(len(self.green_state)):
            if self.green_state[i] != -1 and self.green_state[i] != word[i]:
                return False
        return True

    def decrease_domain(self, feedback, guessed_word):
        for i in range(len(feedback)):
            if feedback[i] == 2:
                self.green_state[i] = guessed_word[i]
                if guessed_word[i] in self.yellow_state:
                    del self.yellow_state[guessed_word[i]]
            elif feedback[i] == 1:
                if guessed_word[i] not in self.yellow_state:
                    self.yellow_state[guessed_word[i]] = [i]
                else:
                    self.yellow_state[guessed_word[i]].append(i)
        
        for i in range(len(feedback)):
            if feedback[i] == 0 and guessed_word[i] not in self.green_state and guessed_word[i] not in self.yellow_state and guessed_word[i] not in self.gray_state:
                self.gray_state.append(guessed_word[i])
        

        temp = [i for i in self.domains]
        for word in temp:
            if not self.check(word):
                self.domains.remove(word)

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
    choose_time_exec = []
    resp_time_exec = []
    solve_time_exec = []
    freq = []
    for target in words:
        try:
            guesser = WordleGuesserBrute(words)
            solve_start_time = time.time()
            step = 0
            choose_time = ''
            resp_time = ''
            while True:
                step += 1
                choose_start_time = time.time()
                guessed_word = guesser.guess()
                choose_end_time = time.time()

                AIfeedback = get_feedback(guessed_word, target)

                resp_start_time = time.time()
                guesser.decrease_domain(AIfeedback, guessed_word)
                resp_end_time = time.time()

                if(guessed_word == target):
                    print(guessed_word)
                    choose_time_exec.append(choose_time+f"{(choose_end_time-choose_start_time)*1000}\n")
                    resp_time_exec.append(resp_time+f"{(resp_end_time-choose_start_time)*1000}\n")
                    freq.append(str(step)+'\n')
                    break
                choose_time += f"{(choose_end_time-choose_start_time)*1000};"
                resp_time += f"{(resp_end_time-resp_start_time)*1000};"
        except:
            print("Exception!")
            return 0
        solve_end_time = time.time()
        solve_time_exec.append(f"{(solve_end_time-solve_start_time)*1000}\n")
    
    open("Testing/CSP/Result/brute-prune-choose.txt", "w").writelines(choose_time_exec)
    open("Testing/CSP/Result/brute-prune-feedback-response.txt", "w").writelines(resp_time_exec)
    open("Testing/CSP/Result/brute-prune-solve.txt", "w").writelines(solve_time_exec)
    open("Testing/CSP/Result/brute-prune-step.txt", "w").writelines(freq)

if __name__ == "__main__":
    main()