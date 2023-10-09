import os
import wget
import random
import shutil
import platform
import fileinput
import tkinter as tk
from PIL import Image, ImageTk
from functools import partial
from pathlib import Path

def missing_font(font):
    window = tk.Tk()
    window.title("Missing font")
    frame = tk.Frame(window, bd=10)
    frame.pack()

    text = "It seems like a font is missing from your fonts directory.\n\nMissing font: %s\nDo you want to install it now?\n\nNote: you can play the game without installing the font, but you will lose out on the classic Minesweeper experience!" % font
    message = tk.Message(frame, text=text)
    message.pack()

    buttons = tk.Frame(frame)
    buttons.pack()

    tk.Button(buttons, text="Yes", command=lambda: install_font(window)).grid(row=0, column=0)
    tk.Button(buttons, text="No", command=window.destroy).grid(row=0, column=1)

    window.mainloop()

installed = False

def install_font(window):
    global installed
    installed = True
    shutil.copyfile(src, dst)
    window.destroy()

files = ("minesweeper.png", "smiley_happy.png", "smiley_shock.png", "smiley_cool.png", "smiley_dead.png", "config.txt", "topscores.txt", "DSEG7Classic-Bold.ttf", "mine-sweeper.ttf")
variables = ("icon", "happy", "shock", "cool", "dead", "config", "scoreboard")

for file in files:

    filepath = str(Path(__file__).parent)+"/data/%s" % file

    if not os.path.isfile(filepath):
        wget.download("https://github.com/xhoneybear/minesweeper/blob/main/data/%s" % file, filepath)

    if ".ttf" in file:
        src = str(Path(__file__).parent)+"/data/%s" % file
        if platform.system() == "Windows":
            homedir = os.getenv("USERPROFILE")
            fontdir = "AppData\\Local\\Microsoft\\Windows\\Fonts"
        elif platform.system() == "Darwin":
            homedir = os.path.expanduser("~")
            fontdir = "Library/Fonts"
        elif platform.system() == "Linux":
            homedir = os.path.expanduser("~")
            fontdir = ".fonts"

        dst = os.path.join(homedir, fontdir, file)
        if os.path.isfile(dst) == False:
            missing_font(file)

if installed == True:
    window = tk.Tk()
    window.title("Missing font")
    frame = tk.Frame(window, bd=10)
    frame.pack()

    text = "Font(s) installed. Please run the game again."
    message = tk.Message(frame, text=text)
    message.pack()

    tk.Button(frame, text="OK", command=quit).pack()

    window.mainloop()

for i in range(len(variables)):
    globals()[variables[i]] = str(Path(__file__).parent)+"/data/%s" % files[i]

def start():

    global mainframe, timer, smiley, smileyface, flagcount, flags, gameinprogress, firstmove

    pixel = tk.PhotoImage(width=1, height=1)
    flagcount = bombs
    gameinprogress = 0

    try:
        mainframe.destroy()
    except:
        pass
    mainframe = tk.Frame(window, bd=10)
    mainframe.pack(fill="both", expand="yes")

    topframe = tk.Frame(mainframe, bd=3, relief="sunken")
    topframe.pack()

    # Fill the top bar with spacers - assure symmetry
    for i in range(0,width):
        tk.Button(topframe, bd=0, highlightthickness=0, relief="flat", image=pixel, width=24, state="disabled").grid(row=0, column=i)

    smileyface = ImageTk.PhotoImage(Image.open(happy).resize((28,28)))

    flags = tk.Label(topframe, text=str(flagcount).zfill(3), bd=2, relief="sunken", bg="#000000", fg="#FF0000", font=("DSEG7 Classic", 20))
    flags.grid(row=0, column=0, columnspan=3)

    smiley = tk.Button(topframe, bd=4, width=28, height=28, image=smileyface, command=start)
    smiley.grid(row=0, column=0, columnspan=width)
    smileyhover(smiley)

    timer = tk.Label(topframe, text="000", bd=2, relief="sunken", bg="#000000", fg="#FF0000", font=("DSEG7 Classic", 20))
    timer.grid(row=0, column=width-3, columnspan=3)

    middlebar = tk.Frame(mainframe, height=10)
    middlebar.pack()

    firstmove = 1

    makeboard()

