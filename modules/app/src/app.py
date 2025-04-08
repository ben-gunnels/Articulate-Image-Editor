import tkinter as tk
from gui.src.gui import GUI
from core.src.layers_manager import LayersManager
from app.Globals import Globals


root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# App Objects
g = Globals()
layer_manager = LayersManager(root)


g.SCREEN_WIDTH = int(screen_width * 0.75)
g.SCREEN_HEIGHT = int(screen_height * 0.75)

gui = GUI(root, g, layer_manager)

root.mainloop()