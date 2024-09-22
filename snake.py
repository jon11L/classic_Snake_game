import random
import tkinter as tk
# from tkinter import *

from tkinter import ttk
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



# initialize 

snake_color = "red"
food_color = "green"
background_color = "black"


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
root = tk.Tk()
root.title('Snake')
root.resizable(False, False)


# screen 
window_width = 800
window_height = 600


# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# center the window on the screen
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)


# start the window application



root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

message = ttk.Label(root, text="Start the game.").pack()
# message.pack()

# exit button
exit_button = ttk.Button(
    root,
    text='Exit',
    command=lambda: root.quit()
)

exit_button.pack(
    ipadx=1,
    ipady=1,
    expand=True
)


root.mainloop()