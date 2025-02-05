import cv2
import easygui
import numpy as np
import imageio
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image

def cartoonify(image_path):
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    
    if original_image is None:
        messagebox.showerror("Error", "Cannot find any image. Choose an appropriate file.")
        return
    
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)
    smooth_gray = cv2.medianBlur(gray_image, 7)
    edges = cv2.adaptiveThreshold(smooth_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 9)
    color_filtered = cv2.bilateralFilter(original_image, 10, 250, 250)
    cartoon_image = cv2.bitwise_and(color_filtered, color_filtered, mask=edges)
    
    display_images([original_image, gray_image, smooth_gray, edges, color_filtered, cartoon_image])
    save_button = tk.Button(root, text="Save Cartoon Image", command=lambda: save_image(cartoon_image, image_path), padx=30, pady=5, bg='#364156', fg='white', font=('calibri', 10, 'bold'))
    save_button.pack(side=tk.TOP, pady=10)

def display_images(images):
    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    plt.show()

def save_image(cartoon_image, image_path):
    new_name = "cartoonified_Image"
    path = os.path.join(os.path.dirname(image_path), new_name + os.path.splitext(image_path)[1])
    cv2.imwrite(path, cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR))
    messagebox.showinfo("Saved", f"Image saved as {path}")

def upload_image():
    image_path = easygui.fileopenbox()
    if image_path:
        cartoonify(image_path)

root = tk.Tk()
root.geometry('400x400')
root.title('Cartoonify Your Image!')
root.configure(bg='white')

title_label = tk.Label(root, text="Cartoonify Your Image", bg='#CDCDCD', font=('calibri', 20, 'bold'))
title_label.pack(pady=20)

upload_button = tk.Button(root, text="Cartoonify an Image", command=upload_image, padx=10, pady=5, bg='#364156', fg='white', font=('calibri', 10, 'bold'))
upload_button.pack(pady=20)

root.mainloop()
