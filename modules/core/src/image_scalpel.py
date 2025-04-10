import cv2
import numpy as np

class ImageScalpel:
    line_color = (1, 1, 1, 255)
    line_thickness = 2

    def draw_lines(self, mask: np.array, clicked_points: list):
        for i in range(len(clicked_points) - 1):
            cv2.circle(mask, (clicked_points[i][0], clicked_points[i][1]), radius=2, color=(255, 255, 255, 255))
            cv2.line(mask, clicked_points[i], clicked_points[i+1], color=self.line_color, thickness=self.line_thickness)  
        cv2.circle(mask, (clicked_points[-1][0], clicked_points[-1][1]), radius=2, color=(255, 255, 255, 255))

    def apply_polygon_mask(self, mask, clicked_points: list):
        pts = np.array([clicked_points], dtype=np.int32)
        cv2.fillPoly(mask, pts, color=self.line_color)

    def get_non_transparent_bounds(self, image):
        """
        Returns the bounding box (left, top, right, bottom) of non-transparent pixels
        in an RGBA image.
        
        Parameters:
            rgba_image (np.ndarray): Image of shape (H, W, 4) with an alpha channel.
        
        Returns:
            (left, top, right, bottom): Coordinates of bounding box.
        """
        # Extract alpha channel
        alpha = image[:, :, 3]

        # Find coordinates where alpha > 0
        non_transparent_coords = np.argwhere(alpha > 0)

        if non_transparent_coords.size == 0:
            return None  # Entire image is transparent

        # Get bounds
        left = np.min(non_transparent_coords[:, 1])
        right = np.max(non_transparent_coords[:, 1]) + 1
        top = np.min(non_transparent_coords[:, 0])
        bottom = np.max(non_transparent_coords[:, 0]) + 1

        # How much does the image need to be shifted by
        left_shift = left / image.shape[1]
        right_shift = right / image.shape[1]
        top_shift = top / image.shape[0]
        bottom_shift = bottom / image.shape[0]

        return [(left, right, top, bottom), (left_shift, right_shift, top_shift, bottom_shift)]

