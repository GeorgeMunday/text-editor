import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog
import tkinter as tk

class TextEditor:
    def __init__(self):
        self.window = tb.Window(themename="morph")  
        self.window.title("Python Text Editor")
        self.window.geometry("")

        self.text_area = tb.Text(self.window, wrap="word", undo=True, font=("Consolas", 12))
        self.text_area.pack(expand=YES, fill=BOTH)

        self.status = tb.Label(self.window, text="Words: 0  Characters: 0", anchor="w")
        self.status.pack(side="bottom", fill="x")
        self.text_area.bind("<<Modified>>", self.update_status)

        self.current_file = None
        self.create_menu()
        self.bind_shortcuts()

        self.window.mainloop()

    def create_menu(self):
        menu = tb.Menu(self.window)
        self.window.config(menu=menu)

        file_menu = tb.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.quit)

        toolbar_menu = tb.Menu(menu, tearoff=0)
        menu.add_cascade(label="Toolbar", menu=toolbar_menu)
        toolbar_menu.add_command(label="Undo", command=lambda: self.text_area.event_generate("<<Undo>>"))
        toolbar_menu.add_command(label="Redo", command=lambda: self.text_area.event_generate("<<Redo>>"))
        toolbar_menu.add_separator()
        toolbar_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        toolbar_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        toolbar_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        
        color_menu = tb.Menu(menu, tearoff=0)
        menu.add_cascade(label="Color", menu=color_menu)
        color_menu.add_command(label="Red", command=lambda: self.change_text_color("red"))
        color_menu.add_command(label="Green", command=lambda: self.change_text_color("green"))
        color_menu.add_command(label="Blue", command=lambda: self.change_text_color("blue"))

        # Theme Menu
        theme_menu = tb.Menu(menu, tearoff=0)
        menu.add_cascade(label="Theme", menu=theme_menu)

        themes = ["flatly", "minty", "litera", "lumen", "sandstone", "yeti",
                  "morph", "pulse", "darkly", "cyborg", "solar", "superhero", "vapor"]

        for theme in themes:
            theme_menu.add_command(label=theme.capitalize(), command=lambda t=theme: self.change_theme(t))

        font_menu = tb.Menu(menu, tearoff=0)
        menu.add_cascade(label="Font", menu=font_menu)
        font_menu.add_command(label="Increase Font", command=self.increase_font)
        font_menu.add_command(label="Decrease Font", command=self.decrease_font)

    def bind_shortcuts(self):
        self.window.bind("<Control-n>", lambda event: self.new_file())
        self.window.bind("<Control-o>", lambda event: self.open_file())
        self.window.bind("<Control-s>", lambda event: self.save_file())
        self.window.bind("<Control-z>", lambda event: self.text_area.event_generate("<<Undo>>"))
        self.window.bind("<Control-y>", lambda event: self.text_area.event_generate("<<Redo>>"))
        self.window.bind("<Control-x>", lambda event: self.text_area.event_generate("<<Cut>>"))
        self.window.bind("<Control-c>", lambda event: self.text_area.event_generate("<<Copy>>"))
        self.window.bind("<Control-v>", lambda event: self.text_area.event_generate("<<Paste>>"))

    def change_theme(self, theme_name):
        self.window.style.theme_use(theme_name)
        
    def change_text_color(self, color):
        try:
            start = self.text_area.index("sel.first")
            end = self.text_area.index("sel.last")
            self.text_area.tag_configure(color, foreground=color)
            self.text_area.tag_add(color, start, end)
        except tk.TclError:
            pass

    def new_file(self):
        self.text_area.delete(1.0, "end")
        self.current_file = None
        self.window.title("Python Text Editor")

    def open_file(self):
        file = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()
                self.current_file = file
                self.window.title(f"Python Text Editor - {file}")
                self.text_area.delete(1.0, "end")
                self.text_area.insert("insert", content)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not open file:\n{e}")

    def save_file(self):
        if not self.current_file:
            file = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if not file:
                return
            self.current_file = file

        try:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text_area.get(1.0, "end-1c"))
            self.window.title(f"Python Text Editor - {self.current_file}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Could not save file:\n{e}")

    def update_status(self, event=None):
        text = self.text_area.get("1.0", "end-1c")
        words = len(text.split())
        chars = len(text)
        self.status.config(text=f"Words: {words}  Characters: {chars}")
        self.text_area.edit_modified(False)

    def increase_font(self):
        font = self.text_area.cget("font")
        name, size = font.split()
        size = int(size) + 2
        self.text_area.config(font=(name, size))

    def decrease_font(self):
        font = self.text_area.cget("font")
        name, size = font.split()
        size = max(2, int(size) - 2)
        self.text_area.config(font=(name, size))

if __name__ == "__main__":
    TextEditor()
