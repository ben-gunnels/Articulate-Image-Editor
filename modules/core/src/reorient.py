from core.src.Widget import Widget

class Reorient(Widget):
    def __init__(self):
        super().__init__()

    def move(self, label):
        label.drag_active = True