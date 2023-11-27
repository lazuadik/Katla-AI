from tkinter import messagebox
import tkinter as tk
from solver import *

root = tk.Tk()
root.title('Wordle')
frame = tk.Frame(root)
frame.pack()

# Variabel GUI
green = '#27e512'
yellow = '#e8ef0e'
gray = '#4c4c4c'
font = 'Verdana, 38'
letters = []
letter_count = 0
guess = ''
words = []
winner = False
wordleGuesser = None

with open('wordle-dictionary.txt', 'r') as file:
    data = file.readlines()
    for i in data:
        words.append(i[:-1])

def start_new_game():
    global letter_count, guess, winner, wordleGuesser
    layout()
    letter_count = 0
    guess = ''
    winner = False
    wordleGuesser = WordleGuesser(trie)

def key_pressed(event):
    global letter_count, guess, winner
    if not winner:
        if event.char.isalpha():
            if letter_count <= 29:
                letters[letter_count]['text'] = event.char.upper()
                letters[letter_count].focus()
                guess = guess + event.char.upper()
                letter_count += 1
                if letter_count % 5 == 0:
                    user_input = ''.join(letters[i]['text'] for i in range(letter_count - 5, letter_count))
                    AIfeedback = get_feedback(guess, target)
                    wordleGuesser.feedback_processing(AIfeedback, guess)

                    userfeedback = get_feedback(user_input, target, AIfeedback)
                    wordleGuesser.feedback_processing(userfeedback, user_input)

                    check_word(guess)
                    guess = ''
                    if winner:
                        win_lose(winner)

            if letter_count == 30:
                win_lose(winner)

def check_word(guess):
    global winner
    btn_index = letter_count - 5
    
    for i, letter in enumerate(guess):
        if letter == target[i]:
            letters[btn_index + i]['bg'] = green
            letters[btn_index + i]['activebackground'] = green
        elif letter in target:
            if guess.count(letter) >= 1 and guess.count(letter) == target.count(letter):
                letters[btn_index + i]['bg'] = yellow
                letters[btn_index + i]['activebackground'] = yellow
            else:
                letters[btn_index + i]['bg'] = gray
                letters[btn_index + i]['activebackground'] = gray
        else:
            letters[btn_index + i]['bg'] = gray
            letters[btn_index + i]['activebackground'] = gray
            
    if guess == target:
        winner = True
        win_lose(winner)

def win_lose(winner):
    if not winner:
        title = 'Anda kalah'
        message = f'Jawaban: {target} \n Lihat di KBBI https://kbbi.kemdikbud.go.id/entri/siput'
    else:
        title = 'Gacor kang'
        message = 'Well done, you got it in {} guess(s)'.format(int(letter_count / 5))
    play_again = messagebox.askquestion(title=title, message=f'{message}.\nMain lagi?')

    if play_again == 'yes':
        start_new_game()
    else:
        root.destroy()

def go_again():
    for i in range(5):
        letters[letter_count + i]['text'] = ' '

def layout():
    global frame, letter_count, winner, guess, target
    frame.destroy()
    frame = tk.Frame(root)
    frame.pack()
    letters.clear()
    letter_count = 0
    winner = False
    guess = ''
    target = random.choice(words).upper()

    for row in range(6):
        for col in range(5):
            btn = tk.Button(frame, text=' ', width=1, bg='white',
                            activebackground='white', font=font)
            btn.grid(row=row, column=col, padx=3, pady=5)
            letters.append(btn)

    menu = tk.Menu(root)
    root.config(menu=menu)
    new_game = tk.Menu(menu)
    menu.add_command(label='New Game', command=start_new_game)

# Menghubungkan dengan trie
trie = Trie(words)

root.bind('<Key>', key_pressed)
layout()
root.mainloop()