def makeboard():

    global boardframe, pixel, board, coverstate, marks

    pixel = ImageTk.PhotoImage(Image.open(icon).resize((1,1)))

    try:
        boardframe.destroy()
    except:
        pass
    boardframe = tk.Frame(mainframe, bd=3, relief="sunken")
    boardframe.pack()

    fields = []

    for i in range(0,width*height-bombs):
        fields.append("O")

    for i in range(0,bombs):
        fields.append("*")
            
    random.shuffle(fields)

    board = []
    coverstate = []

    a=0

    for y in range(0,height):
        row = []
        cover = []
        for x in range(0,width):
            row.append(fields[a])
            cover.append(1)
            dynvar = "x%dy%d" % (x,y)
            globals()[dynvar] = tk.Button(boardframe, bd=3, highlightthickness=0, image=pixel, width=18, height=18, padx=0, pady=0, compound="c", font=("Mine-sweeper", 10), command=partial(reveal, x, y))
            obj = globals()[dynvar]
            obj.grid(row=y, column=x)
            obj.bind("<Button-3>", partial(flag_toggle, x, y, marks))
            a += 1
        board.append(row)
        coverstate.append(cover)
    
    for y in range(0,height):
        for x in range(0,width):
            if board[y][x] == "O":

                b = 0

                for i in range(y-1,y+2):
                    for j in range(x-1,x+2):
                        if 0 <= i < height and 0 <= j < width:
                            b += isbombnearby(i,j)

                board[y][x] = b

                dynvar = "x%dy%d" % (x,y)
                obj = globals()[dynvar]

                text_color(x,y,obj)

def text_color(x,y,obj):

    if board[y][x] == 0:
        board[y][x] = ""

    if board[y][x] == 1:
        obj.config(fg="#0000FF")

    if board[y][x] == 2:
        obj.config(fg="#008000")

    if board[y][x] == 3:
        obj.config(fg="#FF0000")

    if board[y][x] == 4:
        obj.config(fg="#000080")

    if board[y][x] == 5:
        obj.config(fg="#800000")

    if board[y][x] == 6:
        obj.config(fg="#008080")

    if board[y][x] == 7:
        obj.config(fg="#000000")
        
    if board[y][x] == 8:
        obj.config(fg="#808080")
        
def isbombnearby(y,x):
    b = 0
    try:
        if board[y][x] == "*":
            b = 1
    except IndexError:
        pass
    return b

def whitefill(x,y):
    dynvar = "x%dy%d" % (x,y)
    queue.add(dynvar)
    for a in range(y-1,y+2):
        for b in range(x-1,x+2):
            if 0 <= a < height and 0 <= b < width and coverstate[a][b] == 1:
                coverstate[a][b] = 0
                dynvar = "x%dy%d" % (b,a)
                obj = globals()[dynvar]
                obj.config(text=board[a][b], relief="sunken", bd=0, highlightthickness=0, image=pixel, width=24, height=24)
                obj.unbind("<Button-3>")
                if dynvar not in queue and board[a][b] == "":
                    whitefill(b,a)

def reveal(x,y):
    
    global queue, firstmove, time, gameinprogress

    if firstmove == 1:
        while board[y][x] == "*":
            makeboard()
        gameinprogress = 1
        time = 0
        timerfunc()
        firstmove -= 1

    if coverstate[y][x] == 1:
        coverstate[y][x] = 0
        dynvar = "x%dy%d" % (x,y)
        obj = globals()[dynvar]
        obj.config(text=board[y][x], relief="sunken", bd=0, highlightthickness=0, image=pixel, width=24, height=24)
        obj.unbind("<Button-3>")

    if board[y][x] == "":
        queue = set(())
        whitefill(x,y)
    elif board[y][x] == "*":
        gameover()
    
    checkwin()

def timerfunc():

    global time
    if gameinprogress == 1 and time < 999:
        time += 1
        timer.config(text=str(time).zfill(3))
        window.after(1000, timerfunc)
    
