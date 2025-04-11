import cv2
import numpy as np
from core.src.articulate_image import ArticulateImage

class ColorEditor:
    def __init__(self):
        pass

    def contrast(self, image: ArticulateImage, alpha: float) -> None:
        """
        Adjusts the contrast of an image using a linear transformation.

        Parameters:
            image (ArticulateImage): The image object containing the original image.
            alpha (float): Contrast control factor.
                        - Values > 1.0 increase contrast.
                        - Values < 1.0 decrease contrast.
                        - Value of 1.0 leaves contrast unchanged.

        Returns:
            None. Updates the image._numpy array and regenerates the display image.
        """
        image_array = np.array(image.original_image, dtype=np.uint8)
        image._numpy = cv2.convertScaleAbs(image_array, alpha=alpha)
        image.image_from_array()


    def brightness(self, image: ArticulateImage, beta: float) -> None:
        """
        Adjusts the brightness of an image using a linear transformation.

        Parameters:
            image (ArticulateImage): The image object containing the original image.
            beta (float): Brightness control value.
                        - Positive values make the image brighter.
                        - Negative values make the image darker.
                        - Value of 0 leaves brightness unchanged.

        Returns:
            None. Updates the image._numpy array and regenerates the display image.
        """
        image_array = np.array(image.original_image, dtype=np.uint8)
        image._numpy = cv2.convertScaleAbs(image_array, beta=beta)
        image.image_from_array()


    def blur(self, image: ArticulateImage, value: int) -> None:
        """
        Applies Gaussian blur to the image.

        Parameters:
            image (ArticulateImage): The image object containing the original image.
            value (int): Strength of the blur. Must be a non-negative integer.
                        A value of 0 applies no blur.
                        The actual kernel size used is (2 * value + 1).

        Returns:
            None. Updates the image._numpy array and regenerates the display image.
        """
        if not isinstance(value, int):
            raise TypeError("value must be an int")
        
        if value == 0:
            return

        kernel_size = value * 2 + 1
        image_array = np.array(image.original_image, dtype=np.uint8)
        image._numpy = cv2.GaussianBlur(image_array, (kernel_size, kernel_size), 0)
        image.image_from_array()

    def saturation(self, image: ArticulateImage, factor: float) -> None:
        """
        Adjusts the saturation of an image by scaling the saturation (S) channel in HSV color space.

        Parameters:
            image (ArticulateImage): The image object containing the original image.
            factor (float): The factor by which to adjust saturation.
                            - Values > 1.0 increase saturation.
                            - Values < 1.0 decrease saturation.
                            - Value of 1.0 leaves the image unchanged.

        Returns:
            None. The method updates the image._numpy and regenerates the image view.
        """
        # Convert original image to NumPy array
        image_array = np.array(image.original_image, dtype=np.uint8)

        # Convert to HSV color space
        hsv_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_image)

        # Scale the saturation channel
        s = np.clip(s.astype(np.float32) * factor, 0, 255).astype(np.uint8)

        # Merge and convert back to BGR
        hsv_scaled = cv2.merge([h, s, v])
        recolored_image = cv2.cvtColor(hsv_scaled, cv2.COLOR_HSV2BGR)

        # Update the image object
        image._numpy = recolored_image
        image.image_from_array()