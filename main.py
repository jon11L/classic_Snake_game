import random
import tkinter as tk

from tkinter import ttk, Canvas
from tkinter.constants import *

# ------------------------
# -- set up screen
# -- set snake and apple objects
# - - set objects on the screen : apple and snake
#  - - set movement direction event
# -- grow size snake when eating an apple
# -- win event
# lost event
# start again 
# ------------------------------



# initialize elements.
SNAKE_COLOR = "red"
FOOD_COLOR = "green"
BACKGROUND_COLOR = "black"

score= 0

class Snake:
    X = 10
    Y = 10
    speed = 1

    def move_left(self):
        self.x = self.x + self.speed
        pass

    def move_right(self, x):
        pass

    def move_up(self, y):
        pass

    def move_down(self, y):
        pass

class Apple:
    x = 0
    y = 0
    size = 1
    
    position = random.randint(1, 800*600)

class Game():
    pass









# set up screen
window = tk.Tk()
window.title('Snake')
window.resizable(False, False)


# screen 
window_width = 600
window_height = 600


# get the screen dimension
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# center the window on the screen
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")



message = ttk.Label(window, text="Score:{}".format(score), font=('consolas', 15))
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


canvas = Canvas(window, bg=BACKGROUND_COLOR, width=window_width, height=window_height)
canvas.pack()





window.mainloop()