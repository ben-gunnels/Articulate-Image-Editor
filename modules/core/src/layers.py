import tkinter as tk
from PIL import ImageTk, Image
from core.src.articulate_image import ArticulateImage
from core.src.reorient import Reorient
from core.src.draggable_label import DraggableLabel
from core.src.utils.utils import *
from app.Globals import Globals
from core.src.resize import Resizer

__all__ = [
    "Layer",
    "Layers"
]

g = Globals()

class Layer:
    resizer = Resizer()
    # Holds the previous scaler value
    last_scaler = [50, 50, 50]
    def __init__(self, frame):
        self._frame = frame
        self._widget_state = None
        self.x = 0
        self.y = 0

    def store_image(self, image: ArticulateImage):
        self._image = image
        self._set_image_position(0, 0)
        
    def show_image(self):
        self._image.initialize_size((self._frame.winfo_width(), self._frame.winfo_height()), resample=Image.Resampling.NEAREST)
        self._update_label()

    def unclick(self):
        if self.label:
            self.label.unclick()

    def resize(self, params):
        assert (len(params) == 2)
        assert (isinstance(params[0], str))
        assert (isinstance(params[1], int))

        self.resizer.resize(params, self._image, self.last_scaler)

        # Update position
        self._set_image_position(self.x, self.y)
        self.label.destroy()
        self._update_label()

    def add_crop_box(self):
        self.label.config(
            highlightthickness=3,              # Thickness of the border
            highlightbackground="black",        # Color of the border when not focused
            highlightcolor="black"              # Color of the border when focused
        )

    def crop(self, params):
        new_pos = self.resizer.crop(params, self._image, None)
        if new_pos: # update the position on top or left crop
            match params[0]:
                case "Top":
                    self._set_image_position(self.x, self.y + new_pos)
                case "Left":
                    self._set_image_position(self.x + new_pos, self.y)
                case _:
                    self._set_image_position(self.x, self.y)

        # Update position
        self.label.destroy()
        self._update_label()
        self.add_crop_box()

    def _update_label(self):
        tk_image = ImageTk.PhotoImage(self._image.image)
        self.label = DraggableLabel(layer=self, master=self._frame, image=tk_image)

        self.label.image = tk_image

        self.label.place(x=self._position[0].x, y=self._position[0].y)

    def _set_image_position(self, start_x, start_y):
        # Save the positioning of the image layer
        self._position = [
            Point(start_x, start_y), # Left top corner of layer
            Point(start_x + self._image.width, start_y), # Top right corner
            Point(start_x + self._image.width, start_y + self._image.height), # Bottom right corner
            Point(start_x, start_y + self._image.height) # Bottom left corner
        ]

    @property
    def widget_state(self):
        return self._widget_state
    
    @widget_state.setter
    def widget_state(self, new_state):
        if self.label:
            self._widget_state = new_state
            match new_state:
                case "Move":
                    self.label.drag_active = True
                case "Resize":
                    self.last_scaler = [50, 50, 50]
                case _:
                    self.unclick()
                    self.last_scaler = [50, 50, 50]
                    self.label.drag_active = False

class Layers:
    def __init__(self):
        self.layer_number = 0
        self.layers = []
        self._active_layer = None
    
    def add_layer(self, layer: Layer):
        if self.layer_number + 1 > g.LAYER_LIMIT:
            return 0
        self.layers.append(layer)
        self.layer_number += 1
        return 1

    def layers_clicked(self, event):
        for layer in self.layers:
            widget = event.widget.winfo_containing(event.x_root, event.y_root)
            if layer.label and widget == layer.label:
                pass
            else:
                self._active_layer = None
                layer.unclick()  # Clicked the frame
    
    def send_action(self, event_type: str, params: list):
        self._get_active_layer()

        match event_type:
            case "scale-slide":
                if self._active_layer:  
                    self._active_layer.resize(params)
            case "initialize-crop":
                if self._active_layer:
                    self._active_layer.add_crop_box()
            case "crop-slide":
                if self._active_layer:
                    self._active_layer.crop(params)

    def _get_active_layer(self):
        for layer in self.layers:
            if layer.label.selected:
                self._active_layer = layer



