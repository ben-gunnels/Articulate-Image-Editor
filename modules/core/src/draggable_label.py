import tkinter as tk

class DraggableLabel(tk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Button-1>", self.on_click)         # Mouse click
        self.bind("<B1-Motion>", self.on_drag)         # Mouse drag
        self._drag_data = {"x": 0, "y": 0}
        self.drag_active = False

    def on_click(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_drag(self, event):
        if self.drag_active:
            dx = event.x - self._drag_data["x"]
            dy = event.y - self._drag_data["y"]
            x = self.winfo_x() + dx
            y = self.winfo_y() + dy
            self.place(x=x, y=y)