def checkwin():

    global smileycool, gameinprogress

    winflags = 0
    winfields = 0
    
    for y in range(0,height):
        for x in range(0, width):
            if coverstate[y][x] == 0 and board[y][x] != "*":
                winfields += 1
            # if coverstate[y][x] == 2 and board[y][x] == "*":
                # winflags += 1

    # if winflags == bombs or winfields == height*width-bombs:
    if winfields == height*width-bombs:

        smileycool = ImageTk.PhotoImage(Image.open(cool).resize((28,28)))
        smiley.config(image=smileycool)

        gameinprogress = 0
        
        for y in range(0,height):
            for x in range(0,width):
                if coverstate[y][x] == 1:
                    dynvar = "x%dy%d" % (x,y)
                    obj = globals()[dynvar]
                    obj.config(command="")
                    obj.unbind("<Button-3>")
                    if board[y][x] == "*":
                        obj.config(text="`", command="")
                    else:
                        obj.config(text=board[y][x], command="")

        if width == height:
            with open(scoreboard, "r") as f:
                line = f.readlines()

            if width == 8 and bombs == 10:
                if int(line[0]) > time:
                    line[0] = "%d\n" % time
            elif width == 16 and bombs == 40:
                if int(line[1]) > time:
                    line[1] = "%d\n" % time
            elif width == 24 and bombs == 100:
                if int(line[2]) > time:
                    line[2] = "%d" % time
            
            with open(scoreboard, "w") as f:
                f.writelines(line)

marks = False

def toggle_marks():

    global marks

    if marks == False:
        marks = True
    else:
        marks = False
    
    start()

def flag_toggle(x, y, marks, event):

    global flagcount

    dynvar = "x%dy%d" % (x,y)
    obj = globals()[dynvar]

    if coverstate[y][x] == 1 and flagcount > 0:
        coverstate[y][x] = 2
        obj.config(fg="#000000", text="`", command="")
        flagcount -= 1
    
    else:
        if marks == False or coverstate[y][x] == 3:
            coverstate[y][x] = 1
            text_color(x,y,obj)
            obj.config(text="", command=partial(reveal, x, y))
            flagcount += 1
        else:
            coverstate[y][x] = 3
            obj.config(text="?")

    flags.config(text=str(flagcount).zfill(3))

    # checkwin()

def gameover():

    global smileydead, gameinprogress

    gameinprogress = 0

    smiley.unbind("<Enter>")
    smiley.unbind("<Leave>")
    smileydead = ImageTk.PhotoImage(Image.open(dead).resize((28,28)))
    smiley.config(image=smileydead)
    
    for y in range(0,height):
        for x in range(0,width):
            dynvar = "x%dy%d" % (x,y)
            obj = globals()[dynvar]
            obj.config(command="")
            obj.unbind("<Button-3>")
            if coverstate[y][x] != 2:
                obj.config(text=board[y][x])
            elif coverstate[y][x] == 2 and board[y][x] != "*":
                obj.config(text="x")

def smileyhover(button):

    global smileyhappy, smileyshock
    smileyhappy = ImageTk.PhotoImage(Image.open(happy).resize((28,28)))
    smileyshock = ImageTk.PhotoImage(Image.open(shock).resize((28,28)))

    button.bind("<Enter>", func=lambda e: button.config(image=smileyshock))
    button.bind("<Leave>", func=lambda e: button.config(image=smileyhappy))

def size(*args):
    
    global width, height, bombs

    def update():

        global width, height, bombs

        width=var_width.get()
        height=var_height.get()
        bombs=var_bombs.get()

        limit = int(0.8*int(var_width.get())*int(var_height.get()))
        bombs_spin.config(to=limit)

    def ok():
        custom.quit()
        custom.destroy()

    if len(args) < 3:

        custom = tk.Toplevel()
        custom.title("Custom settings")

        frame = tk.LabelFrame(custom, text="Customize your board")
        frame.pack(fill="both", expand="yes")

        var_width = tk.IntVar()
        var_height = tk.IntVar()
        var_bombs = tk.IntVar()

        limit = 3

        tk.Label(frame, text="Width:").grid(column=1, row=1, sticky="W")
        width_spin = tk.Spinbox(frame, width=4, from_=5, to=100, textvariable=var_width, command=lambda: update()).grid(column=2, row=1)

        tk.Label(frame, text="Height:").grid(column=1, row=2, sticky="W")
        height_spin = tk.Spinbox(frame, width=4, from_=5, to=100, textvariable=var_height, command=lambda: update()).grid(column=2, row=2)

        tk.Label(frame, text="Bombs:").grid(column=1, row=3, sticky="W")
        bombs_spin = tk.Spinbox(frame, width=4, from_=1, to=limit, textvariable=var_bombs, command=lambda: update())
        bombs_spin.grid(column=2, row=3)

        tk.Button(frame, text="OK", command=lambda: ok()).grid(row=height, column=2)
        tk.Button(frame, text="Cancel", command=lambda: custom.destroy()).grid(row=height, column=3)

        custom.mainloop()

    else:
        width = args[0]
        height = args[1]
        bombs = args[2]

    start()

