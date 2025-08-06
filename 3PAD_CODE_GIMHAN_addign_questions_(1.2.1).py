import os
import tkinter as tk
#import customtkinter
from tkinter import *
from PIL import Image, ImageTk
import tkinter.font as tkFont
import math
import fractions
import random
import pygame
import time
from tkinter import messagebox

#THIS CODE IS MADE BY GIMHAN DEERASINHA KANKANAMAGE
#(05/May/2025)
#The perpouse of this code is to create a fun math game, that will teach you math and have fun at the same time.



#Saving the data
data = []

#Creating the Main window

# Make the  window
window = tk.Tk()
window.title("Pac-Man Math Game")
# Set the size of the main window
window.geometry("650x650")

#Making Background for main

os.chdir(os.path.dirname(os.path.abspath(__file__)))
         
main_OG_image = Image.open("Pacman_window.png")
main_REZ_image = main_OG_image.resize ((650,650))
win_background_image = ImageTk.PhotoImage(main_REZ_image)

#Creat and place the image in near order
create_canvas_main = tk.Canvas(window, width=6500, height=650)
#fits the image and everytiem canvassie changes
create_canvas_main.pack(fill="both", expand=True)
create_canvas_main.create_image(0,0, image=win_background_image, anchor="nw")

#placew the background image
#background_label = tk.Label(window, image=win_background_image)
#background_label.place(x=0, y=0, relwidth=1, relheight=1)

#Finding the cordinates of he canvas
def get_coordinates(event):
    print(f"Mouse clicked at: {event.x}, {event.y}")

#chosign what mode the usar will use
def chose_mode():
    create_canvas_main.create_text(300, 240, text="Enter Login Username:", font=("fixedsys", 16), fill="white")
    username_entry = tk.Entry(window, font=("fixedsys", 14))
    #placing the suername and adding 5 pixel of padding (space) on the sides and top and bottom
    create_canvas_main.create_window(300, 290, window=username_entry)

    create_canvas_main.create_text(300, 340, text="Enter Login Password:", font=("fixedsys", 16), fill="white")
    login_password_entry = tk.Entry(window, font=("fixedsys", 14), show="*")
    #placing the suername and adding 5 pixel of padding (space) on the sides and top and bottom
    create_canvas_main.create_window(300, 390, window=login_password_entry)

    #tk.Label(window, text="Enter Username:").pack()
    #username_entry = Entry(window)
    #username_entry.pack()
    
    #wont let continue if there is an empty space
    def validate_username_info(username):
        return username.strip() != ""
    
    def validate_login_password_info():
        return login_password_entry.get().strip() != ""
    
#validate user entries
    def handle_submit(mode):
        username_text = username_entry.get().strip()
        password_text = login_password_entry.get().strip()

#check if the username has numbers innit
        if any(numb.isdigit() for numb in username_text):
            messagebox.showerror("INVALID USERNAME!","Please do not add numbers")
            return

        if any (numb.isalpha() for numb in password_text):
            messagebox.showerror("INVALID LOGIN PASSWORD!", "Please do not add letters")
            return
        
#checkign if the username excist in the txt file
        try:
            with open("data.txt","r") as file:
                found = False
                for line in file:
                    saved_username, saved_password, *_ = line.strip().split(",")
                    if saved_username == username_text and saved_password == password_text:
                        found = True
                        break
            if not found:
                messagebox.showerror("Login Failed", "Username of password does not match")
                return
        except FileNotFoundError:
            messagebox.showerror("Eroor","No user data found")
            return
        
