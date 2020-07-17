import csv
import random as R
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Main directory - CSV file with categories and elements for the games
FILE_PATH = "C:\\Users\\HAL-9000\\OneDrive\\Programming\\Python\\Learning\\MultipleJoy\\"
FILE_NAME = "game_categories.csv"


# ------------------------------ Gets opposite color - Used on StartPage
def opposite_color(hex):
    if hex[0] == "#":
        hex = hex[1:]
    
    rgb = (hex[0:2], hex[2:4], hex[4:6])

    opposite = ["%02X" % (255 - int(a, 16)) for a in rgb]

    return "#" + "".join(opposite)


# ------------------------------ Game categories
def set_categories():
    file = FILE_PATH + FILE_NAME
    
    firstline = "Category,Name"

    dic = {}

    for line in open(file).readlines():
        if not firstline in line:
            line = line.strip()
            line = line.split(",")

            key = line[0]

            for value in line[1:]:
                dic.setdefault(key, []).append(value)

    return dic


# ------------------------------ MAIN WINDOW
class MultipleJoy(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

    # FRAME - Container
        container = tk.Frame(self)
        container.pack(side="top", fill=tk.BOTH, expand=True)
        container.columnconfigure(0, weight=1)

    # COMBOBOX - Categories
        self.cmb_var = tk.StringVar()

        self.cmb_categories = ttk.Combobox(container,
                                           values=[(key.upper()) for key in set_categories().keys()],
                                           textvariable=self.cmb_var,
                                           height=20,
                                           width=26,
                                           state="readonly",
                                           justify=tk.CENTER,
                                           font=("Verdana", 12),
                                           )
        self.cmb_categories.current(None)
        self.cmb_categories.grid(row=0, column=0, pady=5)
        
        self.frames = {}     # Fills a dictionary with every page on the app
        
        for f in (StartPage, GamePage):
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=1, column=0, sticky="nswe")
            frame.rowconfigure([0,1,2,3,4,5], weight=1)
            frame.columnconfigure([0,2], weight=2)
            frame.columnconfigure([1], weight=1)
        
        self.show_frame(StartPage)     # Shows StartPage

    
    def show_frame(self, cont):     # Shows page
        frame = self.frames[cont]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")


# ------------------------------ START PAGE
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        color = "#%06x" % R.randint(0, 0xFFFFFF)
        opposite = opposite_color(color)

    # LABEL - Start game!
        self.btn_start = tk.Button(self,
                                   text="START GAME!",
                                   relief=tk.SUNKEN,
                                   fg=color,
                                   bg=opposite,
                                   activeforeground=color,
                                   activebackground=opposite,
                                   font=("Verdana", 50, "bold"),
                                   command=lambda: self.controller.show_frame(GamePage),
                                   )
        self.btn_start.grid(row=0, column=0, rowspan=5, columnspan=3, sticky="nswe")

    # LABEL - Please, select a category...
        lbl1 = tk.Label(self,
                        text="Please, select a category from the list",
                        relief=tk.SUNKEN,
                        fg=opposite,
                        bg=color,
                        activeforeground=opposite,
                        activebackground=color,
                        font=("Verdana", 12),
                        )
        lbl1.grid(row=5, column=0, columnspan=3, sticky="nswe")


# ------------------------------ GAME PAGE
class GamePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.controller.cmb_categories.bind("<<ComboboxSelected>>",
                                            lambda event, parent=self: Game(event, self)
                                            )
                
    # FRAME - Left - Radio buttons with words/names
        self.frm_left = tk.Frame(self,
                                 relief=tk.SUNKEN,
                                 borderwidth=1,
                                 bg="pink",
                                 )
        self.frm_left.grid_propagate(False)
        self.frm_left.grid(row=0, column=0, rowspan=10, padx=5, pady=5, sticky="nswe")

    # FRAME - Right - Radio buttons as images (no selection dot)
        self.frm_right = tk.Frame(self,
                                  relief=tk.SUNKEN,
                                  borderwidth=1,
                                  bg="light blue",
                                  )
        self.frm_right.grid_propagate(False)
        self.frm_right.grid(row=0, column=2, rowspan=10, padx=5, pady=5, sticky="nswe")

    # LABEL - Scoreboard
        self.lbl_scoreboard = tk.Label(self,
                                       text="SCOREBOARD",
                                       height=1,
                                       relief=tk.RIDGE,
                                       borderwidth=2,
                                       fg="orange",
                                       font=("Verdana", 25, "bold"),
                                       )
        self.lbl_scoreboard.grid(row=0, column=1, pady=5, sticky="new")

    # LABEL - Score
        self.lbl_score = tk.Label(self,
                                  height=1,
                                  relief=tk.FLAT,
                                  fg="purple",
                                  font=("Verdana", 25),
                                  )
        self.lbl_score.grid(row=1, column=1, rowspan=2, sticky="n")

    # LABEL - Your answer is...
        lbl1 = tk.Label(self,
                        text="Your answer is...",
                        height=1,
                        font=("MS Sans Serif", 15),
                        )
        lbl1.grid(row=3, column=1, pady=6, sticky="n")

    # LABEL - Correct / Incorrect
        self.lbl_answer = tk.Label(self,
                                   relief=tk.SUNKEN,
                                   width=10,
                                   font=("Verdana", 25, "bold"),
                                   )
        self.lbl_answer.grid(row=3, column=1, pady=31, sticky="new")

    # CANVAS
        self.canvas = tk.Canvas(self,
                                height=320,
                                width=150,
                                )
        self.canvas.grid(row=4, column=1, sticky="nswe")

    # LABEL - Name
        self.lbl_name = tk.Label(self,
                                 height=1,
                                 font=("Courier New", 15, "bold"),
                                 )
        self.lbl_name.grid(row=5, column=1, sticky="n")

        self.bind("<<ShowFrame>>",
                  lambda event, parent=self: Game(event, parent)
                  )


