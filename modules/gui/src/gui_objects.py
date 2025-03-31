import os
from types import MappingProxyType
from app.Globals import Globals
from gui.utils import *

__all__ = [
    "GetMenuBarButtons", 
    "GetSubFrames",
    "GetDropdownOptions",
    "GetWidgetButtons"
]

def GetMenuBarButtons():
    return ["File", "Edit", "Help"] 

def GetSubFrames(globals: Globals):
    SUB_FRAMES = {
        "layers-frame": ({"width": int(globals.SCREEN_WIDTH * 0.8), 
                         "height": int(globals.SCREEN_HEIGHT * 0.87), 
                         "borderwidth": 2, "bg": "#A9A9A9"}, 
                         {"row": 2, "column": 0, "padx": 30, "pady": 45}),
        "widgets-frame": ({"width": int(globals.SCREEN_WIDTH * 0.175), 
                          "height": int(globals.SCREEN_HEIGHT * 0.87), 
                          "borderwidth": 2, "bg": "#A9A9A9"}, 
                          {"row": 2, "column": 6, "padx": 15, "pady": 0})
    }
    return MappingProxyType(SUB_FRAMES) # Freeze SUB_FRAMES

def GetDropdownOptions():
    # Dropdown menu options 
    return [["Open", "Save"], ["Undo", "Redo"], ["Docs"]]

def GetWidgetButtons():
    """
        Generates the button layout for each of the widgets that are used as image editing tools.
    
    """
   

    return [
                ("Scalpel",     {"row": 0, "column": 0, "ipadx": 10, "ipady": 10, "padx": 5, "pady": 5}), 
                ("Rotate",      {"row": 0, "column": 1, "ipadx": 10, "ipady": 10, "padx": 5, "pady": 5}),
                ("Brightness",  {"row": 1, "column": 0, "ipadx": 10, "ipady": 10, "padx": 5, "pady": 5}),
                ("Saturation",  {"row": 1, "column": 1, "ipadx": 10, "ipady": 10, "padx": 5, "pady": 5}),
                ("Contrast",    {"row": 2, "column": 0, "ipadx": 10, "ipady": 10, "padx": 5, "pady": 5}),
                ("Blur",        {"row": 2, "column": 1, "ipadx": 10, "ipady": 10, "padx": 5, "pady": 5}),
                ("Filter",      {"row": 3, "column": 0, "ipadx": 10, "ipady": 10, "padx": 5, "pady": 5}),
                ("Move",        {"row": 3, "column": 1, "ipadx": 10, "ipady": 10, "padx": 5, "pady": 5}),
                ("Layers",      {"row": 4, "column": 0, "ipadx": 10, "ipady": 10, "padx": 5, "pady": 5}),
                ("Crop",        {"row": 4, "column": 1, "ipadx": 10, "ipady": 10, "padx": 5, "pady": 5}),
                ("Draw",        {"row": 5, "column": 0, "ipadx": 10, "ipady": 10, "padx": 5, "pady": 5}),
                ("Enhance",     {"row": 5, "column": 1, "ipadx": 10, "ipady": 10, "padx": 5, "pady": 5})
            ]