#the speed of the ghost dependign o nthe dificulty                
        global ghost_speed
        if mode == "easy":
            ghost_speed = 1
        elif mode == "medium":
            ghost_speed = 1.3
        elif mode == "hard":
            ghost_speed = 1.6

        start_game(mode)

    #selecting the dificulty buttons
    #Selecting  dficluty heading
    create_canvas_main.create_text(300, 440, text="Select Difficulty:", font=("fixedsys", 16), fill="white")
    #buttosn for selecting the dificuly
    easy_button = tk.Button(window, text="Easy Mode", command=lambda: handle_submit("easy"), font=("fixedsys", 12), bg=("purple"),fg=("White"), width=20)#easy
    create_canvas_main.create_window(200, 490, window=easy_button)
    medium_button = tk.Button(window, text="Medium Mode", command=lambda: handle_submit("medium"),  font=("fixedsys", 12), bg=("purple"),fg=("White"),  width=20)#medium
    create_canvas_main.create_window(400, 490, window=medium_button)
    hard_button = tk.Button(window, text="Hard Mode", command=lambda: handle_submit("hard"),  font=("fixedsys", 12), bg=("purple"), fg=("White"), width=20)#hard
    create_canvas_main.create_window(300, 540, window=hard_button)

    #Adding a sigh up button on the cordner of the window(canvas)
    sign_up__button = tk.Button(window, text="Sign up", command=lambda: sign_up_window(),  font=("fixedsys", 12), bg=("purple"), fg=("White"), width=20)
    create_canvas_main.create_window(100,30, window=sign_up__button)
chose_mode()

def sign_up_window():
    # Make the sign up window
    sign_up_window = tk.Toplevel()
    sign_up_window.title("Pac-Man Math Game - Sign Up")
    sign_up_window.geometry("300x400")

    # Create and place the canvas
    create_canvas_sign = tk.Canvas(sign_up_window, width=300, height=400, bg="indigo")
    create_canvas_sign.pack(fill="both", expand=True)

    # Add sing up up username and password
    create_canvas_sign.create_text(150, 80, text="Enter Sign Up Username:", font=("fixedsys", 12), fill="white")
    sign_up_user_entry = tk.Entry(sign_up_window, font=("fixedsys", 10))
    create_canvas_sign.create_window(150, 110, window=sign_up_user_entry) 

    create_canvas_sign.create_text(150, 150, text="Enter Sign Up Password:", font=("fixedsys", 12), fill="white")
    sign_up__password_entry = tk.Entry(sign_up_window, font=("fixedsys", 10), show="*")
    create_canvas_sign.create_window(150, 180, window=sign_up__password_entry)  

    #savign the sign up info and validatign
    def validate_username(username):
        return username.strip() != ""

    def validate_password(password):
        return password.strip() != ""

        #Avoid making the same reciept number by storing
    generated_gamer_tag = set()

    # Function to generate a unique random 5-digit receipt number
    def generate_gamer_tag():
        while True:
            gamer_tag = str(random.randint(10000, 99999))
            if gamer_tag not in generated_gamer_tag:
                generated_gamer_tag.add(gamer_tag)
                return gamer_tag  
            
    gamer_tag = generate_gamer_tag()

    def save_sign_up_info():
        username = sign_up_user_entry.get().strip()
        password = sign_up__password_entry.get().strip()

        if not validate_username(username):
            messagebox.showwarning("Warning", "Please enter a valid username.")
            return

        if not validate_password(password):
            messagebox.showwarning("Warning", "Please enter a valid password.")
            return

        #Saving the data
        with open("data.txt", "a") as file:
            file.write(f"{username},{password},{gamer_tag}\n")
        messagebox.showinfo("Success",f"Account created successfully!/n Your GamerTag is: {gamer_tag}")
        sign_up_window.destroy()
    
    # Function to display data from the text file
    #def display_data():
        #try:
           # with open("data.txt", "r") as file:
              #  data = file.readlines()
          #  display_window = tk.Toplevel()
          #  display_window.title("Data Display")
          #  text = tk.Text(display_window)
         #   text.pack()
         #   for line in data:
          #      text.insert(tk.END, line)
       # except FileNotFoundError:
            #messagebox.showwarning("Warning", "No data file found")
                                   
    #submit button
    sign_up_submit_button = tk.Button(sign_up_window, text="Submit", command=lambda: save_sign_up_info(), font=("fixedsys", 12), bg="purple", fg="white", width=20)
    create_canvas_sign.create_window(150,250, window=sign_up_submit_button)