# ------------------------------ GAME
class Game:

    def __init__(self, event, parent):
        self.parent = parent

        self.categ = set_categories()
        
        self.combo = self.parent.controller.cmb_categories

        self.score = 0

        self.parent.lbl_score["text"] = self.score
        self.parent.lbl_answer["text"] = ""
        self.parent.canvas.delete("all")
        self.parent.lbl_name["text"] = ""

        for rad in self.parent.frm_left.winfo_children():
            if rad != None:
                rad.destroy()

        for rad in self.parent.frm_right.winfo_children():
            if rad != None:
                rad.destroy()

        self.build_game()


    def build_game(self):     # Generates the radio button sets based on the selected category
        self.options = []

        for key, value in self.categ.items():     # Fills the elements list
            if self.combo.current() != -1:
                if self.parent.controller.cmb_var.get() == key.upper():
                    self.current_category = key.upper()

                    for val in value:
                        self.options.append(val.upper())

        for n in range(0, 5):     # Shuffles the original list
            R.shuffle(self.options)

        if len(self.options) > 4:     # Leaves the first four elements of the list
            while len(self.options) > 4:
                self.options.remove(self.options[-1])

        self.var_left = tk.StringVar()
        self.var_left.set(-1)
        self.var_right = tk.StringVar()
        self.var_right.set(-1)
        
    # RADIO BUTTONS - Left - Names
        for n in range(0, 5):
            R.shuffle(self.options)

        i = 0

        for option in self.options:
            self.rad1 = tk.Radiobutton(self.parent.frm_left,
                                       text=option,
                                       variable=self.var_left,
                                       value=option,
                                       bg="pink",
                                       activebackground="pink",
                                       font=("Verdana", 12),
                                       command=self.play_game
                                       )
            self.rad1.grid(row=i, column=0, padx=25, pady=35, ipady=15, sticky="nw")

            i += 1

    # RADIO BUTTONS - Right - Images (no selection dot)
        for n in range(0, 5):
            R.shuffle(self.options)

        j = 0

        self.lst_img = []

        for option in self.options:
            self.img_tmp1 = Image.open(FILE_PATH + option.lower() + ".png")
            self.img_tmp1 = self.img_tmp1.resize((120, 120), Image.ANTIALIAS)

            self.img1 = ImageTk.PhotoImage(self.img_tmp1)

            self.lst_img.append(self.img1)

            self.rad2 = tk.Radiobutton(self.parent.frm_right,
                                       variable=self.var_right,
                                       value=option,
                                       image=self.lst_img[j],
                                       indicatoron=0,
                                       command=self.play_game,
                                       )
            self.rad2.grid(row=j, column=0, padx=100, pady=5, sticky="nswe")

            j += 1

    def play_game(self):     # Starts the game
        self.select_left = self.var_left.get()
        self.select_right = self.var_right.get()

        if self.select_left != "-1" or self.select_right != "-1":
            self.parent.lbl_answer["text"] = ""

            self.parent.canvas.delete("all")

            self.parent.lbl_name["text"] = ""

        
        if self.select_left != "-1" and self.select_right != "-1":
            if self.select_left == self.select_right:     # Correct answer
                self.score += 1     # Updates score
                self.parent.lbl_score["text"] = self.score

                self.parent.lbl_answer["text"] = "CORRECT!"
                self.parent.lbl_answer["fg"] = "green"
                
                self.img_temp2 = Image.open(FILE_PATH + self.select_left.lower() + ".png")
                self.img_temp2 = self.img_temp2.resize((300, 300), Image.ANTIALIAS)

                self.img2 = ImageTk.PhotoImage(self.img_temp2)     # Shows image in canvas

                self.parent.canvas.create_image(210, 172,     # Shows name below canvas
                                                image=self.img2,
                                                anchor=tk.CENTER,
                                                )

                self.parent.lbl_name["text"] = self.select_left

                for rad in self.parent.frm_left.winfo_children():     # Destroys selected radio buttons
                    if rad["value"] == self.select_left:
                        self.var_left.set("-1")
                        rad.destroy()

                for rad in self.parent.frm_right.winfo_children():     # Destroys selected radio buttons
                    if rad["value"] == self.select_right:
                        self.var_right.set("-1")
                        rad.destroy()

            else:     # Incorrect answer
                self.parent.lbl_answer["text"] = "INCORRECT!"
                self.parent.lbl_answer["fg"] = "red"

                self.var_left.set("-1")
                self.var_right.set("-1")

            # When runs out of radio buttons, generates new radio button sets
            if (len(self.parent.frm_left.children) == 0) and (len(self.parent.frm_right.children) == 0):
                self.build_game()


def main():
    app = MultipleJoy()
    app.title("Multiple Joy!")

    w = 1100
    h = 597

    sw = app.winfo_screenwidth()
    sh = app.winfo_screenheight()

    x = (sw/2) - (w/2)
    y = (sh/2) - (h/2)

    app.geometry("%dx%d+%d+%d" % (w, h, x, y-30))

    app.mainloop()


main()