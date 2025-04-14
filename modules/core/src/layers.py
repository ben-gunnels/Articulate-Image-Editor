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
        """
        Stores the given ArticulateImage object as the current image layer and sets its position.

        Args:
            image (ArticulateImage): The image object to store.
            start_x (int, optional): X-coordinate of the top-left corner. Defaults to 0.
            start_y (int, optional): Y-coordinate of the top-left corner. Defaults to 0.

        Returns:
            None
        """
        self._image = image
        self._set_image_position(start_x, start_y)


    def show_image(self):
        """
        Initializes the display size of the current image and renders it in the frame.

        The method adjusts the image to fit within the frame dimensions,
        updates its associated mask, and refreshes the display label.

        Returns:
            None
        """
        self._image.initialize_size((self._frame.winfo_width(), self._frame.winfo_height()), resample=Image.Resampling.NEAREST)
        self._update_mask()
        self._update_label(destroy=False)


    def unclick(self):
        """
        Handles the unclick action for the layer’s label, reverting any active visual state.

        Only performs the unclick if the widget state is not set to "Delete" and
        the label exists.

        Returns:
            None
        """
        if self._widget_state != "Delete":
            if self.label:
                self.label.unclick()


    def handle_return(self):
        """
        Handles the return action based on the current widget state.

        For example, if the widget state is "Scalpel", it finalizes and applies
        the polygon mask using `_handle_scalpel_return`.

        Returns:
            None
        """
        match self._widget_state:
            case "Scalpel":
                self._handle_scalpel_return()


    def resize(self, params):
        """
        Resizes the image based on the provided scaling parameters.

        Args:
            params (list): A list with [direction: str, scale: int]. For example, ["width", 120].

        Raises:
            AssertionError: If `params` does not contain exactly two elements or has incorrect types.

        Returns:
            None
        """
        assert (len(params) == 2)
        assert (isinstance(params[0], str))
        assert (isinstance(params[1], int))

        self.resizer.resize(params, self._image, self.last_scalers)
        self._update_mask()
        self._set_image_position(self.x, self.y)
        self._update_label()


    def rotate(self):
        """
        Rotates the current image 90 degrees clockwise and updates the label display.

        Returns:
            None
        """
        self.reorient.rotate(self._image)
        self._update_label()


    def add_crop_box(self):
        """
        Highlights the image label with a visible border to indicate cropping mode.

        This provides visual feedback that the image is being cropped.

        Returns:
            None
        """
        self.label.config(
            highlightthickness=3,
            highlightbackground="black",
            highlightcolor="black"
        )


    def crop(self, params):
        """
        Crops the image in the specified direction by a given amount.

        This method supports directional cropping (Top, Bottom, Left, Right),
        adjusts the crop state trackers, repositions the image, and updates the display.

        Args:
            params (list): [direction: str, amount: int]

        Raises:
            AssertionError: If `params` does not contain exactly two elements.

        Returns:
            None
        """
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

        self._update_label()
        self.add_crop_box()


    def contrast(self, params):
        """
        Adjusts the contrast of the current image.

        Args:
            params (list): A list where the second element is the contrast value (int).

        Returns:
            None
        """
        self.color.contrast(self._image, params[1] / 50)
        self._update_label()


    def brightness(self, params):
        """
        Adjusts the brightness of the current image.

        Args:
            params (list): A list where the second element is the brightness value (int).

        Returns:
            None
        """
        self.color.brightness(self._image, (params[1] - 50) * 2)
        self._update_label()


    def blur(self, params):
        """
        Applies a blur effect to the current image.

        Args:
            params (list): A list where the second element is the blur intensity (int).

        Returns:
            None
        """
        self.color.blur(self._image, params[1])
        self._update_label()


    def saturation(self, params):
        """
        Adjusts the saturation level of the current image.

        Args:
            params (list): A list where the second element is the saturation value (int).

        Returns:
            None
        """
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

    def get_valid_bounds(self, bounds):
        """
            Returns the part of the layer that is within the layers frame.
        """
        start_row, start_col = 0, 0
        end_row, end_col = self._image.numpy().shape[0], self._image.numpy().shape[1]

        left = self.label.layer.x
        top = self.label.layer.y

        right = left + end_col
        bottom = top + end_row

        if left < bounds[0][0]:
            scale = (bounds[0][0] - left) / (right - left)
            start_col = scale * end_col
        
        if top < bounds[0][1]:
            scale = (bounds[0][1] - top) / (bottom - top)
            start_row = scale * end_row

        if right > bounds[2][0]:
            scale = (bounds[2][0] - left) / (right - left)
            end_col *= scale
        
        if bottom > bounds[2][1]:
            scale = (bounds[2][1] - top) / (bottom - top)
            end_row *= scale

        return (int(start_row), int(end_row), int(start_col), int(end_col))

    
    def _handle_scalpel_return(self):
        """
        Finalizes a scalpel (polygon mask) operation on the image layer.

        This method applies the current polygon mask to the layer's image, updates
        its pixel data, resets transparent pixels, and crops the image to only
        include visible content. It also updates the image's position to reflect any
        cropping offset and refreshes the label widget accordingly.

        Steps performed:
        - Applies the polygon mask to the current image.
        - Sets fully transparent pixels to (0, 0, 0, 0).
        - Crops the image to non-transparent bounds.
        - Recalculates the image's position on the canvas.
        - Reconfigures the layer's label widget for display.

        Returns:
            None
        """
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
        """
        Initializes or resets the mask used for scalpel polygon operations.

        This method creates a zeroed (fully transparent) mask with the same shape as
        the current image array. The mask is typically updated during interactive
        polygon editing (scalpel use).

        Returns:
            None
        """
        self.mask = np.zeros(self._image.numpy().shape)


    def _update_label(self, destroy=True):
        """
        Replaces the label widget representing this layer with an updated version.

        This is useful after an image has been modified or repositioned. It optionally
        destroys the old label widget, creates a new one with the updated image,
        and repositions it on the canvas.

        Args:
            destroy (bool): Whether to destroy the old label widget before updating. Default is True.

        Returns:
            None
        """
        if destroy:
            self.label.destroy()

        tk_image = ImageTk.PhotoImage(self._image.image)
        self.label = DraggableLabel(layer=self, master=self._frame, image=tk_image, bg="#A9A9A9")
        self.label.image = tk_image
        self.label.place(x=self._position[0].x, y=self._position[0].y)


    def _set_image_position(self, start_x, start_y):
        """
        Updates the positional coordinates of the image layer on the canvas.

        This method recalculates and sets the layer's bounding box based on the 
        specified top-left `(start_x, start_y)` position. It updates the internal 
        `_position` list of corner points accordingly.

        Args:
            start_x (int): X-coordinate of the top-left corner.
            start_y (int): Y-coordinate of the top-left corner.

        Returns:
            None
        """
        self._position = [
            Point(start_x, start_y),  # Top-left
            Point(start_x + self._image.width, start_y),  # Top-right
            Point(start_x + self._image.width, start_y + self._image.height),  # Bottom-right
            Point(start_x, start_y + self._image.height)  # Bottom-left
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
            Apply the default settings when a widget state is changed. 
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
    def __init__(self, globals: Globals):
        self.layer_number = 0
        self.layers = []
        self._active_layer = None
        self.globals = globals
    
    def add_layer(self, layer: Layer):
        """
        Adds a new layer to the current canvas if the layer limit has not been reached.

        The method appends a new `Layer` object to the internal list of layers, 
        and increments the layer count. If the addition would exceed the maximum 
        allowed layers (as defined in `self.globals.LAYER_LIMIT`), the method 
        returns 0 to indicate failure.

        Args:
            layer (Layer): The `Layer` object to be added.

        Returns:
            int: Returns 1 if the layer was successfully added, 0 otherwise.
        """
        if self.layer_number + 1 > self.globals.LAYER_LIMIT:
            return 0
        self.layers.append(layer)
        self.layer_number += 1
        return 1

    def layers_clicked(self, event):
        """
        Handles mouse click events to determine which layer, if any, has been clicked.

        This method checks if the click event occurred on a layer's label. If it did not,
        the active layer is reset and the `unclick()` method is called on that layer.
        This is typically used for deselecting a layer when clicking outside of it.

        Args:
            event (tkinter.Event): The event object containing click position and widget context.
        """
        for layer in self.layers:
            widget = event.widget.winfo_containing(event.x_root, event.y_root)
            if layer.label and widget == layer.label:
                pass
            else:
                self._active_layer = None
                layer.unclick()  # Clicked the frame
    
    def send_action(self, event_type: str, params: list):
        """
        Dispatches an action to the currently active layer based on the specified event type.

        This method acts as a centralized handler for a variety of user interface events,
        including transformations (scaling, cropping, rotating), image adjustments 
        (brightness, contrast, saturation, blur), and layer operations (deletion, return).

        Args:
            event_type (str): A string identifier for the type of action (e.g., 'scale-slide').
            params (list): A list of parameters required for the specified action.
        """
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

    def save_layers(self):
        """
        Merges all visible layers into a single RGBA image with alpha blending and crops it to content.

        This function:
        1. Creates a blank transparent canvas.
        2. Iterates through all layers and extracts their visible pixel regions.
        3. Applies proper alpha blending to composite each layer onto the canvas.
        4. Crops the resulting image to the smallest bounding box that includes all non-transparent pixels.
        5. Returns a PIL Image object representing the composited and cropped result.

        Returns:
            PIL.Image.Image: The final composited and cropped RGBA image.
        """
        canvas = np.zeros((self.globals.LAYERS_HEIGHT, self.globals.LAYERS_WIDTH, 4), dtype=np.uint8)

        for layer in self.layers:
            _canvas_bounds = ((0, 0), 
                            (self.globals.LAYERS_WIDTH, 0), 
                            (self.globals.LAYERS_WIDTH, self.globals.LAYERS_HEIGHT), 
                            (0, self.globals.LAYERS_HEIGHT))
            
            _start_row, _end_row, _start_col, _end_col = layer.get_valid_bounds(_canvas_bounds)

            _image_width = _end_col - _start_col
            _image_height = _end_row - _start_row

            _start_x = max(0, layer.label.layer.x)
            _start_y = max(0, layer.label.layer.y)

            layer_array = layer._image.numpy().astype(np.uint8)
            patch = layer_array[_start_row:_end_row, _start_col:_end_col]

            # Extract the canvas region where we’ll blend this patch
            canvas_patch = canvas[_start_y:_start_y+_image_height, _start_x:_start_x+_image_width]

            # Blend and write back
            blended_patch = alpha_blend(patch, canvas_patch)
            canvas[_start_y:_start_y+_image_height, _start_x:_start_x+_image_width] = blended_patch
        
        recropped_canvas = self._crop_to_size(canvas)

        output = Image.fromarray(recropped_canvas, mode="RGBA")
        return output
    
    def _crop_to_size(self, image):
        """
        Crops the given RGBA image array to the minimal bounding box that contains all non-transparent pixels.

        This function uses `get_non_transparent_bounds` to identify the bounds of non-transparent regions
        in the input image. It then leverages a `Resizer` and `ArticulateImage` to crop the image
        to these bounds, updating the internal numpy representation afterward.

        Args:
            image (np.ndarray): A NumPy array representing an RGBA image with shape (H, W, 4).

        Returns:
            np.ndarray: A NumPy array representing the cropped image, still in RGBA format.
        """
        bounds, _ = get_non_transparent_bounds(image)
        resizer = Resizer()
        articulate_image = ArticulateImage(image, mode="array")
        articulate_image.original_width, articulate_image.original_height = articulate_image.image.size
        resizer.crop_with_known_bounds(bounds, articulate_image)
        articulate_image._update_numpy()
        return articulate_image.numpy()

    def _get_active_layer(self): 
        """
        Returns the currently active layer if there is one.

        Relies on the layer's label property which stores the boolean value corresponding to it being selected. 
        """  
        for layer in self.layers:
            if layer.label.selected:
                self._active_layer = layer



 