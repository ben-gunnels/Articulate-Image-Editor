import tkinter as tk
import numpy as np
from PIL import ImageTk, Image
from core.src.articulate_image import ArticulateImage
from core.src.draggable_label import DraggableLabel
from core.src.reorient import Reorient
from core.src.image_scalpel import ImageScalpel
from core.src.color_augmentation import ColorEditor
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
    scalpel = ImageScalpel()
    reorient = Reorient()
    color = ColorEditor()
    # Holds the previous scaler value
    last_scalers = [50, 50, 50]
    crop_scalers = [100, 100, 100, 100] # Bottom, Left, Top, Right
    delta_x, delta_y = 0, 0
    last_dimension = None
    scalpel_points = []

    def __init__(self, frame):
        self._frame = frame
        self._widget_state = None
        self.x = 0
        self.y = 0

    def store_image(self, image: ArticulateImage, start_x=0, start_y=0):
        self._image = image
        self._set_image_position(start_x, start_y)
        
    def show_image(self):
        self._image.initialize_size((self._frame.winfo_width(), self._frame.winfo_height()), resample=Image.Resampling.NEAREST)
        self._update_mask()
        self._update_label(destroy=False)

    def unclick(self):
        if self._widget_state != "Delete":
            if self.label:
                self.label.unclick()

    def handle_return(self):
        match self._widget_state:
            case "Scalpel":
                self._handle_scalpel_return()

    def resize(self, params):
        assert (len(params) == 2)
        assert (isinstance(params[0], str))
        assert (isinstance(params[1], int))

        self.resizer.resize(params, self._image, self.last_scalers)
        self._update_mask()

        # Update position
        self._set_image_position(self.x, self.y)
        self._update_label()

    def rotate(self):
        """
            Rotate the image 90 degrees clockwise.
        """
        self.reorient.rotate(self._image)
        self._update_label()

    def add_crop_box(self):
        self.label.config(
            highlightthickness=3,               # Thickness of the border
            highlightbackground="black",        # Color of the border when not focused
            highlightcolor="black"              # Color of the border when focused
        )

    def crop(self, params):
        assert len(params) == 2
        _translation_table = {
            "Bottom": 0,
            "Left": 1,
            "Top": 2,
            "Right": 3
        }

        if self.last_dimension and self.last_dimension != params[0]:
            self._image.original_width = self._image.width
            self._image.original_height = self._image.height

        self.crop_scalers[_translation_table[params[0]]] = params[1]

        new_pos = self.resizer.crop(params[0], self._image, self.crop_scalers)

        self.x += new_pos[0] - self.delta_x if new_pos[0] > 0 else 0
        self.y += new_pos[1] - self.delta_y if new_pos[1] > 0 else 0

        self.delta_x = new_pos[0]
        self.delta_y = new_pos[1]

        self.last_dimension = params[0]
        self._set_image_position(self.x, self.y)

        # Update position
        self._update_label()
        self.add_crop_box()

    def contrast(self, params):
        self.color.contrast(self._image, params[1] / 50)
        self._update_label()

    def brightness(self, params):
        self.color.brightness(self._image, (params[1] - 50) * 2)
        self._update_label()

    def blur(self, params):
        self.color.blur(self._image, params[1])
        self._update_label()

    def saturation(self, params):
        self.color.saturation(self._image, params[1] / 50)
        self._update_label()
    
    def update_scalpel(self, event):
        """
        Handle a scalpel (drawing) update based on user input coordinates.

        This function appends the current (x, y) point to the list of scalpel points,
        draws connecting lines on the RGBA mask, blends the updated mask onto the
        base image using alpha transparency, and refreshes the GUI label to reflect
        the changes.

        Parameters:
            event (tuple): A tuple (x, y) containing the coordinates of the user interaction.
        """
        x, y = event
        self.scalpel_points.append((x, y))

        if len(self.scalpel_points) > 1:
            self._update_mask()
            # Draw on the RGBA mask
            self.scalpel.draw_lines(self.mask, self.scalpel_points)

            # Convert image to NumPy array
            image_array = self._image.numpy()

            # Extract RGB and Alpha channels from mask
            mask_rgb = self.mask[:, :, :3]
            alpha = self.mask[:, :, 3] / 255.0  # Normalize alpha to range [0, 1]

            # Apply alpha blending
            blended = image_array
            for c in range(3):  # Loop through B, G, R channels
                blended[:, :, c] = (
                    alpha * mask_rgb[:, :, c] + (1 - alpha) * image_array[:, :, c]
                ).astype(np.uint8)

            # Update the image object and GUI
            self._image.image_from_array()
            self._update_label()

            # Apply styling and state to the label
            self.label.config(
                highlightthickness=1,
                highlightbackground="blue",
                highlightcolor="blue"
            )
            self.label.selected = True
            self.label.scalpel = True
    
    def _handle_scalpel_return(self):
        self._update_mask()
        self._image._update_numpy()
        self.scalpel.apply_polygon_mask(self.mask, self.scalpel_points)
        # Get a fresh image
        self._image.resize((self._image.width, self._image.height), resample=Image.Resampling.NEAREST)
        image_array = self._image.numpy()
        image_array[:, :, 3] = self.mask[:, :, 3]
        image_array[image_array[:, :, 3] == 0] = [0, 0, 0, 0]  # R=0, G=0, B=0, A=0

        w, h = self._image.width, self._image.height

        self._image.image_from_array()
        (bounds, shifts) = self.scalpel.get_non_transparent_bounds(image_array)
        new_pos = self.resizer.crop_with_known_bounds(bounds, self._image)

        self.x += int(shifts[0] * w)
        self.y += int(shifts[2] * h)

        self._set_image_position(self.x, self.y)
        self._update_label()

        # Apply styling and state to the label
        self.label.config(
            highlightthickness=1,
            highlightbackground="blue",
            highlightcolor="blue"
        )

    def _update_mask(self):
        self.mask = np.zeros(self._image.numpy().shape)

    def _update_label(self, destroy=True):
        if destroy:
            self.label.destroy()
        tk_image = ImageTk.PhotoImage(self._image.image)
        self.label = DraggableLabel(layer=self, master=self._frame, image=tk_image, bg="#A9A9A9")

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


    def destroy(self):
        self.label.destroy()
        self._image.image.close()

    @property
    def widget_state(self):
        return self._widget_state
    
    @widget_state.setter
    def widget_state(self, new_state):
        """
            Set the default settings when a widget state is changed. 
        """
        if self.label and new_state != self.widget_state:
            self._widget_state = new_state
            match new_state:
                case "Move":
                    self.label.drag_active = True
                case "Resize":
                    self.last_scalers = [50, 50, 50]
                case "Delete":
                    pass
                case "Scalpel":
                    self.label.scalpel = True
                case "Rotate":
                    pass
                case _:
                    # Cleanup
                    self.unclick()
                    self._image._update_numpy()
                    self._image.set_changes()
                    self.crop_scalers = [100, 100, 100, 100]
                    self.last_scalers = [50, 50, 50]
                    self.scalpel_points = []
                    self.label.drag_active = False
                    self.label.scalpel = False

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
            case "contrast-slide":
                if self._active_layer:
                    self._active_layer.contrast(params)
            case "brightness-slide":
                if self._active_layer:
                    self._active_layer.brightness(params)
            case "blur-slide":
                if self._active_layer:
                    self._active_layer.blur(params)
            case "saturation-slide":
                if self._active_layer:
                    self._active_layer.saturation(params)
            case "delete-layer":
                if self._active_layer:
                    self._active_layer.destroy()
                    self.layers.remove(self._active_layer)
                    self._active_layer = None
            case "scalpel":
                pass
            case "rotate":
                if self._active_layer:
                    self._active_layer.rotate()
            case "return":
                if self._active_layer:
                    self._active_layer.handle_return()

    def _get_active_layer(self):
        for layer in self.layers:
            if layer.label.selected:
                self._active_layer = layer



 