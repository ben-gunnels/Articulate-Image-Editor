import os

__all__ = [
    "get_icon_path"

]

def get_icon_path(icon: str):
    return os.path.join("..\data\icons", f"{icon.lower()}.png")
