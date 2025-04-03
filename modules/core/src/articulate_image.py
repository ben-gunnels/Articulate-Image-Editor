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
        self.width, self.height = self.image.size
        self.original_width, self.original_height = self.original_image.size
       
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
        self.width, self.height = self.image.size

    
    def resize(self, new_size: tuple, resample, keep_aspect_ratio=True):
        _scale_factor_w = int(new_size[0])
        _scale_factor_h = int(new_size[1])

        self.image = self.original_image.resize((_scale_factor_w, _scale_factor_h), resample=resample)
        self.width, self.height = self.image.size


