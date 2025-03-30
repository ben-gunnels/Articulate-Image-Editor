import tkinter as tk

from gui.src.config import *
from app.Globals import Globals

__all__ = [
    "GUI"
]

g = Globals()

class GUI(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master)
        g.APP_TITLE = kwargs.get("app_title", g.APP_TITLE)
        g.SCREEN_WIDTH = kwargs.get("screen_width", 1640)
        g.SCREEN_HEIGHT = kwargs.get("screen_height", 1220)

        InitializeGUIConfiguration(self, **kwargs)

        self.pack()

        self.grid()
        
        # Create a menu bar frame and align it to top-left
        menu_frame = tk.Frame(self)
        menu_frame.grid(row=0, column=0, sticky="nw", columnspan=7)

        menu_bar_buttons = GetMenuBarButtons()
        sub_frames = GetSubFrames(g)

        for key, value in menu_bar_buttons.items():
            tk.Button(menu_frame, text=key).grid(**value)

        for key, (val1, val2) in sub_frames.items():
            tk.Frame(self, **val1).grid(**val2)