def tutorial():

    top = tk.Toplevel()
    top.title("How to play")

    global logo
    logo = ImageTk.PhotoImage(Image.open(icon).resize((128,128)))
    image = tk.Label(top, image=logo)
    image.pack()

    frame = tk.LabelFrame(top, text="How to play minesweeper?", labelanchor="n")
    frame.pack(fill="both", expand="yes")

    text = "Minesweeper is a logic game where the goal is to clear a board without hitting a mine. In minesweeper you uncover fields trying to avoid mines and place flags to mark fields with mines.\n\nControls:\nLeft click uncovers a field.\nRight click places a flag.\n\nGame ends when you hit a mine, successfully flag all bombs or uncover all fields without hitting a mine.\n\nGood luck!"
    message = tk.Message(frame, text=text)
    message.pack()

    top.mainloop()

def about():
    
    top = tk.Toplevel()
    top.title("About Minesweeper")

    global logo
    logo = ImageTk.PhotoImage(Image.open(icon).resize((128,128)))
    image = tk.Label(top, image=logo)
    image.pack()

    frame = tk.LabelFrame(top, text="Minesweeper", labelanchor="n")
    frame.pack(fill="both", expand="yes")

    text = "A logic puzzle video game. The game features a grid of clickable squares with hidden \"mines\" scattered throughout the board. The objective is to clear the board without detonating any mines, with help from clues about the number of neighboring mines in each field.\n\nThe first version of the game was 1990's Microsoft Minesweeper developed by Curt Johnson and distributed with Microsoft Windows operating system family."
    message = tk.Message(frame, text=text)
    message.pack()

    top.mainloop()

def topscores():

    def reset():
        with open(scoreboard, "w") as f:
            f.writelines("999\n999\n999")
        scoreframe.destroy()
        scores()
    
    def scores():
        global scoreframe
        scoreframe = tk.Frame(frame)
        scoreframe.grid(row=0, column=1)

        with open(scoreboard, "r") as f:
            scores = f.read()

        scorelist = tk.Message(scoreframe, text=scores, justify="right")
        scorelist.pack()
    
    top = tk.Toplevel()
    top.title("Best scores")

    frame = tk.LabelFrame(top, highlightthickness=10, relief="flat", text="Top times", labelanchor="n")
    frame.grid(columnspan=4)

    difficulty = tk.Frame(frame)
    difficulty.grid(row=0, column=0)

    difficulties = tk.Message(difficulty, text="Beginner:\nIntermediate:\nExpert:")
    difficulties.pack()

    scores()

    ok = tk.Button(top, text="OK", width=5, command=top.destroy)
    ok.grid(row=1, column=1)

    reset = tk.Button(top, text="Reset", width=5, command=reset)
    reset.grid(row=1, column=2)

    top.mainloop()

window = tk.Tk()
window.title("Minesweeper")
window.iconphoto(True,  ImageTk.PhotoImage(Image.open(icon)))

menu = tk.Menu(window)
window.configure(menu=menu)

game = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Game", menu=game)

game.add_command(label="New", command=start)

game.add_separator()

game.add_radiobutton(label="Beginner", command=lambda: size(8,8,10))
game.add_radiobutton(label="Intermediate", command=lambda: size(16,16,40))
game.add_radiobutton(label="Expert", command=lambda: size(24,24,100))
game.add_radiobutton(label="Custom", command=lambda: size())

game.add_separator()

game.add_checkbutton(label="Marks (?)", command=lambda: toggle_marks())
game.add_checkbutton(label="Colors", command=lambda: size(16,16,40))
game.add_checkbutton(label="Sound", state="disabled")

game.add_separator()

game.add_command(label="Best scores", command=topscores)

game.add_separator()

game.add_command(label="Exit", command=quit)

helpmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=helpmenu)

helpmenu.add_command(label="How to play?", command=tutorial)
helpmenu.add_command(label="About...", command=about)

size(8,8,10)

window.mainloop()