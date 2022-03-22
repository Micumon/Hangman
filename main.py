from tkinter import *
from tkinter import ttk
from tkinter import font
from random import randrange


def keyboard(letter):
    global guess_letter_labels
    global word
    global loose_cond
    global win_cond
    if letter in word and letter not in guessed:
        for i in range(len(word)):
            if word[i] == letter:
                guess_letter_labels[i].configure(text=letter)
                win_cond -= 1
                guessed.add(letter)
    else:
        draw_gallows(loose_cond)
        loose_cond -= 1
        print("Pudlo")
    if win_cond == 0:
        win()
    if loose_cond == 0:
        loose()


def win():
    win_screen = Toplevel(root)
    root_position = root.geometry()
    root_position = root_position.replace("x", "+")
    root_position = root_position.split("+")
    win_screen_position = ["150x", "150+", str(int(root_position[2])+int(int(root_position[0])/2)-75)+"+",
                           int(int(root_position[3])+int(root_position[1])/2-75)]
    win_screen_position_geo = ""
    for element in win_screen_position:
        win_screen_position_geo = win_screen_position_geo+str(element)
    print(win_screen_position_geo)
    win_screen.geometry(win_screen_position_geo)
    win_label = ttk.Label(win_screen, text="Zwycięstwo!", justify="center")
    win_label.grid(row=1, column=1, columnspan=2, sticky=(N, W, E, S))
    new_game_button_w = ttk.Button(win_screen, text="Nowa gra")
    new_game_button_w.grid(row=2, column=1, sticky=S)
    new_game_button_w.bind("<Button-1>", lambda e: new_game())
    new_game_button_w.bind("<ButtonRelease>", lambda e: win_screen.destroy())
    close_button_w = ttk.Button(win_screen, text="Zamknij", command=exit)
    close_button_w.grid(row=2, column=2, sticky=S)


def loose():
    print("przegrana")


def draw_gallows(count):
    gallows = {10: lambda: playground.create_line(200, 350, 400, 350, fill="brown", width=10, capstyle="round", tags="A"),
               9: lambda: playground.create_line(300, 350, 300, 50, fill="brown", width=10, capstyle="round", tags="A"),
               8: lambda: playground.create_line(300, 50, 450, 50, fill="brown", width=10, capstyle="round", tags="A"),
               7: lambda: playground.create_line(450, 50, 450, 100, fill="coral2", width=10, capstyle="round", tags="A"),
               6: [lambda: playground.create_oval(425, 100, 475, 150, fill='yellow', outline='red', tags="A"),
                   lambda: playground.create_line(440, 150, 460, 150, fill="coral2", width=8, capstyle="round", tags="A"),
                   lambda: playground.create_text(450, 120, text='X  X', justify="center", fill='black', tags="A")],
               5: [lambda: playground.create_line(450, 150, 450, 165, fill="yellow", width=8, capstyle="round", tags="A"),
                   lambda: playground.create_line(450, 165, 450, 240, fill="blue", width=8, capstyle="round", tags="A"),
                   lambda: playground.create_line(440, 150, 460, 150, fill="coral2", width=8, capstyle="round", tags="A")],
               4: [lambda: playground.create_line(450, 165, 470, 200, fill="blue", width=8, capstyle="round", tags="A"),
                   lambda: playground.create_line(470, 200, 480, 214, fill="yellow", width=8, capstyle="round", tags="A")],
               3: [lambda: playground.create_line(450, 165, 430, 200, fill="blue", width=8, capstyle="round", tags="A"),
                   lambda: playground.create_line(430, 200, 420, 214, fill="yellow", width=8, capstyle="round", tags="A")],
               2: [lambda: playground.create_line(450, 240, 470, 275, fill="dark grey", width=8, capstyle="round", tags="A"),
                   lambda: playground.create_line(470, 275, 480, 275, fill="dark green", width=8, capstyle="round", tags="A")],
               1: [lambda: playground.create_line(450, 240, 430, 275, fill="dark grey", width=8, capstyle="round", tags="A"),
                   lambda: playground.create_line(430, 275, 420, 275, fill="dark green", width=8, capstyle="round", tags="A")]}
    if type(gallows[count]) is list:
        for func in gallows[count]:
            func()
    else:
        gallows[count]()

def letter_button(letter, column, row):
    name = ttk.Button(frame, text=letter, command=lambda: keyboard(letter), width=5)
    name.grid(column=column, row=row)
    return name


def letter_labels(column):
    name = ttk.Label(frame, text="   ", font=underline_font)
    name.grid(row=2, column=column, sticky=(W,E))
    return name


def new_game():
    global word_varibles
    global guess_letter_labels
    global letters
    global word
    global win_cond
    global loose_cond
    global guessed


    for i in range(len(guess_letter_labels)):
        guess_letter_labels[i].destroy()
    guess_letter_labels.clear()
    word_varibles.clear()
    win_cond = 0
    loose_cond = 10
    guessed.clear()
    playground.delete("A")

    with open("Easy.txt", "r", encoding="utf-8") as f:
        word_list_unformat = f.readlines()
    word_list = []
    for line in word_list_unformat:
        line = line.upper()
        word_list.append(line.rstrip())
    word = word_list[randrange(len(word_list))]
    win_cond = len(word)
    for letter in word:
        word_varibles[letter] = 0
    column_offset = int((len(letters)/4)-(len(word)/2))
    for i in range(len(word)):
        guess_letter_labels.append(letter_labels(i+column_offset))


root = Tk()
root.title("Wisielec")

underline_font = font.Font(family='Segoe UI', name='under_font', size=15, underline=True, weight="normal")
word_varibles = {}
guess_letter_labels = []
word = ""
win_cond = 0
loose_cond = 10
guessed = {"0"}


frame = ttk.Frame(root, padding=5)
frame.grid(row=1, column=0, sticky=(W,S,E,N))


playground = Canvas(frame, background="azure", relief="sunken", borderwidth=5, height=400, width=650)
playground.grid(row=1, column=0, columnspan=16, sticky=(W,S,E,N))

separator_line1 = ttk.Separator(frame, orient="horizontal")
separator_line1.grid(row=3, column=0, columnspan=16, sticky=(W,S,E,N))


letters = ("A","Ą","B","C","Ć","D","E","Ę","F","G","H","I","J","K","L","Ł","M","N","Ń","O","Ó","P","R","S","Ś","T","U",
           "W","Y","Z","Ź","Ż")
buttons = []
for i in range(len(letters)):
    row = 4
    if i >= len(letters)/2:
        row = 5
        buttons.append(letter_button(letters[i], i-16, row))
    else:
        buttons.append(letter_button(letters[i], i, row))

separator_line1 = ttk.Separator(frame, orient="horizontal")
separator_line1.grid(row=6, column=0, columnspan=16, sticky=(W,S,E,N))

new_game_button = ttk.Button(frame, text="Nowa gra", command=new_game)
new_game_button.grid(row=7, column=4, columnspan=3, sticky=W)

close_button = ttk.Button(frame, text="Zamknij", command=exit)
close_button.grid(row=7, column=9, columnspan=3, sticky=E)



root.mainloop()