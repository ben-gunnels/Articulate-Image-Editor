import numpy as np
from collections import namedtuple
__all__ = [
    "Point",
    "alpha_blend",
    "get_non_transparent_bounds"
]

Point = namedtuple("Point", "x y")

def alpha_blend(src, dst):
    """
    Alpha blends src RGBA over dst RGBA (both as uint8 arrays).
    Assumes src and dst are (H, W, 4).
    Returns the blended result (H, W, 4).
    """
    src = src.astype(np.float32) / 255.0
    dst = dst.astype(np.float32) / 255.0

    src_rgb = src[..., :3]
    src_alpha = src[..., 3:]

    dst_rgb = dst[..., :3]
    dst_alpha = dst[..., 3:]

    out_alpha = src_alpha + dst_alpha * (1 - src_alpha)
    out_rgb = (src_rgb * src_alpha + dst_rgb * dst_alpha * (1 - src_alpha)) / np.clip(out_alpha, 1e-6, 1)

    out = np.concatenate((out_rgb, out_alpha), axis=-1)
    return (out * 255).astype(np.uint8)

def get_non_transparent_bounds(image):
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