import random
words = [[] for _ in range(26)]
for word in open("wordle-dictionary.txt", "r").read().split("\n"):
   words[ord(word[0])-ord('a')].append(word)

f = open("Testing/LCV/sample-lcv.txt", "w")

for words_alf in words:
    for word in random.choices(words_alf, k=3):
        f.write(word+'\n')