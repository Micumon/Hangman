from tkinter import *
from tkinter import ttk
from tkinter import font
from random import randrange
from tkinter import messagebox
from file_new import create_file


def keyboard(letter):
    global guess_letter_labels
    global word
    global loose_cond
    global win_cond
    global buttons

    if letter in word and letter not in guessed:
        for i in range(len(word)):
            if word[i] == letter:
                guess_letter_labels[i].configure(text=letter)
                win_cond -= 1
                guessed.add(letter)
    else:
        draw_gallows(loose_cond)
        loose_cond -= 1
    for button in buttons:
        if button["text"] == letter:
            button.configure(style="used.TButton")

    if win_cond == 0:
        buttons_state(False)
        win()
    if loose_cond == 0:
        buttons_state(False)
        loose()


def win():
    decision = messagebox.askyesno(title="Zwycięstwo!", message="Wygrana! Chcesz zagrać jeszcze raz?", icon="info")
    if decision:
        new_game()
    else:
        exit()


def loose():
    global word
    global guess_letter_labels
    for i in range(len(word)):
        guess_letter_labels[i].configure(text=word[i])
    decision = messagebox.askyesno(title="Przegrana!", message="Przegrana! Chcesz zagrać jeszcze raz?", icon="error")
    if decision:
        new_game()
    else:
        exit()


def draw_gallows(count):
    gallows = {10: lambda: playground.create_line(200, 350, 400, 350, fill="brown", width=10, capstyle="round",
                                                  tags="A"),
               9: lambda: playground.create_line(300, 350, 300, 50, fill="brown", width=10, capstyle="round",
                                                 tags="A"),
               8: lambda: playground.create_line(300, 50, 450, 50, fill="brown", width=10, capstyle="round", tags="A"),
               7: lambda: playground.create_line(450, 50, 450, 100, fill="coral2", width=10, capstyle="round",
                                                 tags="A"),
               6: [lambda: playground.create_oval(425, 100, 475, 150, fill='yellow', outline='red', tags="A"),
                   lambda: playground.create_line(440, 150, 460, 150, fill="coral2", width=8, capstyle="round",
                                                  tags="A"),
                   lambda: playground.create_text(450, 120, text='X  X', justify="center", fill='black', tags="A")],
               5: [lambda: playground.create_line(450, 150, 450, 165, fill="yellow", width=8, capstyle="round",
                                                  tags="A"),
                   lambda: playground.create_line(450, 165, 450, 240, fill="blue", width=8, capstyle="round", tags="A"),
                   lambda: playground.create_line(440, 150, 460, 150, fill="coral2", width=8, capstyle="round",
                                                  tags="A")],
               4: [lambda: playground.create_line(450, 165, 470, 200, fill="blue", width=8, capstyle="round", tags="A"),
                   lambda: playground.create_line(470, 200, 480, 214, fill="yellow", width=8, capstyle="round",
                                                  tags="A")],
               3: [lambda: playground.create_line(450, 165, 430, 200, fill="blue", width=8, capstyle="round", tags="A"),
                   lambda: playground.create_line(430, 200, 420, 214, fill="yellow", width=8, capstyle="round",
                                                  tags="A")],
               2: [lambda: playground.create_line(450, 240, 470, 275, fill="dark grey", width=8, capstyle="round",
                                                  tags="A"),
                   lambda: playground.create_line(470, 275, 480, 275, fill="dark green", width=8, capstyle="round",
                                                  tags="A")],
               1: [lambda: playground.create_line(450, 240, 430, 275, fill="dark grey", width=8, capstyle="round",
                                                  tags="A"),
                   lambda: playground.create_line(430, 275, 420, 275, fill="dark green", width=8, capstyle="round",
                                                  tags="A")]}
    if type(gallows[count]) is list:
        for func in gallows[count]:
            func()
    else:
        gallows[count]()


