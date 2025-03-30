import tkinter as tk
from gui.src.gui import GUI


root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

gui = GUI(root, app_title="Articulate Image Editor", screen_width=screen_width, screen_height=screen_height)

root.mainloop()