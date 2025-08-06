import os
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as tkFont
import random
import pygame
import time


#Sore is 0 at 1st
score = 0

# Initialize mixer
pygame.mixer.init()

# setting the dictionary file to the place of python file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#playign the music
pygame.mixer.music.load('PacMan_Original_Theme.mp3') 

# Play the music
pygame.mixer.music.play(-1)

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
canvas = tk.Canvas(root, width=600, height=550)
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
    (36, 27, 286, 24), #wall 1
    (41, 89, 47, 137), #wall 2 (downwards)
    (59, 84, 107, 82), #wall 3(sideways)
    (165, 85, 173, 134), #wall 4 (downwards)
    (112, 140, 173, 138), #wall 5 (sideways)
    (360, 29, 370, 81), #wall 6 (downward)
    (229, 83, 370, 81), #wall 7 (sideways)
    (425, 25, 558, 29), #wall 8 (sideways)
    (552, 29, 559, 134), #wall 9 (downwards)
    (36, 195, 110, 195), #wall 10 (sideways)
    (35, 251, 111, 249), #wall 11 (sideways)
    (40, 309, 44, 412), #wall 12 (downwards)
    (35, 469, 111, 468), #wall 13 (sideways)
    (167, 198, 176, 250), #wall 14 (downwards)
    (230, 143, 237, 304), #wall 15 (downwards)
    (430, 84, 489, 82), #wall 16 (sideways)
    (297, 141, 494, 144), #wall 17 (sideways)
    (111, 305, 175, 309), #wall 18 (sideways)
    (109, 361, 305, 358), #wall 19 (sideways)
    (234, 367, 239, 412), #wall 20 (downwards)
    (113, 419, 175, 423), #wall 21 (sideways)
    (163, 416, 175, 467), #wall 22 (downwards)
    (298, 198, 374, 198), #wall 23 (sideways)
    (298, 251, 374, 252), #wall 24 (sideways)
    (428, 197, 492, 199), #wall 25 (sideways)
    (552, 197, 560, 246), #wall 26 (downwards)
    (491, 251, 559, 253), #wall 27 (sideways)
    (428, 258, 437, 302), #wall 28 (downwards)
    (427, 306, 492, 307), #wall 29 (sideways)
    (428, 360, 563, 365), #wall 30 (sideways)
    (552, 306, 561, 412), #wall 31 (downwards)
    (297, 309, 369, 310), #wall 32 (sideways)
    (360, 306, 374, 410), #wall 33 (downwards)
    (361, 414, 492, 419), #wall 34 (sideways)
    (428, 470, 563, 473), #wall 35 (sidways)
    (296, 416, 307, 466), #wall 36 (downwards)
    (229, 470,373, 472) #wall 37 (sdeways)
    
]
    
#make the rectangle colltion wall
walls = []
for x1, y1, x2, y2 in Wall_cords:
    wall = canvas.create_rectangle(x1, y1, x2, y2, fill="", outline="")
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
    dx, dy = 0, 0

    if event.keysym == "Left":
        dx = -10
    elif event.keysym == "Right":
        dx = 10
    elif event.keysym == "Up":
        dy = -10
    elif event.keysym == "Down":
        dy = 10

    # Get Pacman's center
    px, py = canvas.coords(pacman)

    # Calculate future hitbox for Pacman
    x1 = px - 20 + dx
    y1 = py - 20 + dy
    x2 = px + 20 + dx
    y2 = py + 20 + dy

    # Check collision beforeing the moving
    if not check_collision(x1, y1, x2, y2):
        canvas.move(pacman, dx, dy)

# Bind arrow keys
root.bind("<Left>", move_pacman)
root.bind("<Right>", move_pacman)
root.bind("<Up>", move_pacman)
root.bind("<Down>", move_pacman)

#Creating the score keeper lable
scoreLabel = Label(root, text =":Your Score:" ,font="fixedsys 20")
scoreLabel.place(x=25, y=520)

#Update the score evry 1 second by adding one point
def update_score():
    #initialsing the score variable
    global score
    score += 1
    scoreLabel.config(text =f"Score:{score}")
    root.after(1000, update_score)

update_score()

#image oh ghost (1) (sideways)
OG_image1 = Image.open("Ghost_Pac.png")
REZ_image1 = OG_image1.resize ((39,39))
ghost_image1 = ImageTk.PhotoImage(REZ_image1)

#Adding ghe setting ghost image to "pacman"
ghost1 = canvas.create_image(331,441, image=ghost_image1)

    
#ADDING THE GHSOT DIRECTIONS
ghost_direc1 = 1

def everyframe():
#Helps keep it withi na loop and not break
    global ghost_direc1
    
#ADDING THE GHSOT DIRECTIONS
    #ghost_direc = 1
    ghost_left_limit1 = 330#left
    ghost_right_limit1 = 560 #rigt

#movign  the ghost left or right on repeat
    canvas.move(ghost1, ghost_direc1, 0)

#check the currunt x of the ghost
    gx, gy = canvas.coords(ghost1)

