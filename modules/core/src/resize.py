from PIL import ImageTk, Image

class Resizer:
    def __init__(self):
        pass

    def resize(self, params, image, scalers):
        dimension, value = params

        match dimension:
            case "all":
                _new_width = (value / scalers[2]) * image.width
                _new_height = (value / scalers[2]) * image.height
                _new_width = max(_new_width, 1) # Ensure  there is a positive width
                _new_height = max(_new_height, 1) # Ensure a positive height
                image.resize((_new_width, _new_height), resample=Image.Resampling.NEAREST)
                # Update the most recent scaler for all
                scalers[2] = value
            case "width":
                _new_width = (value / scalers[0]) * image.width
                _new_width = max(_new_width, 1)
                image.resize((_new_width, image.height), resample=Image.Resampling.NEAREST)
                # Update the most recent scaler for the width
                scalers[0] = value
            case "height":
                _new_height = (value / scalers[1]) * image.height
                _new_height = max(_new_height, 1)
                image.resize((image.width, _new_height), resample=Image.Resampling.NEAREST)
                # Update the most recent scaler value for the height
                scalers[1] = value

    def crop(self, params, image, scalers):
        dimension, value = params
        
        new_pos = image.crop(dimension, value)
        return new_pos