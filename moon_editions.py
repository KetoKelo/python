
import random as R
import tkinter as tk
from tkinter import ttk


class MoonEditions(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("MoonEditions")
        self.geometry("687x495")
        self.build_window()
        self.bind_all("<Key>", self.on_key_press)
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.count = 0

    def build_window(self):
        container = tk.Frame(self)
        container.grid(row=0, column=0, padx=5, sticky="nswe")

        self.txt_composer = tk.Text(container, width=61, height=30, wrap=tk.WORD)
        self.txt_composer.grid(row=0, column=0, pady=5, sticky="nswe")
        self.txt_composer.bindtags("selection")

        self.scroll = ttk.Scrollbar(container, command=self.txt_composer.yview)
        self.scroll.grid(row=0, column=1, pady=5, sticky="nsw")
        self.txt_composer["yscrollcommand"] = self.scroll.set

        frm_radiobuttons = tk.Frame(container, relief=tk.GROOVE, bd=2)
        frm_radiobuttons.grid(row=0, column=2, padx=5, pady=5, sticky="nswe")
        frm_radiobuttons.grid_rowconfigure([0, 1], weight=1)
        frm_radiobuttons.grid_rowconfigure([2], weight=30)

        self.var_language = tk.StringVar()
        self.var_language.set("spanish")

        rad_spanish = tk.Radiobutton(frm_radiobuttons, text="CASTELLANO",
                                     variable=self.var_language, value="spanish",
                                     command=lambda: Write(self).select_language()
                                     )
        rad_spanish.grid(row=0, column=0, padx=5, pady=5, sticky="nsw")

        rad_english = tk.Radiobutton(frm_radiobuttons, text="ENGLISH",
                                     variable=self.var_language, value="english",
                                     command=lambda: Write(self).select_language()
                                     )
        rad_english.grid(row=1, column=0, padx=5, pady=5, sticky="nsw")

        btn_erase = tk.Button(frm_radiobuttons, text="Erase All", width=20, height=3,
                              command=lambda: self.txt_composer.delete("1.0", tk.END))
        btn_erase.grid(row=2, column=0, padx=5, pady=5, sticky="swe")

        btn_create_file = tk.Button(frm_radiobuttons, text="Create File", width=20, height=3,
                                    command=lambda: File(self).create_file(Write(self).get_title()))
        btn_create_file.grid(row=3, column=0, padx=5, pady=5, sticky="swe")

    def on_key_press(self, event):
        self.count += 1

        if self.count == 1:
            Write(self).compose()
            self.count = 0
        
    def _on_mousewheel(self, event): # Enables mouse wheel scroll for textbox
        self.txt_composer.yview_scroll(int(-1*(event.delta/120)), "units")

class Write:

    def __init__(self, parent):
        self.parent = parent

    def select_language(self):
        if self.parent.var_language.get() == "english":
            words = words_english
        elif self.parent.var_language.get() == "spanish":
            words = words_spanish

        return words

    def compose(self):
        words = self.select_language()
        punctuation = " "

        rnd_ind = R.randint(0, len(words) - 1)
        if self.parent.txt_composer.get("1.0") != "":
            rnd_punct = R.randint(0, 30)

            if rnd_punct == 30:
                punctuation = ". "
            elif rnd_punct == 20:
                punctuation = ", "
            elif rnd_punct == 10:
                punctuation = "; "
            elif rnd_punct == 0:
                punctuation = ": "
            else:
                punctuation = " "

        self.parent.txt_composer.insert(tk.END, words[rnd_ind] + punctuation)
        self.parent.txt_composer.see(tk.END)

    def get_title(self):
        words = self.select_language()

        title = ""
        while len(title) < 50:
            rnd_ind = R.randint(0, len(words) - 1)
            title += words[rnd_ind] + " "
        
        title = title + "."
        

        return title.replace(" .", ".txt")

class File:

    def __init__(self, parent):
        self.parent = parent

    def create_file(self, file_name):
        if self.parent.txt_composer.get("1.0") != None:
            file = open(file_name, "w")
            file.write(self.parent.txt_composer.get("1.0", tk.END))
            file.close()


def get_words(file_path, file_name, char_list):
    words = []

    file = open(file_path + file_name, encoding="utf-8")
    text = file.read().replace("\n", " ")
    
    for char in char_list:
        if char in text:
            text = text.replace(char, "")

    text = text.split(" ")
    for word in text:
        if word.upper() not in words:
            words.append(word.upper())

    file.close()

    return words

if __name__ == "__main__":
    file_path = "C:\\Users\\HAL-9000\\OneDrive\\Programming\\Python\\Learning\\"
    file_english = "alices_adventures_in_wonderland.txt"
    file_spanish = "alicia_en_el_pais_de_las_maravillas.txt"
    chars = ["!",
             "¡",
             "?",
             "¿",
             "\'",
             "\\",
             "\"",
             "#",
             "*",
             "&",
             "“",
             "”",
             ",",
             ";",
             ".",
             ":",
             "-",
             "(",
             ")",
             "=",
             "—",
             "‘",
             "’",
             "»",
             "«",
        ]

    words_english = get_words(file_path, file_english, chars)
    words_spanish = get_words(file_path, file_spanish, chars)

    app = MoonEditions()
    Write(app).select_language()
    app.mainloop()