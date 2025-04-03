import tkinter as tk

__all__ = [
    "scale_widget"
]

def scale_widget(master):
    scale_widget_frame = tk.Frame(master, width=300, height=30, bg="lightgray")
    scaler = tk.Scale(scale_widget_frame, from_=0, to=100, orient=tk.HORIZONTAL)
    scaler.pack()
    return scale_widget_frame
