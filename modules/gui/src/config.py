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
]


def InitializeGUIConfiguration(gui, globals):
    gui.master.title(globals.APP_TITLE)
    gui.master.maxsize(globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT)
    gui.master.minsize(globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT)
    gui.master.geometry(f"{globals.SCREEN_WIDTH}x{globals.SCREEN_HEIGHT}")

