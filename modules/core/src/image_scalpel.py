import cv2
import numpy as np
from core.src.utils.utils import *

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
        return get_non_transparent_bounds(image)