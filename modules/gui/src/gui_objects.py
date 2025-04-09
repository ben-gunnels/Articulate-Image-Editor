import os
from collections import namedtuple

from types import MappingProxyType
from app.Globals import Globals
from gui.utils import *

__all__ = [
    "GetMenuBarButtons", 
    "GetSubFrames",
    "GetDropdownOptions",
    "GetWidgetButtons",
    "ButtonData"
]

def GetMenuBarButtons():
    return ["File", "Edit", "Help"] 

def GetSubFrames(globals: Globals):
    SUB_FRAMES = {
        "layers-frame": ({"width": int(globals.SCREEN_WIDTH * 0.78), 
                         "height": int(globals.SCREEN_HEIGHT * 0.87), 
                         "borderwidth": 2, 
                         "bg": "#A9A9A9"}, 
                         {"row": 2, "column": 1, "padx": 15, "pady": 15}),
        "widgets-frame": ({"width": int(globals.SCREEN_WIDTH * 0.18), 
                          "height": int(globals.SCREEN_HEIGHT * 0.87), 
                          "borderwidth": 2, 
                          "bg": "#A9A9A9"}, 
                          {"row": 2, "column": 0, "padx": 15, "pady": 15, "ipadx": 10, "ipady": 10})
    }
    return MappingProxyType(SUB_FRAMES) # Freeze SUB_FRAMES

def GetDropdownOptions():
    # Dropdown menu options 
    return [{"Open": None, "Save": None}, {"Undo": None, "Redo": None}, {"Docs": None}]

def GetWidgetButtons():
    """
        Generates the button layout for each of the widgets that are used as image editing tools.
    """
    button_names = ["Move", "Scale", "Rotate", "Crop", "Scalpel", "Brightness", "Saturation", "Contrast", "Blur", "Delete", "Layers", "Draw"]

    def get_horizontal_padding(i):
        if i%2:
            return (5, 20)
        else:
            return (40, 5)
        
    def get_vertical_padding(i):
        if i == 0:
            return (20, 5)
        else:
            return 5
    return [(name, {"row": i // 2, "column": i%2, "ipadx": 10, "ipady": 10, "padx": get_horizontal_padding(i), "pady": get_vertical_padding(i//2)}) for i, name in enumerate(button_names)]

ButtonData = namedtuple("ButtonData", "button icon")
