import random
import tkinter as tk

from tkinter import ttk, Canvas
from tkinter.constants import *

# ------------------------
# -- set up screen V
# -- set snake and apple objects   V
# -- set objects on the screen : apple and snake V
# -- set movement direction event
# -- grow size snake when eating an apple
# -- win event
# lost event
# start again 
# ------------------------------


# initialize elements.
# screen dimension
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
# objects colors
SNAKE_COLOR = "darkgreen"
FOOD_COLOR = "darkred"
BACKGROUND_COLOR = "black"

SPEED = 40
SPACE_SIZE = 40
BODY_SIZE = 3

score= 0

class Snake:

    def __init__(self):
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_SIZE):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)
            print(f"square is: {square}")
            print(f"self.squares are: {self.squares}")
        
        # return self.coordinates


class Food:
    def __init__(self):
        # food generate at a random place in the game
        x = random.randint(0, (WINDOW_WIDTH/SPACE_SIZE) - 1) * SPACE_SIZE	
        y = random.randint(0, (WINDOW_HEIGHT/SPACE_SIZE)- 1) * SPACE_SIZE

        self.coordinates = [x, y]
        # food shape
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    
    global score 

    x, y = snake.coordinates[0]

    print(snake.coordinates) # debugging purpose
    print(f"new headsnake coordinate \n {snake.coordinates[0]}") # debugging purpose
    
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR,)

    snake.squares.insert(0, square)

    del snake.coordinates[-1]

    canvas.delete(snake.squares[-1]) # should not happen when head snake == food coordinates.

    del snake.squares[-1]

    window.after(SPEED, next_turn, food, snake)

    print(f"food coord: {food.coordinates}") # debugging purpose
    if snake.coordinates[0] == food.coordinates: # and snake.coordinates[0[y]] == food.coordinates[1]:
        score += 1
        message.config(text=f"Score:{score}")

        # generate food at a different location
        canvas.delete("food")
        x = random.randint(0, (WINDOW_WIDTH/SPACE_SIZE) - 1) * SPACE_SIZE    
        y = random.randint(0, (WINDOW_HEIGHT/SPACE_SIZE)- 1) * SPACE_SIZE
        food.coordinates = [x, y]
        print(f"new food coord: {food.coordinates}") # debugging purpose
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def change_direction(new_direction):
    
    global direction

    if new_direction == 'left':
        if direction!= 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction!= 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction!= 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction!= 'up':
            direction = new_direction
    
    next_turn(snake, food)



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

# set movement direction event
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

direction = 'down'
snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()

