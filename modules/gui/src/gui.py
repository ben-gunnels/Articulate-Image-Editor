import tkinter as tk
import time
from PIL import Image
from core.src.layers_manager import *
from app.Globals import *
from gui.src.config import *
from gui.src.articulate_frame import *
from gui.src.gui_objects import *
from gui.src.widgets import *
from gui.utils import *


__all__ = [
    "GUI"
]

class GUI(tk.Frame):
    # Define the stored objects
    menus = {
        "File": None,
        "Edit": None,
        "Help": None
    }

    sub_frames = {
        "layers-frame": None,
        "widgets-frame": None
    }

    buttons = {
            "Scalpel": None,
            "Rotate": None,
            "Brightness": None,
            "Saturation": None,
            "Contrast": None,
            "Blur": None,
            "Filter": None,
            "Move": None,
            "Layers": None,
            "Crop": None,
            "Draw": None,
            "Enhance": None
    }

    def __init__(self, master, globals: Globals, layers_manager: LayersManager):
        super().__init__(master)
        self.master = master
        self.layers_manager = layers_manager

        # Widget Control
        self.active_widget = None
        self.widget_box = None

        InitializeGUIConfiguration(self, globals)

        self.pack()

        self.grid()
        
        # Create a menu bar frame and align it to top-left
        menu_bar = tk.Menu(self)
        master.config(menu=menu_bar)

        self._set_menu_bar(menu_bar)
        self._set_sub_frames(globals)
        self.layers_manager.provide_frames(self.sub_frames)
        self._set_widget_buttons()

        self.master.bind("<Return>", self._on_enter)

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
        frame_functions = {
            "widgets-frame": None,
            "layers-frame": self._on_click_layers_frame
        }
        sub_frames_data = GetSubFrames(globals)
        for frame_name, (val1, val2) in sub_frames_data.items():
            frame = tk.Frame(self, **val1)
            frame.bind("<Button-1>", frame_functions[frame_name])
            frame.grid(**val2)
            self.sub_frames[frame_name] = frame

    def _set_widget_buttons(self):
        """
            Create the widget buttons with their proper icons. 
            Store the tk.Button object and tk.PhotoImage object corresponding to each button 
            in the buttons dictionary. 
        """
        # Get the widget button names with the corresponding grid placements
        widget_buttons = GetWidgetButtons()

        for (label, kwargs) in widget_buttons:
            button_icon = tk.PhotoImage(file=get_icon_path(label))
            button = tk.Button(
                self.sub_frames["widgets-frame"],
                image=button_icon, 
                command=lambda l=label: self._bind_widget(l)
            ) 
 
            # button_data is a namedtuple that holds the button and then the icon object for the button
            self.buttons[label] = ButtonData(button, button_icon)
            self.buttons[label].button.grid(**kwargs)

    def _set_menu_bar_functions(self, dropdown_options):
        """
            Assign the proper manager functions to the options that are given by the menu bar.
        """
        for menu_bar_button in dropdown_options:
            match menu_bar_button:
                case {"Open": None, "Save": None}:
                    menu_bar_button["Open"] = self.layers_manager.upload_file
                    menu_bar_button["Save"] = self.layers_manager.save_file

                case {"Undo": None, "Redo": None}:
                    pass

                case {"Docs": None}:
                    pass

                case _:
                    raise ValueError("Unknown Menu Bar Button Object")
                
    def _on_click_layers_frame(self, event):
        self.layers_manager.register_event("layers-click", event)
    
    def _bind_widget(self, label):
        """
            Manages logic for when a widget button is clicked. 
            If the widget is already active and it is clicked it sets its state to inactive.
            If a widget is inactive when it is clicked it sets its state to active.

            This modifies the layer_manager's active_widget property to the currently active widget or None.
            It sets the button to sunken if it becomes active or raised if it becomes inactive. 
        """
        if self.active_widget:
            if self.widget_box:
                self.widget_box.destroy()
                self.widget_box = None
            button = self.buttons[self.active_widget].button
            button.config(relief="raised")
            self.layers_manager.update_active_widget(None)
            if self.active_widget == label: # Button pressed is the currently active one so set it to inactive
                self.active_widget = None
                return
        
        button = self.buttons[label].button
        button.config(relief="sunken")
        self.active_widget = label
        self.layers_manager.update_active_widget(label)

        x, y = button.winfo_x(), button.winfo_y() + button.winfo_height()

        match label:
            case "Move":
                pass
            case "Scale":
                self.widget_box = scale_widget(self.sub_frames["widgets-frame"], self.layers_manager.register_event)
                self.widget_box.place(x=x, y=y)
            case "Rotate":
                pass
            case "Scalpel":
                self.layers_manager.register_event("scalpel")
            case "Brightness":
                pass
            case "Saturation":
                pass
            case "Contrast":
                pass
            case "Blur":
                pass
            case "Delete":
                self.layers_manager.register_event("delete-layer")
            case "Layers":
                pass
            case "Crop":
                self.layers_manager.register_event("initialize-crop")
                self.widget_box = crop_widget(self.sub_frames["widgets-frame"], self.layers_manager.register_event)
                self.widget_box.place(x=x, y=y)
            case "Draw":
                pass
            case _:
                raise ValueError(f"Invalid widget label {label}")
            
        if label == "Delete":
            time.sleep(0.3)
            self._bind_widget("Delete")

    def _on_enter(self, event):
        self.layers_manager.register_event("return")