#THE MATHC QUESTIONS
#showign what typa math question there are 
#and how the 2 numbers combine to make the question
def make_easy_questiosn():
    BEDMAS = ['+', '-', '*', '/']
    first_numb = random.randint(1,100)
    second_numb = random. randint(1,50)
    BEDMAS_ques = random.choice(BEDMAS)

    if BEDMAS_ques =="+":
        correct = first_numb + second_numb
    elif BEDMAS_ques=='-':
        correct = first_numb - second_numb
    elif BEDMAS_ques =='*':
        correct = first_numb * second_numb
    elif BEDMAS_ques =='/':
        second_numb = random.randint(1,10)
        correct = round(first_numb / second_numb, 2)
        BEDMAS_ques = '/'

    question = f"{first_numb} {BEDMAS_ques} {second_numb} = ?"
    return question, correct

#Make the AREA question for medium mode

class area_question:
    def __init__(self):
        self.shapes = [
            {"base":6,"height":8, "image":"Tri 1.png", "type": "triangle"},
            {"base":4,"height":6, "image":"Tri 2.png", "type": "triangle"},
            {"base":9,"height":4, "image":"Tri 3.png", "type": "triangle"},
           #{"base":6,"height":8, "image":"Tri 4.png", "type": "triangle"},
           #{"base":6,"height":8, "image":"Tri 5.png", "type": "triangle"},
            {"base":5,"height":5, "image":"sq 1.png", "type": "square"},
           #{"base":5,"height":5, "image":"sq 2.png", "type": "square"},
           #{"base":5,"height":5, "image":"sq 3.png", "type": "square"},
            {"radius":5, "image":"ci 1.png", "type": "circle"},
           #{"radius":5, "image":"ci 2.png", "type": "circle"}
        ]
        self.shape = random.choice(self.shapes)
    
#Dispays the math questions
    def make_medium_question (self):
        if self.shape["type"] == "triangle":
            return "Find the area of the TRIANGLE", self.shape["image"]
        if self.shape["type"] == "square":
            return "Find the area of the SQUARE", self.shape["image"]
        else:
            return "Find the area of the CIRCLE", self.shape["image"]

#see if the math questiosn are correct
    def check_medium_answer (self, player_input):
        try:
            player_input_value = float(player_input)
            if self.shape["type"] == "triangle":
                correct = (self.shape['base'] * self.shape['height']) / 2
            if self.shape["type"] == "square":
                correct = (self.shape['base'] * self.shape['height'])
            else:
                correct = math.pi * (self.shape['radius'] **2)

            return abs(player_input_value - correct) <0.1, round(correct, 2)
        
        except:
            return False, None

#Maske the math questions for HARD Mode

class fraction_question:
    def __init__(self):
        self.one = random.randint(1,10)
        self.two = random.randint(1,10)
        self.three = random.randint(1,10)
        self.four = random.randint(1,10)

    def make_hard_question(self):
        return f"What is ({self.one}/{self.two}) + ({self.three}/{self.four})?"
    
    def check_hard_answer(self,player_input_value):
        try:
            correct = (self.one / self.two) + (self.three / self.four)
            player_value = float(player_input_value)
            return abs(player_value - correct) <0.05, round(correct, 2)
        except:
            return False, None
        
#GHOST COLLITON 
#When collided with the ghost the math questiosn show
 
#for mediuynm mode
# Define the flag globally
question_window_open = False

#for mediuynm mode
# Define the flag globally
question_window_open = False

