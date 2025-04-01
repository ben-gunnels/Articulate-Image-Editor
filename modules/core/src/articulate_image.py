import io
import numpy as np
from PIL import Image

class ArticulateImage:
    """
        The standard image object for the Articulate Image Editor. 
    
    """
    def __init__(self, bytes):
        self.image = Image.open(io.BytesIO(bytes))
        self._numpy = np.array(self.image, dtype=np.uint8)
        self.width, self.height = self.image.size
       
    def numpy(self):
        return self._numpy
    
    def resize(self, new_size: tuple, resample):
        new_w, new_h = new_size

        # Determine the dominant scale factor
        _scale_factor = min(new_w / self.width, new_h / self.height)

        # Compute the new dimensions while maintaining aspect ratio
        scaled_w, scaled_h = int(self.width * _scale_factor), int(self.height * _scale_factor)

        # Resize the image
        self.image = self.image.resize((scaled_w, scaled_h), resample=resample)
        self.width, self.height = self.image.size
