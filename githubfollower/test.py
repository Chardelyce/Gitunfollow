import tkinter as tk
from tkinter import ttk
import math

# Create the main GUI window
root = tk.Tk()
root.title("Wave Animation")
root.geometry("800x600")
root.resizable(False, False)

# Colors
bg_color = "#000000"  # Black background
wave_color = "#551A8B"  # Purple wave color

# Create a canvas for the animation
canvas = tk.Canvas(root, width=800, height=600, bg=bg_color)
canvas.pack()

# Function to create the initial wave animation
def create_wave():
    x1, y1, x2, y2 = 0, 400, 0, 400
    for _ in range(800):
        x2 = x1 + 1
        y2 = 400 + math.sin(x2 / 50) * 50  # Adjust the parameters for the desired wave effect
        canvas.create_line(x1, y1, x2, y2, fill=wave_color, width=2, tags="wave")
        x1, y1 = x2, y2
    canvas.update()

# Function to move the wave animation
def move_wave():
    for line in canvas.find_withtag("wave"):
        coords = canvas.coords(line)
        new_coords = [coord - 1 for coord in coords]
        canvas.coords(line, *new_coords)
    root.after(20, move_wave)  # Repeat the animation every 20 milliseconds

# Start creating and moving the wave animation
create_wave()
move_wave()

root.mainloop()
