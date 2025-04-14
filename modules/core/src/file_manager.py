from tkinter import filedialog, messagebox
from core.src.articulate_image import ArticulateImage

__all__ = [
    "FileManager"
]

class FileManager:
    _valid_file_types = (("PNG Files", "*.png"), ("JPG Files", "*.jpg"), ("JPEG Files", "*.jpeg"))
    
    def upload_file(self) -> ArticulateImage:
        file = filedialog.askopenfile(mode='rb', filetypes=self._valid_file_types)

        if file:
            try:
                bytes = file.read()
                return ArticulateImage(bytes)
            except Exception as e:
                messagebox.showerror("Error!", str(e))

    def save_file(self, image=None):
        if image is None:
            messagebox.showerror("Error", "No image to save.")
            return

        filetypes = [("PNG files", "*.png")]
        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=filetypes)

        if filepath:
            try:
                image.save(filepath)
                messagebox.showinfo("Success", f"Image saved to {filepath}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save image:\n{str(e)}")