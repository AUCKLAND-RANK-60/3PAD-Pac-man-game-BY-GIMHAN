import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkFont
import random

# Stores the entered data from the GUI
Pacman_Game = []

#Avoid making the same reciept number by storing
generated_receipt_number = set()

# Function to generate a unique random 5-digit receipt number
def generate_receipt_number():
    while True:
        receipt_number = str(random.randint(10000, 99999))
        if receipt_number not in generated_receipt_number:
            generated_receipt_number.add(receipt_number)
            return receipt_number

# Function to save data to a text file
def save_data(id_value, name_value):
    if id_value != "" and name_value != "":
        with open("data.txt", "a") as file:
            file.write(f"{id_value},{name_value}\n")
        messagebox.showinfo("Success", "Data saved successfully")
    else:
        messagebox.showwarning("Warning", "Please enter both ID and Name")

# Function to display data from the text file
def display_data():
    try:
        with open("data.txt", "r") as file:
            data = file.readlines()
        display_window = tk.Toplevel()
        display_window.title("Data Display")
        text = tk.Text(display_window)
        text.pack()
        for line in data:
            text.insert(tk.END, line)
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No data file found")

#Creating the main menue
# Initialize window
root = tk.Tk()
root.title("Pac-Man Math Game")

#Making Background
BG_OG_image = Image.open("Background_pacman.png")
BG_REZ_image = BG_OG_image.resize ((600,500))
background_image = ImageTk.PhotoImage(BG_REZ_image)

# Create Canvas
canvas = tk.Canvas(root, width=600, height=500)
canvas.pack()

#puttign the image int othe canva's
canvas.create_image(0,0, image= background_image, anchor="nw") #0,0 is the coridnates and nz means top left corner

# Create Pac-Man (Yellow Circle)
#pacman = canvas.create_rectangle(50, 50, 90, 90, fill="yellow")
#Making the PACMAN (using the PILLOW)
OG_image = Image.open("Pacman_BGR.png")
REZ_image = OG_image.resize ((40,40))
pacman_image = ImageTk.PhotoImage(REZ_image)

#Adding ghe setting pacman image to "pacman"
pacman = canvas.create_image(100,115, image=pacman_image)

#Finding the cordinates of he canvas
def get_coordinates(event):
    print(f"Mouse clicked at: {event.x}, {event.y}")
    
#Wall cordinates
Wall_cords = [
    (33, 22, 279, 39) #wall 1
]
#make the rectangle colltion wall
walls = []
for x1, y1, x2, y2 in Wall_cords:
    wall = canvas.create_rectangle(x1, y1, x2, y2, fill="")
    walls.append(wall)

# Check collision function
def check_collision(x1, y1, x2, y2):
    for wall in walls:
        wx1, wy1, wx2, wy2 = canvas.coords(wall)
        if not (x2 <= wx1 or x1 >= wx2 or y2 <= wy1 or y1 >= wy2):
            return True  # Collisioning  detected
    return False #colltiong not ditected

# Bind mouse click event to get the coordinates
canvas.bind("<Button-1>", get_coordinates)

# Move Pac-Man
def move_pacman(event):
    if event.keysym == "Left":
        canvas.move(pacman, -10, 0)  
    elif event.keysym == "Right":
        canvas.move(pacman, 10, 0)   
    elif event.keysym == "Up":
        canvas.move(pacman, 0, -10) 
    elif event.keysym == "Down":
        canvas.move(pacman, 0, 10)   
# Get current position
px, py = canvas.coords(pacman)  # Get center of Pacman
pacman_hitbox = (px - 20, py - 20, px + 20, py + 20)


# Check if the new position collides with walls
if not check_collision(x1 + px, y1 + py, x2 + px, y2 + py):
    canvas.move(pacman, px, py)

# Bind arrow keys
root.bind("<Left>", move_pacman)
root.bind("<Right>", move_pacman)
root.bind("<Up>", move_pacman)
root.bind("<Down>", move_pacman)

# Run the game loop
root.mainloop()

