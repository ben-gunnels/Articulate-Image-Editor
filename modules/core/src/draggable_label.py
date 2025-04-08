import tkinter as tk

class DraggableLabel(tk.Label):
    def __init__(self, layer, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Button-1>", self.on_click)         # Mouse click
        self.bind("<B1-Motion>", self.on_drag)         # Mouse drag
        self.layer = layer
        self._drag_data = {"x": 0, "y": 0}
        self.drag_active = False
        self.selected = False

    

    def on_click(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

        self.selected = True
        # Add thin blue outline
        self.config(
            highlightthickness=1,              # Thickness of the border
            highlightbackground="blue",        # Color of the border when not focused
            highlightcolor="blue"              # Color of the border when focused
        )
    
    def unclick(self):
        self.selected = False

        self.config(
            highlightthickness=0
        )

    def on_drag(self, event):
        if self.drag_active:
            dx = event.x - self._drag_data["x"]
            dy = event.y - self._drag_data["y"]
            self.layer.x = self.winfo_x() + dx
            self.layer.y = self.winfo_y() + dy
            self.place(x=self.layer.x, y=self.layer.y)