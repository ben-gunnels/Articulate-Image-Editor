import tkinter as tk
from PIL import Image
from gui.src.config import *
from gui.src.gui_objects import *
from gui.utils import *

__all__ = [
    "GUI"
]


class GUI(tk.Frame):
    def __init__(self, master, globals):
        super().__init__(master)
        self.menus = {}
        self.sub_frames = {}
        self.button_icons = {}

        InitializeGUIConfiguration(self, globals)

        self.pack()

        self.grid()
        
        # Create a menu bar frame and align it to top-left
        menu_bar = tk.Menu(self)
        master.config(menu=menu_bar)

        menu_bar_buttons = GetMenuBarButtons()
        sub_frames_data = GetSubFrames(globals)

        dropdown_options = GetDropdownOptions()


        for i, key in enumerate(menu_bar_buttons):
            self.menus[key] = tk.Menu(menu_bar)
            for option in dropdown_options[i]:
                self.menus[key].add_command(label=option)

            menu_bar.add_cascade(label=key, menu=self.menus[key])

            #tk.OptionMenu(menu_frame, key, *dropdown_items[i]).grid(**value)


        for key, (val1, val2) in sub_frames_data.items():
            frame = tk.Frame(self, **val1)
            frame.grid(**val2)
            self.sub_frames[key] = frame

        widget_buttons = GetWidgetButtons()

        for (button, kwargs) in widget_buttons:
            self.button_icons[button] = tk.PhotoImage(file=get_icon_path(button))
            tk.Button(self.sub_frames["widgets-frame"], image=self.button_icons[button]).grid(**kwargs)
