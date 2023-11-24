def check(str):
    for i in str:
        if ord(i) < ord('a') or ord(i) > ord('z'):
            return False
    return True

f = open("dictionary.txt", "rb").read().decode().split("\n")
print(len(f))

ans = []
p = open("wordle-dictionary.txt", "w")

for i in f:
    if len(i) == 5 and check(i):
        ans.append(i)
        p.write(i+"\n")
p.close()

