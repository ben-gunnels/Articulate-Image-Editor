import tkinter as tk
from PIL import Image
from core.src.layer_manager import *
from app.Globals import *
from gui.src.config import *
from gui.src.gui_objects import *
from gui.utils import *

__all__ = [
    "GUI"
]

class GUI(tk.Frame):
    def __init__(self, master, globals: Globals, layer_manager: LayerManager):
        super().__init__(master)
        self.menus = {}
        self.sub_frames = {}
        self.button_objects = {}
        self.button_icons = {}
        self.layer_manager = layer_manager
        self.layer_manager.provide_frames(self.sub_frames)

        # Widget Control
        self.active_widget = None

        InitializeGUIConfiguration(self, globals)

        self.pack()

        self.grid()
        
        # Create a menu bar frame and align it to top-left
        menu_bar = tk.Menu(self)
        master.config(menu=menu_bar)

        self._set_menu_bar(menu_bar)
        self._set_sub_frames(globals)
        self._set_widget_buttons()

    def _set_menu_bar(self, menu_bar):
        menu_bar_buttons = GetMenuBarButtons()
        dropdown_options = GetDropdownOptions()
        self._set_menu_bar_functions(dropdown_options=dropdown_options)
        for i, key in enumerate(menu_bar_buttons):
            self.menus[key] = tk.Menu(menu_bar)
            for (label, command) in dropdown_options[i].items():
                self.menus[key].add_command(label=label, command=command)

            menu_bar.add_cascade(label=key, menu=self.menus[key])

    def _set_sub_frames(self, globals):
        sub_frames_data = GetSubFrames(globals)
        for key, (val1, val2, val3) in sub_frames_data.items():
            frame = tk.Frame(self, **val1)
            frame.grid(**val2)
            if not val3:
                frame.pack_propagate(False)
            self.sub_frames[key] = frame

    def _set_widget_buttons(self):
        widget_buttons = GetWidgetButtons()

        for i, (button, kwargs) in enumerate(widget_buttons):
            self.button_icons[button] = tk.PhotoImage(file=get_icon_path(button))
            self.button_objects[button] = tk.Button(
                self.sub_frames["widgets-frame"], 
                image=self.button_icons[button], 
                command=lambda b=button: self._bind_widget(b)
            ) 
            self.button_objects[button].grid(**kwargs)

    def _set_menu_bar_functions(self, dropdown_options):
        for menu_bar_button in dropdown_options:
            match menu_bar_button:
                case {"Open": None, "Save": None}:
                    menu_bar_button["Open"] = self.layer_manager.upload_file
                    menu_bar_button["Save"] = self.layer_manager.save_file

                case {"Undo": None, "Redo": None}:
                    pass

                case {"Docs": None}:
                    pass

                case _:
                    raise ValueError("Unknown Menu Bar Button Object")
    
    def _bind_widget(self, b):
        if self.active_widget:
            button = self.button_objects[self.active_widget]
            button.config(relief="raised")
            self.layer_manager.update_active_widget(None)
            if self.active_widget == b:
                self.active_widget = None
                return
            
        button = self.button_objects[b]
        button.config(relief="sunken")
        self.active_widget = b
        self.layer_manager.update_active_widget(b)
