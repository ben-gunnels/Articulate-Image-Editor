import tkinter as tk

__all__ = [
    "scale_widget"
]

def scale_widget(master, command):
    scale_widget_frame = tk.Frame(master, width=300, height=30, bg="lightgray")
    # Add label above the slider
    for (label, slider_type) in [("Adjust Width", "width"), ("Adjust Height", "height"), ("Adjust Width/Height", "all")]:
        _add_slider(scale_widget_frame, label, slider_type, command)
    return scale_widget_frame

def _add_slider(master, label, slider_type, command):
    slider_label = tk.Label(master, text=label, bg="lightgray", fg="black")
    slider_label.pack(pady=(5, 0))  # Add some padding above the label
    slider = tk.Scale(master,
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
        width=15,          # thickness of the trough
    )

    slider.set(50)
    slider.config(command=lambda value: command("scale-slide", params=[slider_type, int(value)]))
    slider.pack()