#for mediuynm mode
def random_question_pop_up(mode, game_window, canvas, pacman):
    global question_window_open

    if question_window_open:
        return
    question_window_open = True

    correct_answer = None
    image_path = None

    if mode == "medium":
        question = area_question()
        question_text, image_path = question.make_medium_question()
    elif mode == "hard":
        question = fraction_question()
        question_text = question.make_hard_question()
        image_path = None
    else:
        question_text, correct_answer = make_easy_questiosn()
        question = None

    popup = tk.Toplevel(game_window)
    popup.title("Math Question")

    tk.Label(popup, text=question_text, font=("Arial", 14)).pack()

    if image_path:
        img = Image.open(image_path)
        img = img.resize((300, 300))
        img = ImageTk.PhotoImage(img)
        image_label = tk.Label(popup, image=img)
        image_label.image = img
        image_label.pack()

    entry = tk.Entry(popup)
    entry.pack()

    # Mode-based timeout
    if mode == "easy":
        timeout_ms = 15000
    elif mode == "medium":
        timeout_ms = 12000
    else:
        timeout_ms = 10000

    def auto_close():
        global question_window_open
        if popup.winfo_exists():
            popup.destroy()
            print("Time's up!")
            question_window_open = False
            schedule_next_popup()

    def check_answer():
        global question_window_open
        try:
            user_input = float(entry.get())
            if correct_answer is not None:
                if abs(user_input - correct_answer) < 0.05:
                    print("Correct")
                else:
                    print("Incorrect")
            else:
                print("Answer submitted (image mode)")
        except:
            print("Invalid input")
        popup.destroy()
        question_window_open = False
        schedule_next_popup()

    def submit():
        global question_window_open
        try:
            if mode == "easy":
                player_answer = float(entry.get())
                if abs(player_answer - correct_answer) < 0.1:
                    messagebox.showinfo("CORRECT!", "W's in the chat, you may continue.")
                else:
                    messagebox.showerror("INCORRECT!", f"Correct answer: {correct_answer}")
                    game_window.destroy()

            elif mode == "medium":
                correct, actual = question.check_medium_answer(entry.get())
                if correct:
                    messagebox.showinfo("CORRECT!", "W's in the chat, you may continue.")
                else:
                    messagebox.showerror("INCORRECT!", f"Answer was: {actual}")
                    game_window.destroy()

            elif mode == "hard":
                correct, actual = question.check_hard_answer(entry.get())
                if correct:
                    messagebox.showinfo("CORRECT!", "W's in the chat, you may continue.")
                else:
                    messagebox.showerror("WRONG!", f"Answer was: {actual}")
                    game_window.destroy()

            popup.destroy()
            question_window_open = False
            schedule_next_popup()

        except:
            messagebox.showerror("ERROR", "Enter a valid number")

    def schedule_next_popup():
        next_pop_up = random.randint(5000, 10000)
        game_window.after(next_pop_up, lambda: random_question_pop_up(mode, game_window, canvas, pacman))

    tk.Button(popup, text="Submit", command=submit).pack()

    popup.after(timeout_ms, auto_close)



    # timeout based on difficulty
    timeout = 15000 if mode == "easy" else 12000 if mode == "medium" else 10000

    def auto_close():
        global question_window_open
        if popup.winfo_exists():
            popup.destroy()
            messagebox.showinfo("TIME OUT!", "You ran out of time!")
            question_window_open = False

    popup.after(timeout, auto_close)

    # schedule next popup
    #next_pop_up = random.randint(5000, 10000)
    #game_window.after(next_pop_up, lambda: random_question_pop_up(mode, game_window, canvas, pacman))


    #so the ghots knwos to move
    
    #showing up the question at a random time
 #   next_pop_up = random.randint (5000, 10000)
 #   game_window.after (next_pop_up, lambda: random_question_pop_up(mode, game_window, canvas,pacman))


        

        
#ADDING THE GHSOT DIRECTIONS
ghost_direc1 = 1
ghost_direc2 = 1
ghost_direc3 = 1
ghost_direc4 = 1
ghost_direc5 = 1
#ghost_direc6 = 1
ghost_direc7 = 1
ghost_direc8 = 1

#Testing main window remvoed for reasons (Remove after the main window is done)

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

def start_game(mode):
    #chekc if the window for liek the game questions is flagged
   # shared_state = {"question_window_open": False}
  # NEW FLAG

 #Creating the main menue
