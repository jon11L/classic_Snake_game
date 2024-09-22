import random
import tkinter as tk

from tkinter import ttk, Canvas
from tkinter.constants import *

# ------------------------
# -- set up screen V
# -- set snake and apple objects   V
# - - set objects on the screen : apple and snake V
#  - - set movement direction event
# -- grow size snake when eating an apple
# -- win event
# lost event
# start again 
# ------------------------------


# initialize elements.
# screen 
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
#color  objects
SNAKE_COLOR = "darkgreen"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"

SPEED = 40
SPACE_SIZE = 40
BODY_SIZE = 4

score= 0

class Snake:
    X = 10
    Y = 10
    speed = 1

    def __init__(self):
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_SIZE):
            self.coordinates.append([300,300])

        for x, y in self.coordinates:
            sqare = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(sqare)
            print(f"square is: {sqare}")
            print(f"self.squares are: {self.squares}")


    

class Food:
    def __init__(self):
        # food generate at a random place in the game
        x = random.randint(0, (WINDOW_WIDTH/SPACE_SIZE) - 1) * SPACE_SIZE
        print(f"size of food is {WINDOW_WIDTH/SPACE_SIZE}")	
        y = random.randint(0, (WINDOW_HEIGHT/SPACE_SIZE)- 1) * SPACE_SIZE

        self.coordinates = [x, y]

        # food shape
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")




def next_turn(snake, food):
    
    x,y = Snake.coordinates[0]

    if direction == "up": # type: ignore
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    
    # snake.coordinates.insert(0,  (x,y))

    
    window.after(SPEED, next_turn, food, snake)





    # def move_left(self):
    #     self.x = self.x + self.speed
    #     pass

    # def move_right(self, x):
    #     pass

    # def move_up(self, y):
    #     pass

    # def move_down(self, y):
    #     pass





# set up screen
window = tk.Tk()
window.title('Snake')
window.resizable(False, False)

# get the screen dimension
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# center the window on the screen
center_x = int(screen_width/2 - WINDOW_WIDTH / 2)
center_y = int(screen_height/2 - WINDOW_HEIGHT / 2)
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}")

message = ttk.Label(window, text=f"Score:{score}", font=('consolas', 20))
message.pack()

# exit button
button_frame = ttk.Frame(window)
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

exit_button = ttk.Button(
    button_frame,
    text='Exit',
    command=lambda: window.quit()
)

exit_button.pack(ipadx=1, ipady=1, expand=True)


canvas = Canvas(window, bg=BACKGROUND_COLOR, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

snake = Snake()
food = Food()

window.mainloop()