import tkinter as tk

__all__ = [
    "scale_widget",
    "crop_widget",
    "contrast_widget",
    "brightness_widget",
    "saturation_widget",
    "blur_widget"
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

def contrast_widget(master, command):
    scale_widget_frame = tk.Frame(master, width=300, height=30, bg="lightgray")
    _add_slider(scale_widget_frame, "Contrast", "Contrast", command, "contrast-slide")
    return scale_widget_frame

def brightness_widget(master, command):
    scale_widget_frame = tk.Frame(master, width=300, height=30, bg="lightgray")
    _add_slider(scale_widget_frame, "Brightness", "Brightness", command, "brightness-slide")
    return scale_widget_frame

def saturation_widget(master, command):
    scale_widget_frame = tk.Frame(master, width=300, height=30, bg="lightgray")
    _add_slider(scale_widget_frame, "Saturation", "Saturation", command, "saturation-slide")
    return scale_widget_frame

def blur_widget(master, command):
    scale_widget_frame = tk.Frame(master, width=300, height=30, bg="lightgray")
    _add_slider(scale_widget_frame, "Blur", "Blur", command, "blur-slide", initial_value=0, max_val=7)
    return scale_widget_frame

def _add_slider(master, label, slider_type, command, event_name, initial_value=50, min_val=0, max_val=100):
    slider_label = tk.Label(master, text=label, bg="lightgray", fg="black")
    slider_label.pack(pady=(5, 0))  # Add some padding above the label
    slider = tk.Scale(master,
        from_=min_val,
        to=max_val,
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

