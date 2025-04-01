import tkinter as tk
from tkinter import PhotoImage
from PIL import ImageTk, Image
from core.src.articulate_image import ArticulateImage
from core.src.reorient import Reorient
from core.src.draggable_label import DraggableLabel

__all__ = [
    "Layer",
    "Layers"
]

class Layer:
    def __init__(self):
        self._widget_state = None
        self.label = None

    def store_image(self, image: ArticulateImage):
        self._image = image
        self._tk_image = ImageTk.PhotoImage(image.image)

    def show_image(self, frame):
        self._image.resize((frame.winfo_width(), frame.winfo_height()), resample=Image.Resampling.NEAREST)
        self._tk_image = ImageTk.PhotoImage(self._image.image)
        self.label = DraggableLabel(frame, image=self._tk_image)
        
        # Save the positioning of the image layer
        self.label.image = self._tk_image
        self.label.place(x=0, y=0)

    @property
    def widget_state(self):
        return self._widget_state
    
    @widget_state.setter
    def widget_state(self, new_state):
        if self.label:
            self._widget_state = new_state
            if new_state == "Move":
                self.label.drag_active = True
            else:
                self.label.drag_active = False

class Layers:
    def __init__(self):
        self.layer_number = 0
        self.layers = []
    
    def add_layer(self, layer: Layer):
        self.layers.append(layer)
        self.layer_number += 1



