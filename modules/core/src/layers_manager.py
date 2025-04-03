from core.src.layers import *
from core.src.file_manager import *

class LayersManager:
    def __init__(self):
        self._layers = Layers()
        self._file_manager = FileManager()

    def upload_file(self):
        image = self._file_manager.upload_file()
        new_layer = Layer(self._gui_frame)
        # Store the image, add it to the layers, and show it
        new_layer.store_image(image)
        self._layers.add_layer(new_layer)  
        new_layer.show_image()
        
    def save_file(self):
        self._file_manager.save_file()

    def provide_frames(self, sub_frames):
        self._gui_frame = sub_frames["layers-frame"]

    def on_click(self, event):
        print(f"{event.x}, {event.y}")

    def update_active_widget(self, active_widget):  
        for layer in self._layers.layers:
            layer.widget_state = active_widget
    
    def register_event(self, event_type: str, event):
        match event_type:
            case "layers-click":
                self._layers.layers_clicked(event)

            case _:
                raise ValueError(f"{event_type} not a valid event_type.")