# Initialize window
    game_window = tk.Toplevel()
    game_window.title("Pac-Man Math Game")

    #opop up the question
    #game_window.after (next_pop_up, lambda: random_question_pop_up(mode, game_window, canvas,pacman))
    

    global background_image, pacman_image
    global ghost_image1, ghost_image2, ghost_image3, ghost_image4
    global ghost_image5, ghost_image7, ghost_image8


#Making Background
    BG_OG_image = Image.open("Background_pacman.png")
    BG_REZ_image = BG_OG_image.resize ((600,500))
    background_image = ImageTk.PhotoImage(BG_REZ_image)

# Create Canvas
    canvas = tk.Canvas(game_window, width=600, height=550)
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

    #showing up the question at a random time
  #  next_pop_up = random.randint (5000, 10000)
  #  game_window.after (next_pop_up, lambda: random_question_pop_up(mode, game_window, canvas,pacman, shared_state))

    
    
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
    game_window.bind("<Left>", move_pacman)
    game_window.bind("<Right>", move_pacman)
    game_window.bind("<Up>", move_pacman)
    game_window.bind("<Down>", move_pacman)

#Creating the score keeper lable
    scoreLabel = Label(game_window, text =":Your Score:" ,font="fixedsys 20")
    scoreLabel.place(x=25, y=520)

#Update the score evry 1 second by adding one point
    def update_score():
#initialsing the score variable
        global score
        score += 1
        scoreLabel.config(text =f"Score:{score}")
        game_window.after(1000, update_score)

    update_score()

