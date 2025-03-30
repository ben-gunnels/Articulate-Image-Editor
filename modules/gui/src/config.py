from types import MappingProxyType
from app.Globals import Globals
"""
Layout:
     _________________________________________
    |MENU_BAR_BUTTONS  |         |tk.Frame    |
    |__________________|         |WidgetsFrame|
    | tk.Frame LayersFrame       |  Buttons   |
    |                            |    for     |
    |    Box for Image Editing   |  widgets   |
    |                            |            |
    |                            |            |
    |                            |            |
    |____________________________|____________|

"""


__all__ = [
    "InitializeGUIConfiguration",
    "GetMenuBarButtons", "GetSubFrames",
]

def GetMenuBarButtons():
    MENU_BAR_BUTTONS = {
        "File": {"row": 0, "column": 0, "padx": 5, "pady": 5}, 
        "Edit": {"row": 0, "column": 1, "padx": 5, "pady": 5}, 
        "View": {"row": 0, "column": 2, "padx": 5, "pady": 5}, 
        "Help": {"row": 0, "column": 3, "padx": 5, "pady": 5}
    }

    return MappingProxyType(MENU_BAR_BUTTONS) # Frozen Dict

def GetSubFrames(globals: Globals):
    print(globals.SCREEN_WIDTH / 2)
    SUB_FRAMES = {
        "LayersFrame": ({"width": int(globals.SCREEN_WIDTH * 0.8), "height": int(globals.SCREEN_HEIGHT * 0.87), "borderwidth": 2, "bg": "red"}, {"row": 2, "column": 0, "padx": 5, "pady": 5}),
        "WidgetsFrame": ({"width": int(globals.SCREEN_WIDTH * 0.175), "height": int(globals.SCREEN_HEIGHT * 0.87), "borderwidth": 2, "bg": "green"}, {"row": 2, "column": 6, "padx": 5, "pady": 5})
    }
    return MappingProxyType(SUB_FRAMES) # Freeze SUB_FRAMES


def InitializeGUIConfiguration(gui, app_title, screen_width, screen_height):
    gui.master.title(app_title)
    gui.master.maxsize(screen_width, screen_height)
    gui.master.geometry(f"{screen_width}x{screen_height}")

