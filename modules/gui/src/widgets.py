import tkinter as tk

__all__ = [
    "scale_widget",
    "crop_widget"
]

def scale_widget(master, command):
    scale_widget_frame = tk.Frame(master, width=300, height=30, bg="lightgray")
    # Add label above the slider
    for (label, slider_type) in [("Adjust Width", "width"), ("Adjust Height", "height"), ("Adjust Width/Height", "all")]:
        _add_slider(scale_widget_frame, label, slider_type, command, "scale-slide")
    return scale_widget_frame

def crop_widget(master, command):
    scale_widget_frame = tk.Frame(master, width=300, height=30, bg="lightgray")

    # Add label above the slider
    for (label) in ["Bottom", "Left", "Top", "Right"]:
        _add_slider(scale_widget_frame, label, label, command, "crop-slide", initial_value=100)
    return scale_widget_frame

def _add_slider(master, label, slider_type, command, event_name, initial_value=50):
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

    slider.set(initial_value)
    slider.config(command=lambda value: command(event_name, params=[slider_type, int(value)]))
    slider.pack()