#swapping sides when moving
    if gx >= ghost_right_limit1:
        ghost_direc1 = -1
    elif gx <= ghost_left_limit1:
        ghost_direc1 = 1

#movign the ghost
    root.after(20, everyframe)
everyframe()

#---------------------------------------------------------#
 
#image oh ghost (2) (sideways)
OG_image2 = Image.open("Ghost_Pac.png")
REZ_image2 = OG_image2.resize ((40,39))
ghost_image2 = ImageTk.PhotoImage(REZ_image2)

#Adding ghe setting ghost image to "pacman"
ghost2 = canvas.create_image(43,171, image=ghost_image2)

    
#ADDING THE GHSOT DIRECTIONS
ghost_direc2 = 1

def everyframe2():
#Helps keep it withi na loop and not break
    global ghost_direc2
    
#ADDING THE GHSOT DIRECTIONS
    #ghost_direc = 1
    ghost_left_limit2 = 43#left
    ghost_right_limit2 = 168 #rigt

#movign  the ghost left or right on repeat
    canvas.move(ghost2, ghost_direc2, 0)

#check the currunt x of the ghost
    gx, gy = canvas.coords(ghost2)

#swapping sides when moving
    if gx >= ghost_right_limit2:
        ghost_direc2 = -1
    elif gx <= ghost_left_limit2:
        ghost_direc2 = 1

#movign the ghost
    root.after(20, everyframe2)

everyframe2()

#---------------------------------------------------------#
#image oh ghost (3) (sideways)
OG_image3 = Image.open("Ghost_Pac.png")
REZ_image3 = OG_image3.resize ((40,39))
ghost_image3 = ImageTk.PhotoImage(REZ_image3)

#Adding ghe setting ghost image to "pacman"
ghost3 = canvas.create_image(203,115, image=ghost_image3)

#ADDING THE GHSOT DIRECTIONS 
ghost_direc3 = 1

def everyframe3():
#Helps keep it withi na loop and not break
    global ghost_direc3
    
#ADDING THE GHSOT DIRECTIONS
    #ghost_direc = 1
    ghost_left_limit3 = 203#left
    ghost_right_limit3 = 480#rigt

#movign  the ghost left or right on repeat
    canvas.move(ghost3, ghost_direc3, 0)

#check the currunt x of the ghost
    gx, gy = canvas.coords(ghost3)

#swapping sides when moving
    if gx >= ghost_right_limit3:
        ghost_direc3 = -1
    elif gx <= ghost_left_limit3:
        ghost_direc3 = 1

#movign the ghost
    root.after(20, everyframe3)
everyframe3()

#---------------------------------------------------------#
#image oh ghost (4) (sideways)
OG_image4 = Image.open("Ghost_Pac.png")
REZ_image4 = OG_image3.resize ((40,39))
ghost_image4 = ImageTk.PhotoImage(REZ_image4)

#Adding ghe setting ghost image to "pacman"
ghost4 = canvas.create_image(72,337, image=ghost_image4)

#ADDING THE GHSOT DIRECTIONS 
ghost_direc4 = 1

def everyframe4():
#Helps keep it withi na loop and not break
    global ghost_direc4
    
#ADDING THE GHSOT DIRECTIONS
    #ghost_direc = 1
    ghost_left_limit4 = 72#left
    ghost_right_limit4 = 338#rigt

#movign  the ghost left or right on repeat
    canvas.move(ghost4, ghost_direc4, 0)

#check the currunt x of the ghost
    gx, gy = canvas.coords(ghost4)

#swapping sides when moving
    if gx >= ghost_right_limit4:
        ghost_direc4 = -1
    elif gx <= ghost_left_limit4:
        ghost_direc4 = 1

#movign the ghost
    root.after(20, everyframe4)
everyframe4()

#---------------------------------------------------------#
#image oh ghost (5) (sideways)
OG_image5 = Image.open("Ghost_Pac.png")
REZ_image5 = OG_image5.resize ((40,39))
ghost_image5 = ImageTk.PhotoImage(REZ_image5)

#Adding ghe setting ghost image to "pacman"
ghost5 = canvas.create_image(15,451, image=ghost_image5)

#ADDING THE GHSOT DIRECTIONS 
ghost_direc5 = 1

def everyframe5():
#Helps keep it within a loop and not break
    global ghost_direc5
    
#ADDING THE GHSOT DIRECTIONS
    #ghost_direc = 1
    ghost_left_limit5 = 15#left
    ghost_right_limit5 = 135#rigt

#moving the ghost left or right on repeat
    canvas.move(ghost5, ghost_direc5, 0)

#check the current x of the ghost
    gx, gy = canvas.coords(ghost5)

#swapping sides when moving
    if gx >= ghost_right_limit5:
        ghost_direc5 = -1
    elif gx <= ghost_left_limit5:
        ghost_direc5 = 1

#movign the ghost
    root.after(20, everyframe5)
everyframe5()

# Run the game loop
root.mainloop()

