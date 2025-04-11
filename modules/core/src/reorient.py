import numpy as np
from core.src.Widget import Widget
from core.src.articulate_image import ArticulateImage

class Reorient(Widget):
    def __init__(self):
        super().__init__()

    def rotate(self, image: ArticulateImage):
        # Perform the rotation
        image_array = image.numpy()
        image._numpy = np.rot90(image_array)
        image.image_from_array()
        image.set_changes()
