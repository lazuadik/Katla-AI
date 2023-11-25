import tkinter as tk
from tkinter import messagebox

class KatlaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Katla Game")

        # Inisialisasi array untuk menyimpan huruf yang dipilih
        self.selected_letters = []

        # Inisialisasi posisi saat ini di dalam kotak input
        self.current_row = 0
        self.current_col = 0

        # Membuat kotak input 5x5
        self.entry_boxes = [[None] * 5 for _ in range(5)]
        for i in range(5):
            for j in range(5):
                entry = tk.Entry(root, width=4, font=('Helvetica', 14), justify='center', state='disabled')
                entry.grid(row=i, column=j, padx=5, pady=5)
                self.entry_boxes[i][j] = entry

        # Membuat keyboard
        keyboard_frame = tk.Frame(root)
        keyboard_frame.grid(row=6, column=0, columnspan=5)
        self.create_keyboard(keyboard_frame)

        # Mengaitkan fungsi `key_pressed` dengan tombol keyboard
        self.root.bind('<Key>', self.key_pressed)

    def create_keyboard(self, frame):
        # Daftar huruf yang mungkin dipilih
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # Susunan keyboard laptop
        laptop_layout = [
            'QWERTYUIOP',
            'ASDFGHJKL',
            'ZXCVBNM'
        ]

        # Membuat tombol keyboard
        row, col = 0, 0
        for row_layout in laptop_layout:
            for letter in row_layout:
                button = tk.Button(frame, text=letter, width=4, height=2, command=lambda l=letter: self.select_letter(l))
                button.grid(row=row, column=col, padx=5, pady=5)
                col += 1
            col = 0
            row += 1

    def key_pressed(self, event):
        # Memeriksa apakah tombol yang ditekan adalah huruf
        if event.char.isalpha():
            letter = event.char.upper()
            self.select_letter(letter)
        elif event.keysym == 'BackSpace':
            self.delete_letter()
        elif event.keysym == 'Return':
            self.finish_input()

    def select_letter(self, letter):
    # Memilih huruf dan menambahkannya ke dalam kotak input
        if len(self.selected_letters) < 5:
            self.selected_letters.append(letter)
            self.update_entry_boxes()
            if len(self.selected_letters) < 5:  # Pindah ke kotak berikutnya jika belum mencapai 5 huruf
                self.move_to_next_box()
            else:
                messagebox.showinfo("Info", "Anda sudah memilih 5 huruf.")


    def delete_letter(self):
        # Menghapus huruf dari kotak input sebelumnya
        if len(self.selected_letters) > 0:
            self.selected_letters.pop()
            self.update_entry_boxes()
            self.move_to_previous_box()

    def move_to_previous_box(self):
        # Pindah ke kotak input sebelumnya
        if self.current_col > 0:
            self.current_col -= 1
        elif self.current_row > 0:
            self.current_row -= 1
            self.current_col = 4
        self.update_entry_boxes()

    def move_to_next_box(self):
        # Pindah ke kotak input berikutnya
        if self.current_col < 4:
            self.current_col += 1
        elif self.current_row < 4:
            self.current_row += 1
            self.current_col = 0

    def finish_input(self):
        # Menyelesaikan input dan membersihkan kotak input
        self.selected_letters = []
        self.current_row = 0
        self.current_col = 0
        self.update_entry_boxes()

    def update_entry_boxes(self):
        # Mengisi kotak input dengan huruf yang dipilih
        for i in range(5):
            for j in range(5):
                self.entry_boxes[i][j].config(state='normal')
                self.entry_boxes[i][j].delete(0, 'end')
                if j < len(self.selected_letters) and i == self.current_row:
                    self.entry_boxes[i][j].insert(0, self.selected_letters[j])
                self.entry_boxes[i][j].config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    game = KatlaGame(root)
    root.mainloop()
