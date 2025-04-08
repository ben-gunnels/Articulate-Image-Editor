import io
import numpy as np
from PIL import Image

class ArticulateImage:
    """
        The standard image object for the Articulate Image Editor. 
    
    """
    def __init__(self, bytes):
        self.image = Image.open(io.BytesIO(bytes))
        self.original_image = self.image.copy()
        self._numpy = np.array(self.image, dtype=np.uint8)

        self.prev_crop_dimension = None
       
    def numpy(self):
        return self._numpy
    
    def initialize_size(self, new_size, resample):
        _new_w, _new_h = new_size
        # Determine the dominant scale factor
        _scale_factor = min(_new_w / self.width, _new_h / self.height)

        # Compute the new dimensions while maintaining aspect ratio
        _scale_factor_w, _scale_factor_h = int(self.width * _scale_factor), int(self.height * _scale_factor)

        # Resize the image
        self.image = self.image.resize((_scale_factor_w, _scale_factor_h), resample=resample)
        self.original_width, self.original_height = self.image.size
        self._update_numpy()

    def resize(self, new_size: tuple, resample):
        _scale_factor_w = int(new_size[0])
        _scale_factor_h = int(new_size[1])

        self.image = self.original_image.copy().resize((_scale_factor_w, _scale_factor_h), resample=resample)
        self._update_numpy()

    def crop(self, dimension, value):
        new_pos = None # Tells the layer whether to move the starting position
        _temp_array = self.numpy().copy()

        if self.prev_crop_dimension and self.prev_crop_dimension != dimension:
            self._numpy = np.array(self.image, dtype=np.uint8)

        match dimension:
            case "Top":
                _scaler = _temp_array.shape[0] * (value / 100)
                _start_row = int(_temp_array.shape[0] - _scaler)
                _resized_array = _temp_array[_start_row:, :, :]
                self.image = Image.fromarray(_resized_array)
                new_pos = (self.original_height - self.height)
            case "Bottom":
                _end_row = int(_temp_array.shape[0] * (value / 100))
                _resized_array = _temp_array[:_end_row, :, :]
                self.image = Image.fromarray(_resized_array)
                new_pos = 0
            case "Right":
                _end_col = int(_temp_array.shape[1] * (value / 100))
                _resized_array = _temp_array[:, :_end_col, :]
                self.image = Image.fromarray(_resized_array)
                new_pos = 0
            case "Left":
                _scaler = _temp_array.shape[1] * (value / 100)
                _start_col = int(_temp_array.shape[1] - _scaler)
                _resized_array = _temp_array[:, _start_col:, :]
                self.image = Image.fromarray(_resized_array)
                new_pos = (self.original_width - self.width)
        self.prev_crop_dimension = dimension
        return new_pos
    @property
    def width(self):
        return self.image.size[0]
    
    @property
    def height(self):
        return self.image.size[1]

    def _update_numpy(self):
        self._numpy = np.array(self.image, dtype=np.uint8)  


