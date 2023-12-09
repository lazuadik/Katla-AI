import random
import tkinter as tk
from tkinter import messagebox
from trie import Trie
from solver import WordleGuesser, get_feedback
# from 

# Variabel GUI
green = '#27e512'
yellow = '#e8ef0e'
gray = '#4c4c4c'
font = 'Verdana, 13'
answer = []
words = []
column = 0
row = 0
step = 0
target = ''
wordleGuesser = None

with open('wordle-dictionary.txt', 'r') as file:
    data = file.readlines()
    for i in data:
        words.append(i[:-1].upper())

def start_new_game():
    global wordleGuesser, target, step, row, column, step, answer
    step = 0
    wordleGuesser = WordleGuesser(Trie(words))
    target = random.choice(words)
    column = 0
    row = 0
    answer = []
    layout()

def key_pressed(event):
    global column, row, answer, step
    if row < 8:
        if event.char.isalpha():
            entry = entry_list_1[row][column if column <= 4 else 4]
            entry.configure(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.insert(0, event.char.upper())
            entry.configure(state="readonly")
            if column <= 4:
                column += 1
                answer.append(event.char.upper())
            else:
                answer.pop()
                answer.append(event.char.upper())
        elif event.keysym == 'Return':
            guess = ''.join(answer)
            if column != 5:
                messagebox.showwarning("Peringatan", "Mohon masukkan input terlebih dahulu.")
            elif guess not in words:
                messagebox.showwarning("Peringatan", "Input tidak ada di KBBI")
            else:
                row += 1
                column = 0
                answer = []
                step += 1
                check_word(guess)
        elif event.keysym in ['Delete', 'BackSpace']:
            entry = entry_list_1[row][column-1]
            entry.configure(state=tk.NORMAL)  # Mengubah keadaan menjadi NORMAL sementara
            entry.delete(0, tk.END)
            entry.configure(state="readonly")
            if column > 0:
                column -= 1
                answer.pop()

def check_word(guess):
    assignment = wordleGuesser.backtrack({}, wordleGuesser.csp.trie.root)
    guessed_word = ''.join(assignment)

    AIfeedback = get_feedback(guessed_word, target)
    wordleGuesser.feedback_processing(AIfeedback, guessed_word)

    userfeedback = get_feedback(guess, target, AIfeedback)
    wordleGuesser.feedback_processing(userfeedback, guess)

    update_matrix(AIfeedback, guessed_word, userfeedback)
    win_lose(guess, guessed_word)

def create_matrix(root, rows, columns):
    matrix = []
    for i in range(rows):
        row_frame = tk.Frame(root)
        row_entries = []
        for j in range(columns):
            entry = tk.Entry(row_frame, width=2, font=font, justify='center', state="readonly", readonlybackground='white', background='white')
            entry.pack(side='left', ipadx=10, ipady=10)
            row_entries.append(entry)
        row_frame.pack()
        matrix.append(row_entries)
    return matrix

def win_lose(user_input, guessed_word):
    global matrix_frame_left, matrix_frame_right, entry_list_2, entry_list_1
    isGameOver = False
    if guessed_word == target and user_input == target:
        title = 'Seri!'
        message = f'Jawaban: {target} \n Lihat di KBBI https://kbbi.kemdikbud.go.id/entri/{target}'
        isGameOver = True
    elif guessed_word == target:
        title = 'Anda kalah'
        message = f'Jawaban: {target} \n Lihat di KBBI https://kbbi.kemdikbud.go.id/entri/{target}'
        isGameOver = True
    elif user_input == target:
        title = 'Gacor kang'
        message = 'Well done, you got it in {} guess(s)'.format(step)
        isGameOver = True
    elif row == 8:
        title = 'Seri!'
        message = f'Jawaban: {target} \n Lihat di KBBI https://kbbi.kemdikbud.go.id/entri/{target}'
        isGameOver = True
    if isGameOver:
        play_again = messagebox.askquestion(title=title, message=f'{message}.\nMain lagi?')
        if play_again == 'yes':
            start_new_game()
        else:
            root.destroy()

def update_matrix(AI, guessed_word, user):
    global entry_list_1, entry_list_2
    for entry, char, colour in zip(entry_list_2[row-1], guessed_word, AI):
        entry.configure(state=tk.NORMAL)
        entry.delete(0, tk.END)
        entry.insert(0, char)
        if colour == 0:
            entry.configure(readonlybackground=gray)
        elif colour == 1:
            entry.configure(readonlybackground=yellow)
        else:
            entry.configure(readonlybackground=green)
        entry.configure(state="readonly")
    for entry, colour in zip(entry_list_1[row-1], user):
        entry.configure(state=tk.NORMAL)
        if colour == 0:
            entry.configure(readonlybackground=gray)
        elif colour == 1:
            entry.configure(readonlybackground=yellow)
        else:
            entry.configure(readonlybackground=green)
        entry.configure(state="readonly")

def layout():
    global entry_list_1, entry_list_2
    for entry_row in entry_list_1:
        for entry in entry_row:
            entry.configure(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.configure(readonlybackground='white')
            entry.configure(state="readonly")
    for entry_row in entry_list_2:
        for entry in entry_row:
            entry.configure(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.configure(readonlybackground='white')
            entry.configure(state="readonly")
    

root = tk.Tk()
root.title("Wordle")
root.geometry("655x550")
root.configure(background='pink')
root.resizable(width=False, height=False)
# root.maxsize(width=655, height=550)
# root.minsize(width=655, height=550)
matrix_frame_right = tk.Frame(root)
matrix_frame_left = tk.Frame(root)
entry_list_1 = create_matrix(matrix_frame_right, 8, 5)
entry_list_2 = create_matrix(matrix_frame_left, 8, 5)
matrix_frame_right.pack(side='right')
matrix_frame_left.pack(side='left')
start_new_game()
root.bind("<Key>", key_pressed)

root.mainloop()
