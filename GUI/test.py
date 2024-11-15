import tkinter as tk
from PIL import Image, ImageDraw
import numpy as np

#from some import show_image

DRAW_THICC = 20

class Output:

    def __init__(self):
        self.image_mat = None
        self.exit = False
    
output = Output()

def create():
    # Define the size of the canvas and the resized dimensions
    WIDTH, HEIGHT = 300, 300
    RESIZED_WIDTH, RESIZED_HEIGHT = 28, 28

    # Initialize the main application window
    root = tk.Tk()

    # Create a Tkinter canvas widget
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
    canvas.pack()

    # Create an image to draw on using Pillow
    image = Image.new("L", (WIDTH, HEIGHT), "black")  # "L" mode for grayscale
    draw = ImageDraw.Draw(image)

    # Function to draw on the canvas
    def paint(event):
        x, y = event.x, event.y
        # Draw a small black circle on both the canvas and the Pillow image
        canvas.create_oval(x-DRAW_THICC, y-DRAW_THICC, x+DRAW_THICC, y+DRAW_THICC, fill='white', outline='white')
        draw.ellipse([x-DRAW_THICC, y-DRAW_THICC, x+DRAW_THICC, y+DRAW_THICC], fill='white')

    # Bind the mouse drag event to the paint function
    canvas.bind("<B1-Motion>", paint)

    # Function to clear the canvas and the Pillow image
    def clear():
        # Clear the Pillow image by filling it with black
        draw.rectangle([(0, 0), (WIDTH, HEIGHT)], fill="black")

        # Clear the Tkinter canvas by deleting all drawn items
        canvas.delete("all")

    # Function to save, resize, and convert the image to a NumPy array
    def save_and_convert(output:Output):

        # Resize the image to 28x28
        resized_image = image.resize((RESIZED_WIDTH, RESIZED_HEIGHT), Image.ANTIALIAS)
            
        # Convert the resized image to a NumPy array
        image_mat = np.array(resized_image)

        #show_image(image_mat.flatten())
        

        output.image_mat = image_mat
        
        # Quit the Tkinter main loop
        root.quit()


    def exit(output:Output):
        output.exit = True
        root.quit()
        
            
    

    # Add buttons for saving and clearing the canvas
    submit_btn = tk.Button(root, text="Done!", command=lambda: save_and_convert(output), width=10, height=2, font=('Arial', 10, "bold"))
    clear_btn = tk.Button(root, text="Clear", command=clear, width=10, height=2, font=('Arial', 10, "bold"))
    clear_btn = tk.Button(root, text="Exit", command=lambda: exit(output), width=10, height=2, font=('Arial', 10, "bold"))
    submit_btn.pack(side="left", padx=5)
    clear_btn.pack(side="left", padx=5)

    # Run the Tkinter main loop

    



    root.mainloop()
