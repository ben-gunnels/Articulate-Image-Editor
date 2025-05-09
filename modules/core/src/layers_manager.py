from tkinter import messagebox
from core.src.layers import *
from core.src.file_manager import *

class LayersManager:
    def __init__(self, root, globals):
        self._layers = Layers(globals)
        self._file_manager = FileManager()
        self._root = root

    def upload_file(self):
        image = self._file_manager.upload_file()
        new_layer = Layer(self._gui_frame)
        # Store the image, add it to the layers, and show it
        new_layer.store_image(image)

        if not self._layers.add_layer(new_layer):
            messagebox.showerror("Layer Limit Exceeded",
                                message="Layer limit has been exceeded. Delete a layer to make room for your new layer.")
        new_layer.show_image()
        
    def save_file(self):
        output_image = self._layers.save_layers()
        self._file_manager.save_file(output_image)

    def provide_frames(self, sub_frames):
        self._gui_frame = sub_frames["layers-frame"]

    def on_click(self, event):
        print(f"{event.x}, {event.y}")

    def update_active_widget(self, active_widget):  
        for layer in self._layers.layers:
            layer.widget_state = active_widget
    
    def register_event(self, event_type: str, event=None, params=[]):
        match event_type:
            case "layers-click":
                self._layers.layers_clicked(event)
            case "scale-slide":
                self._layers.send_action(event_type, params)
            case "initialize-crop":
                self._layers.send_action(event_type, params)
            case "crop-slide":
                self._layers.send_action(event_type, params)
            case "contrast-slide":
                self._layers.send_action(event_type, params)
            case "brightness-slide":
                self._layers.send_action(event_type, params)
            case "blur-slide":
                self._layers.send_action(event_type, params)
            case "saturation-slide":
                self._layers.send_action(event_type, params)
            case "delete-layer":
                self._layers.send_action(event_type, params)
            case "scalpel":
                self._layers.send_action(event_type, params)
            case "return":
                self._layers.send_action(event_type, params)
            case "rotate":
                self._layers.send_action(event_type, params)
            case _:
                raise ValueError(f"{event_type} not a valid event_type.")
            
    