#Start adding the ghoststs
    #ghost_speed = 1

    #image oh ghost (1) (sideways)
    OG_image1 = Image.open("Ghost_Pac.png")
    REZ_image1 = OG_image1.resize ((39,39))
    ghost_image1 = ImageTk.PhotoImage(REZ_image1)

    #Adding ghe setting ghost image to "pacman"
    ghost1 = canvas.create_image(331,441, image=ghost_image1)

        
    #ADDING THE GHSOT DIRECTIONS
    #ghost_direc1 = 1

    def everyframe():
    #Helps keep it withi na loop and not break
        global ghost_direc1
        
    #ADDING THE GHSOT DIRECTIONS
        #ghost_direc = 1
        ghost_left_limit1 = 330#left
        ghost_right_limit1 = 560 #rigt

    #movign  the ghost left or right on repeat
        canvas.move(ghost1, ghost_direc1*ghost_speed, 0)

    #check the currunt x of the ghost
        gx, gy = canvas.coords(ghost1)

    #swapping sides when moving
        if gx >= ghost_right_limit1:
            ghost_direc1 = -1
        elif gx <= ghost_left_limit1:
            ghost_direc1 = 1

        #the cords for collide
            # Check collision with Pacman
        ghost_coords = canvas.coords(ghost1)  
        pacman_coords = canvas.coords(pacman)
        if abs(ghost_coords[0] - pacman_coords[0]) < 20 and abs(ghost_coords[1] - pacman_coords[1]) < 20:
            messagebox.showerror("GAME OVER", "You touched a ghost!")
            game_window.destroy()
            return
        

    # schedule next popup
        #next_pop_up = random.randint(5000, 10000)
        #game_window.after(next_pop_up, lambda: random_question_pop_up(mode, game_window, canvas, pacman))
        #movign the ghost
        #movign the ghost
        game_window.after(20, everyframe2)

    game_window.after(100, everyframe)

    #everyframe()
        #game_window.after(100, everyframe)

    

    
    

    #---------------------------------------------------------#
    
    #image oh ghost (2) (sideways)
    OG_image2 = Image.open("Ghost_Pac.png")
    REZ_image2 = OG_image2.resize ((40,39))
    ghost_image2 = ImageTk.PhotoImage(REZ_image2)

    #Adding ghe setting ghost image to "pacman"
    ghost2 = canvas.create_image(43,171, image=ghost_image2)

        
    #ADDING THE GHSOT DIRECTIONS
    #ghost_direc2 = 1

    def everyframe2():
    #Helps keep it withi na loop and not break
        global ghost_direc2
        
    #ADDING THE GHSOT DIRECTIONS
        #ghost_direc = 1
        ghost_left_limit2 = 43#left
        ghost_right_limit2 = 168 #rigt

    #movign  the ghost left or right on repeat
        canvas.move(ghost2, ghost_direc2*ghost_speed, 0)

    #check the currunt x of the ghost
        gx, gy = canvas.coords(ghost2)

    #swapping sides when moving
        if gx >= ghost_right_limit2:
            ghost_direc2 = -1
        elif gx <= ghost_left_limit2:
            ghost_direc2 = 1

    #movign the ghost
        #the cords for collide
            # Check collision with Pacman
        ghost_coords = canvas.coords(ghost2)  
        pacman_coords = canvas.coords(pacman)
        if abs(ghost_coords[0] - pacman_coords[0]) < 20 and abs(ghost_coords[1] - pacman_coords[1]) < 20:
            messagebox.showerror("GAME OVER", "You touched a ghost!")
            game_window.destroy()
            return
        
    #movign the ghost
        game_window.after(20, everyframe2)
    
    #everyframe()
    game_window.after(100, everyframe2)
    #opop up the question
    #game_window.after (next_pop_up, lambda: random_question_pop_up(mode, game_window, canvas,pacman))



    #---------------------------------------------------------#
    #image oh ghost (3) (sideways)
    OG_image3 = Image.open("Ghost_Pac.png")
    REZ_image3 = OG_image3.resize ((40,39))
    ghost_image3 = ImageTk.PhotoImage(REZ_image3)

    #Adding ghe setting ghost image to "pacman"
    ghost3 = canvas.create_image(203,115, image=ghost_image3)

    #ADDING THE GHSOT DIRECTIONS 
    #ghost_direc3 = 1

    def everyframe3():
    #Helps keep it withi na loop and not break
        global ghost_direc3
        
    #ADDING THE GHSOT DIRECTIONS
        #ghost_direc = 1
        ghost_left_limit3 = 203#left
        ghost_right_limit3 = 480#rigt

    #movign  the ghost left or right on repeat
        canvas.move(ghost3, ghost_direc3*ghost_speed, 0)

    #check the currunt x of the ghost
        gx, gy = canvas.coords(ghost3)

    #swapping sides when moving
        if gx >= ghost_right_limit3:
            ghost_direc3 = -1
        elif gx <= ghost_left_limit3:
            ghost_direc3 = 1

    #movign the ghost
                    # Check collision with Pacman
        ghost_coords = canvas.coords(ghost3)  
        pacman_coords = canvas.coords(pacman)
        if abs(ghost_coords[0] - pacman_coords[0]) < 20 and abs(ghost_coords[1] - pacman_coords[1]) < 20:
            messagebox.showerror("GAME OVER", "You touched a ghost!")
            game_window.destroy()
            return
        
    #movign the ghost
        game_window.after(20, everyframe3)
    
    #everyframe()
    game_window.after(100, everyframe3)

    #opop up the question
    #game_window.after (next_pop_up, lambda: random_question_pop_up(mode, game_window, canvas,pacman))



    #---------------------------------------------------------#
    #image oh ghost (4) (sideways)
    OG_image4 = Image.open("Ghost_Pac.png")
    REZ_image4 = OG_image3.resize ((40,39))
    ghost_image4 = ImageTk.PhotoImage(REZ_image4)

    #Adding ghe setting ghost image to "pacman"
    ghost4 = canvas.create_image(72,337, image=ghost_image4)

    #ADDING THE GHSOT DIRECTIONS 
    #ghost_direc4 = 1

    def everyframe4():
    #Helps keep it withi na loop and not break
        global ghost_direc4
        
    #ADDING THE GHSOT DIRECTIONS
        #ghost_direc = 1
        ghost_left_limit4 = 72#left
        ghost_right_limit4 = 338#rigt

    #movign  the ghost left or right on repeat
        canvas.move(ghost4, ghost_direc4*ghost_speed, 0)

    #check the currunt x of the ghost
        gx, gy = canvas.coords(ghost4)

    #swapping sides when moving
        if gx >= ghost_right_limit4:
            ghost_direc4 = -1
        elif gx <= ghost_left_limit4:
            ghost_direc4 = 1

    #movign the ghost
            # Check collision with Pacman
        ghost_coords = canvas.coords(ghost4)  
        pacman_coords = canvas.coords(pacman)
        if abs(ghost_coords[0] - pacman_coords[0]) < 20 and abs(ghost_coords[1] - pacman_coords[1]) < 20:
            messagebox.showerror("GAME OVER", "You touched a ghost!")
            game_window.destroy()
            return
        
    #movign the ghost
        game_window.after(20, everyframe4)
    
    #everyframe()
    game_window.after(100, everyframe4)

    #opop up the question
    #game_window.after (next_pop_up, lambda: random_question_pop_up(mode, game_window, canvas,pacman))



    #---------------------------------------------------------#
    #image oh ghost (5) (sideways)
    OG_image5 = Image.open("Ghost_Pac.png")
    REZ_image5 = OG_image5.resize ((40,39))
    ghost_image5 = ImageTk.PhotoImage(REZ_image5)

    #Adding ghe setting ghost image to "pacman"
    ghost5 = canvas.create_image(15,451, image=ghost_image5)

    #ADDING THE GHSOT DIRECTIONS 
    #ghost_direc5 = 1

    def everyframe5():
    #Helps keep it within a loop and not break
        global ghost_direc5
        
    #ADDING THE GHSOT DIRECTIONS
        #ghost_direc = 1
        ghost_left_limit5 = 15#left
        ghost_right_limit5 = 135#rigt

    #moving the ghost left or right on repeat
        canvas.move(ghost5, ghost_direc5*ghost_speed, 0)

    #check the current x of the ghost
        gx, gy = canvas.coords(ghost5)

    #swapping sides when moving
        if gx >= ghost_right_limit5:
            ghost_direc5 = -1
        elif gx <= ghost_left_limit5:
            ghost_direc5 = 1

    #movign the ghost
             # Check collision with Pacman
        ghost_coords = canvas.coords(ghost5)  
        pacman_coords = canvas.coords(pacman)
        if abs(ghost_coords[0] - pacman_coords[0]) < 20 and abs(ghost_coords[1] - pacman_coords[1]) < 20:
            messagebox.showerror("GAME OVER", "You touched a ghost!")
            game_window.destroy()
            return
        
    #movign the ghost
        game_window.after(20, everyframe5)
    
    #everyframe()
    game_window.after(100, everyframe5)

    #opop up the question
    #game_window.after (next_pop_up, lambda: random_question_pop_up(mode, game_window, canvas,pacman))



    #---------------------------------------------------------#
    #image oh ghost (7) (sideways) (6 was removed due to accidental error)
    OG_image7 = Image.open("Ghost_Pac.png")
    REZ_image7 = OG_image7.resize ((40,39))
    ghost_image7 = ImageTk.PhotoImage(REZ_image7)

    #Adding ghe setting ghost image to "pacman"
    ghost7 = canvas.create_image(300,227, image=ghost_image7)

    #ADDING THE GHSOT DIRECTIONS 
    #ghost_direc7 = 1

    def everyframe7():
    #Helps keep it withi na loop and not break
        global ghost_direc7
        
    #ADDING THE GHSOT DIRECTIONS
        #ghost_direc = 1
        ghost_left_limit7 = 305#left
        ghost_right_limit7 = 527#rigt

    #movign  the ghost left or right on repeat
        canvas.move(ghost7, ghost_direc7*ghost_speed, 0)

    #check the currunt x of the ghost
        gx, gy = canvas.coords(ghost7)

    #swapping sides when moving
        if gx >= ghost_right_limit7:
            ghost_direc7 = -1
        elif gx <= ghost_left_limit7:
            ghost_direc7 = 1

    #movign the ghost
             # Check collision with Pacman
        ghost_coords = canvas.coords(ghost7)  
        pacman_coords = canvas.coords(pacman)
        if abs(ghost_coords[0] - pacman_coords[0]) < 20 and abs(ghost_coords[1] - pacman_coords[1]) < 20:
            messagebox.showerror("GAME OVER", "You touched a ghost!")
            game_window.destroy()
            return
        
    #movign the ghost
        game_window.after(20, everyframe7)
    
    #everyframe()
    game_window.after(100, everyframe7)
    #opop up the question
    #game_window.after (next_pop_up, lambda: random_question_pop_up(mode, game_window, canvas,pacman))
        


    #---------------------------------------------------------#
    #image oh ghost (8) (UP/DOWN)
    OG_image8 = Image.open("Ghost_Pac.png")
    REZ_image8 = OG_image8.resize ((40,39))
    ghost_image8 = ImageTk.PhotoImage(REZ_image8)

    #Adding ghe setting ghost image to "pacman"
    ghost8 = canvas.create_image(400,170, image=ghost_image8)

    #ADDING THE GHSOT DIRECTIONS 
    #ghost_direc8 = 1

    def everyframe8():
    #Helps keep it within a loop and not break
        global ghost_direc8
        
    #ADDING THE GHSOT DIRECTIONS
        #ghost_direc = 1
        ghost_up_limit8 = 400#up
        ghost_down_limit8 = 339#down

    #moving the ghost left or right on repeat
        canvas.move(ghost8, 0, ghost_direc8*ghost_speed)

    #check the current x of the ghost
        gx, gy = canvas.coords(ghost8)

    #swapping sides when moving
        if gy >= ghost_up_limit8:
            ghost_direc8 = -1
        elif gy <= ghost_down_limit8:
            ghost_direc8 = 1

    #movign the ghost
             # Check collision with Pacman
        ghost_coords = canvas.coords(ghost8)  
        pacman_coords = canvas.coords(pacman)
        if abs(ghost_coords[0] - pacman_coords[0]) < 20 and abs(ghost_coords[1] - pacman_coords[1]) < 20:
            messagebox.showerror("GAME OVER", "You touched a ghost!")
            game_window.destroy()
            return
        
    #movign the ghost
        game_window.after(20, everyframe8)
    
    #everyframe()
    game_window.after(100, everyframe8)
    #game_window.after (next_pop_up, lambda: random_question_pop_up(mode, game_window, canvas,pacman))



    


