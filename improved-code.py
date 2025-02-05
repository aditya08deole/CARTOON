# Import necessary libraries
import cv2  # OpenCV for image processing
import easygui  # File dialog for selecting images
import numpy as np  # Numerical operations
import imageio  # Image reading and writing
import os  # File handling
import sys  # System functions
import tkinter as tk  # GUI framework
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt  # Image visualization
from PIL import ImageTk, Image  # Image handling in Tkinter

class CartoonifyApp:
    """A GUI-based application to apply a cartoon effect to images."""
    
    def __init__(self, root):
        """Initialize the application window."""
        self.root = root
        self.root.geometry('500x500')
        self.root.title('Cartoonify Your Image!')
        self.root.configure(background='white')

        # Title Label
        self.label = tk.Label(self.root, text="Cartoonify Your Image!", 
                              background='#CDCDCD', font=('calibri', 20, 'bold'))
        self.label.pack(pady=20)

        # Upload Button
        self.upload_button = tk.Button(self.root, text="Upload Image", 
                                       command=self.upload_image, padx=10, pady=5)
        self.upload_button.configure(background='#364156', foreground='white', 
                                     font=('calibri', 12, 'bold'))
        self.upload_button.pack(pady=20)

        # Exit Button
        self.exit_button = tk.Button(self.root, text="Exit", command=root.quit, 
                                     padx=10, pady=5, background='#FF5733', 
                                     foreground='white', font=('calibri', 12, 'bold'))
        self.exit_button.pack(pady=10)

    def upload_image(self):
        """Opens a file dialog for the user to select an image."""
        image_path = easygui.fileopenbox(msg="Select an image file", title="Image Upload")
        if image_path:
            self.cartoonify(image_path)

    def cartoonify(self, image_path):
        """Applies a cartoon effect to an image and displays the transformation."""
        
        # Read the image and convert to RGB
        original_image = cv2.imread(image_path)
        if original_image is None:
            messagebox.showerror("Error", "Cannot find the image. Choose a valid file.")
            return
        
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        # Resize the original image
        resized_original = cv2.resize(original_image, (960, 540))

        # Convert to grayscale
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)
        resized_gray = cv2.resize(gray_image, (960, 540))

        # Apply median blur to smoothen the image
        smooth_gray = cv2.medianBlur(gray_image, 5)
        resized_smooth = cv2.resize(smooth_gray, (960, 540))

        # Detect edges using adaptive thresholding
        edges = cv2.adaptiveThreshold(smooth_gray, 255, 
                                      cv2.ADAPTIVE_THRESH_MEAN_C, 
                                      cv2.THRESH_BINARY, 9, 9)
        resized_edges = cv2.resize(edges, (960, 540))

        # Apply bilateral filter to preserve edges while smoothing the image
        color_filtered = cv2.bilateralFilter(original_image, 9, 250, 250)
        resized_color = cv2.resize(color_filtered, (960, 540))

        # Combine the filtered image with edges to create a cartoon effect
        cartoon_image = cv2.bitwise_and(color_filtered, color_filtered, mask=edges)
        resized_cartoon = cv2.resize(cartoon_image, (960, 540))

        # Display the transformation process
        self.display_images([resized_original, resized_gray, resized_smooth, 
                             resized_edges, resized_color, resized_cartoon])

        # Save Button
        save_button = tk.Button(self.root, text="Save Cartoon Image", 
                                command=lambda: self.save_image(resized_cartoon, image_path), 
                                padx=10, pady=5, background='#008CBA', foreground='white', 
                                font=('calibri', 12, 'bold'))
        save_button.pack(pady=20)

    def display_images(self, images):
        """Displays the transformation steps using Matplotlib."""
        
        fig, axes = plt.subplots(3, 2, figsize=(10, 10), subplot_kw={'xticks':[], 'yticks':[]}, 
                                 gridspec_kw={'hspace': 0.2, 'wspace': 0.2})
        titles = ["Original Image", "Grayscale Image", "Smooth Image", 
                  "Edge Detection", "Color Filtered", "Cartoonified Image"]
        
        for i, ax in enumerate(axes.flat):
            ax.imshow(images[i], cmap='gray')
            ax.set_title(titles[i], fontsize=10)

        plt.show()

    def save_image(self, image, image_path):
        """Saves the cartoonified image in the same directory as the original."""
        
        new_name = "cartoonified_Image"
        dir_path = os.path.dirname(image_path)
        extension = os.path.splitext(image_path)[1]
        save_path = os.path.join(dir_path, new_name + extension)

        # Convert to BGR before saving
        cv2.imwrite(save_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

        # Show success message
        messagebox.showinfo("Image Saved", f"Image saved at:\n{save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CartoonifyApp(root)
    root.mainloop()
