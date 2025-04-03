import tkinter as tk
from PIL import ImageTk, Image
from core.src.articulate_image import ArticulateImage
from core.src.reorient import Reorient
from core.src.draggable_label import DraggableLabel
from core.src.utils.utils import *

__all__ = [
    "Layer",
    "Layers"
]

class Layer:
    def __init__(self, frame):
        self._frame = frame
        self._widget_state = None

    def store_image(self, image: ArticulateImage):
        self._image = image
        self._set_image_position(0, 0)
        
    def show_image(self):
        self._image.resize((self._frame.winfo_width(), self._frame.winfo_height()), resample=Image.Resampling.NEAREST)
        self._update_label()

    def unclick(self):
        if self.label:
            self.label.unclick()

    def _update_label(self):
        tk_image = ImageTk.PhotoImage(self._image.image)
        self.label = DraggableLabel(master=self._frame, image=tk_image)

        self.label.image = tk_image

        self.label.place(x=self._position[0].x, y=self._position[0].y)

    def _set_image_position(self, start_x, start_y):
        # Save the positioning of the image layer
        self._position = [
            Point(start_x, start_y), # Left top corner of layer
            Point(start_x + self._image.width, start_y), # Top right corner
            Point(start_x + self._image.width, start_y + self._image.height),
            Point(start_x, start_y + self._image.height)
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
                    pass
                case _:
                    self.label.drag_active = False

class Layers:
    def __init__(self):
        self.layer_number = 0
        self.layers = []
    
    def add_layer(self, layer: Layer):
        self.layers.append(layer)
        self.layer_number += 1

    def layers_clicked(self, event):
        for layer in self.layers:
            widget = event.widget.winfo_containing(event.x_root, event.y_root)
            if layer.label and widget == layer.label:
                return  # Clicked a label
            else:
                layer.unclick()  # Clicked the frame