#---------------------------------------------------------#
#image oh ghost (9) (UP/DOWN)
#OG_image9 = Image.open("Ghost_Pac.png")
#REZ_image9 = OG_image9.resize ((40,39))
#ghost_image9 = ImageTk.PhotoImage(REZ_image9)

#Adding ghe setting ghost image to "pacman"
#ghost9 = canvas.create_image(520,273, image=ghost_image9)

#ADDING THE GHSOT DIRECTIONS 
#ghost_direc9 = 1

#def everyframe9():
#Helps keep it within a loop and not break
    #global ghost_direc9
    
#ADDING THE GHSOT DIRECTIONS
    #ghost_direc = 1
    #ghost_up_limit9 = 521
    #ghost_down_limit9 = 338
    #buffer = 3

#moving the ghost left or right on repeat
   # # Move up/down by 2 pixels per loop
   # canvas.move(ghost9, 0, ghost_direc9)

#check the current x of the ghost
   # gx, gy = canvas.coords(ghost9)

#swapping sides when moving
   # if gy >= ghost_down_limit9:
     # ghost_direc9 = -1  # go up
   # elif gy <= ghost_up_limit9:
       #ghost_direc9 = 1   # go down 1

#movign the ghost
   # root.after(20, everyframe9)
#everyframe9()
    # Run the game loop
    #game_window.mainloop()
# End of your script
window.mainloop()
#rusn the game
#start_game()



