import tkinter as tk

__all__ = [
    "scale_widget"
]

def scale_widget(master):
    scale_widget_frame = tk.Frame(master, width=300, height=30, bg="lightgray")
    # slider = tk.Scale(scale_widget_frame, from_=0, to=100, orient=tk.HORIZONTAL)
    slider = tk.Scale(scale_widget_frame,
        from_=0,
        to=100,
        orient=tk.HORIZONTAL,
        length=80,
        sliderlength=20,
        troughcolor="gray",
        fg="blue",         # label color
        bg="white",        # background color
        activebackground="lightblue",
        highlightthickness=0,
        width=15           # thickness of the trough
    )
    slider.set(50)
    slider.pack()
    return scale_widget_frame
