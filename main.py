import random, time
import tkinter as tk

from tkinter import ttk, Canvas
from tkinter.constants import *
# from tkinter import messagebox

# ------------------------
# -- set up screen V
# -- set snake and apple objects   V
# -- set objects on the screen : apple and snake V
# -- set movement direction event V
# - wall limit and collision detection V
# -- grow size snake when eating an apple V
# -- win event
# lost event
# start again 
# time
# -----------------------------

# --- initialize elements. ---
# screen dimension
GAME_WIDTH= 600
GAME_HEIGHT = 600
# objects colors
SNAKE_COLOR = "darkgreen"
FOOD_COLOR = "darkred"
BACKGROUND_COLOR = "black"

SPEED = 120
SPACE_SIZE = 50
BODY_SIZE = 3

score= 0

class Snake:
    def __init__(self):
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []

        start_x = 150

        for i in range(0, BODY_SIZE):
            self.coordinates.append([start_x -(i * SPACE_SIZE), 0])
            print(self.coordinates)

        for x, y in self.coordinates:
            square = screen_game.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        # food generate at a random place in an empty space
        while True:
            x = random.randint(0, (GAME_WIDTH/SPACE_SIZE) - 1) * SPACE_SIZE	
            y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE)- 1) * SPACE_SIZE

            if [x, y] not in snake.coordinates:
                break

        self.coordinates = [x, y]
        # food shape
        screen_game.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake: Snake, food: Food):
    
    global score 

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])

    if check_collision(snake):
        game_over()

    else:    
        square = screen_game.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR,)
        snake.squares.insert(0, square)

        # check if the snake ate the food.
        if snake.coordinates[0] == food.coordinates:
            score += 1
            score_label.config(text=f"Score:{score}")

            # generate food at a different location
            screen_game.delete("food")
            food = Food()     
        else:
            del snake.coordinates[-1]
            screen_game.delete(snake.squares[-1])
            del snake.squares[-1]

        # if collision it stops the game, otherwise goes to next turn.
        window.after(SPEED, next_turn, snake, food)


def check_collision(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if snake.coordinates[0] == body_part:
            return True
        
    return False


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


def game_over():
    print("Game over!")
    screen_game.create_text(screen_game.winfo_width()/2, screen_game.winfo_height()/2,
                        font=("consolas", 60),
                        text="Game Over",
                        fill="red",
                        tag="gameover",
                        )
    

def start_game():
    start_button.place_forget()  # Hide the start button
    next_turn(snake, food)
    


direction = 'right'

# set up the all screen
window = tk.Tk()
window.title('Snake')
window.resizable(False, False)


# display the score.
score_label = ttk.Label(window, text=f"Score:{score}", font=('consolas', 20))
# score_label.pack()
score_label.pack() # anchor='nw', padx=10, pady=10

# screen gaame set up
screen_game = Canvas(window, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
screen_game.pack()


start_button = tk.Button(window, text="Start", command=start_game,
                        font=('consolas', 15, 'bold'),
                        fg="blue",
                        bg="lightblue",
                        padx=10, pady=10,
                        borderwidth=1,
                        relief=RAISED,
                        overrelief=GROOVE,
                        activebackground="lightgray",
                        )
start_button.place(relx=0.5, rely=0.5, anchor=CENTER)


exit_button = ttk.Button(
    window,
    text='Exit',
    command=lambda: window.quit()
)
exit_button.pack(side=tk.BOTTOM, pady=1, ipadx=1, ipady=1, expand=True)


window.update()

# get the screen dimension
window_width = window.winfo_width() 
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# center the window on the screen
center_x = int((screen_width/2) - (window_width/2))
center_y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# set movement direction event
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

# next_turn(snake, food)

window.mainloop()