def letter_button(letter, column, row):
    name = ttk.Button(frame, text=letter, command=lambda: keyboard(letter), width=5, state="disabled")
    name.grid(column=column, row=row)
    return name


def letter_labels(column):
    name = ttk.Label(frame, text="   ", font=underline_font)
    name.grid(row=2, column=column, sticky=(W, E))
    return name


def buttons_state(flag):
    global buttons
    if flag:
        for button in buttons:
            button.configure(state="!disabled")
    else:
        for button in buttons:
            button.configure(state="disabled")
    for button in buttons:
        button.configure(style="TButton")


def new_game():
    global guess_letter_labels
    global letters
    global word
    global win_cond
    global loose_cond
    global guessed

    try:
        with open("Easy.txt", "r", encoding="utf-8") as f:
            word_list_unformat = f.readlines()
    except FileNotFoundError:
        create_file()
        with open("Easy.txt", "r", encoding="utf-8") as f:
            word_list_unformat = f.readlines()
    buttons_state(True)
    for i in range(len(guess_letter_labels)):
        guess_letter_labels[i].destroy()
    guess_letter_labels.clear()
    win_cond = 0
    loose_cond = 10
    guessed.clear()
    playground.delete("A")

    category_list = []
    word_list = []
    for line in word_list_unformat:
        line = line.upper()
        line = line.rstrip()
        line = line.split(":")
        word_list.append(line[0])
        category_list.append(line[1])
    rand_index = randrange(len(word_list))
    word = word_list[rand_index]
    category = "KATEGORIA: "+str(category_list[rand_index])
    playground.create_text(325, 390, text=category, justify="center", fill='black', tags="A")
    win_cond = len(word)
    column_offset = int((len(letters)/4)-(len(word)/2))
    for i in range(len(word)):
        guess_letter_labels.append(letter_labels(i+column_offset))


root = Tk()
root.title("Wisielec")
x_start = int(root.winfo_screenwidth()/2)-int(674/2)
y_start = int(root.winfo_screenheight()/2)-int(535/2)
pos_start = "+"+str(x_start)+"+"+str(y_start)
root.geometry(pos_start)
root.resizable(FALSE, FALSE)
styles = ttk.Style()
styles.configure("used.TButton", background="red")

underline_font = font.Font(family='Segoe UI', name='under_font', size=15, underline=True, weight="normal")
guess_letter_labels = []
word = ""
win_cond = 0
loose_cond = 10
guessed = {"0"}



frame = ttk.Frame(root, padding=5)
frame.grid(row=1, column=0, sticky=(W, S, E, N))


playground = Canvas(frame, background="azure", relief="sunken", borderwidth=5, height=400, width=650)
playground.grid(row=1, column=0, columnspan=16, sticky=(W, S, E, N))

separator_line1 = ttk.Separator(frame, orient="horizontal")
separator_line1.grid(row=3, column=0, columnspan=16, sticky=(W, S, E, N))


letters = ("A", "Ą", "B", "C", "Ć", "D", "E", "Ę", "F", "G", "H", "I", "J", "K", "L", "Ł", "M", "N", "Ń", "O", "Ó", "P",
           "R", "S", "Ś", "T", "U", "W", "Y", "Z", "Ź", "Ż")
buttons = []
for i in range(len(letters)):
    row = 4
    if i >= len(letters)/2:
        row = 5
        buttons.append(letter_button(letters[i], i-16, row))
    else:
        buttons.append(letter_button(letters[i], i, row))

separator_line1 = ttk.Separator(frame, orient="horizontal")
separator_line1.grid(row=6, column=0, columnspan=16, sticky=(W, S, E, N))

new_game_button = ttk.Button(frame, text="Nowa gra", command=new_game)
new_game_button.grid(row=7, column=4, columnspan=3, sticky=W)

close_button = ttk.Button(frame, text="Zamknij", command=exit)
close_button.grid(row=7, column=9, columnspan=3, sticky=E)


root.mainloop()
