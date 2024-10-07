import random, time

import tkinter as tk
from tkinter import ttk, Canvas
from tkinter.constants import *

# ------------------------
# -- set up screen V
# -- set snake and apple objects   V
# -- set objects on the screen : apple and snake V
# -- set movement direction event V
# - wall limit and collision detection V
# -- grow size snake when eating an apple V
# -- win event
# lost event V
# start again V
# time
# -----------------------------

class Game():
    def __init__(self):
        # --- initialize elements. ---
        # screen dimension
        self.GAME_WIDTH = 600
        self.GAME_HEIGHT = 600
        # objects colors
        self.SNAKE_COLOR = "darkgreen"
        self.FOOD_COLOR = "darkred"
        self.BACKGROUND_COLOR = "black"

        self.SPEED = 120
        self.SPACE_SIZE = 50
        self.BODY_SIZE = 3

        self.score = 0
        self.direction = "right"
        self.start_time = 0
        self.game_time = 0

        # use to check if games end, to stop the timer
        self.is_game_over = False

        # set up the all screen
        self.window = tk.Tk()
        self.window.title('Snake')
        self.window.resizable(False, False)
        

        # Use grid for better control of placement
        self.top_frame = ttk.Frame(self.window)
        self.top_frame.pack(fill='x') 

        # Initialize score label
        self.score_label = tk.Label(self.top_frame, text=f"Score: {self.score}", font=('consolas', 20))
        self.score_label.grid(row=0, column=0, sticky='e', padx=50)  # Align to the left with padding

        # Initialize time label
        self.time_label = tk.Label(self.top_frame, text=f"Time: 00:00", font=('consolas', 20))
        self.time_label.grid(row=0, column=1, sticky='w', padx=50)  # Align to the right with padding

        # Configure the frame to make sure the time is on the right
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)


        # screen game set up
        self.screen_game = Canvas(self.window, bg=self.BACKGROUND_COLOR, width=self.GAME_WIDTH, height=self.GAME_HEIGHT)
        self.screen_game.pack()
        

        # create a start button to click, in the window before the game starts
        self.start_button = tk.Button(self.window, text="Start", command=self.start_game,
                                font=('consolas', 15, 'bold'),
                                fg="blue",
                                bg="lightblue",
                                padx=10, pady=10,
                                borderwidth=1,
                                relief=RAISED,
                                overrelief=GROOVE,
                                activebackground="lightgray",
                                )
        self.start_button.place(relx=0.5, rely=0.5, anchor=CENTER)


        # --- creating a restart button when game over---------------
        self.restart_button = tk.Button(self.window, text="Play again", command= self.restart_game,
                                font=('consolas', 15, 'bold'),
                                fg="blue",
                                bg="lightblue",
                                padx=10, pady=10,
                                borderwidth=1,
                                relief=RAISED,
                                overrelief=GROOVE,
                                activebackground="lightgray",
                                )


        exit_button = ttk.Button(self.window,
                                text='Exit',
                                command=lambda: self.window.quit()
                                )
        exit_button.pack(side=tk.BOTTOM, pady=1, ipadx=1, ipady=1, expand=True)

        self.center_window()
        self.bind_keys()

        self.snake = None
        self.food = None


    def center_window(self):
        self.window.update()

        # get the screen dimension
        window_width = self.window.winfo_width() 
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # center the window on the screen
        center_x = int((screen_width/2) - (window_width/2))
        center_y = int((screen_height/2) - (window_height/2))
        self.window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")


    def bind_keys(self):
        # set movement direction event
        self.window.bind('<Left>', lambda event: self.change_direction('left'))
        self.window.bind('<Right>', lambda event: self.change_direction('right'))
        self.window.bind('<Up>', lambda event: self.change_direction('up'))
        self.window.bind('<Down>', lambda event: self.change_direction('down'))


    def start_game(self):
        ''' instantiate game objects, such like the Food, Snake object, the score and time'''
        self.start_button.place_forget()  # Hide the start button
        self.snake = Snake(self)
        self.food = Food(self)
        self.is_game_over = False
        self.start_time = time.time()
        self.update_timer()
        self.next_turn()


    def update_timer(self):
        '''Update the timer display, stops when game is over.'''
        if not self.is_game_over:
            self.game_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(self.game_time, 60)
            self.time_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
            self.window.after(1000, self.update_timer)

    
    def next_turn(self):

        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= self.SPACE_SIZE
        elif self.direction == "down":
            y += self.SPACE_SIZE
        elif self.direction == "left":
            x -= self.SPACE_SIZE
        elif self.direction == "right":
            x += self.SPACE_SIZE

        self.snake.coordinates.insert(0, [x, y])

        if self.check_collision():
            self.game_over()

        else:    
            square = self.screen_game.create_rectangle(x, y, x + self.SPACE_SIZE, y + self.SPACE_SIZE, fill=self.SNAKE_COLOR,)
            self.snake.squares.insert(0, square)

            # check if the snake ate the food.
            if self.snake.coordinates[0] == self.food.coordinates:
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                # generate food at a different location
                self.screen_game.delete("food")
                self.food = Food(self)     
            else:
                del self.snake.coordinates[-1]
                self.screen_game.delete(self.snake.squares[-1])
                del self.snake.squares[-1]

            # if collision it stops the game, otherwise goes to next turn.
            self.window.after(self.SPEED, self.next_turn)
            self.update_timer()


    def check_collision(self):

        x, y = self.snake.coordinates[0]

        if x < 0 or x >= self.GAME_WIDTH:
            return True
        elif y < 0 or y >= self.GAME_HEIGHT:
            return True

        for body_part in self.snake.coordinates[1:]:
            if self.snake.coordinates[0] == body_part:
                return True

        return False
    

    def change_direction(self, new_direction):

        if new_direction == 'left' and self.direction!= 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction!= 'left':
            self.direction = new_direction
        elif new_direction == 'up' and self.direction!= 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction!= 'up':
            self.direction = new_direction


    def game_over(self):
        self.is_game_over = True
        print("Game over!")
        self.screen_game.create_text(self.screen_game.winfo_width()/2, self.screen_game.winfo_height()/2.5,
                            font=("consolas", 80),
                            text="Game Over",
                            fill="red",
                            tag="gameover",
                            )

        # ---set the the restart button after a little delay---------------
        self.window.after(500, lambda: self.restart_button.place(relx=0.5, rely=0.75, anchor=CENTER))


    def restart_game(self):
        self.restart_button.place_forget()
        self.screen_game.delete("all")
        print("Restarting the game!")

        # reset timer
        self.start_time = time.time()
        self.is_game_over = False

        # Reset score
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")


        # reset direction
        self.direction = "right"

        # Recreate the snake and food instances
        self.snake = Snake(self)
        self.food = Food(self)

        self.update_timer()
        self.next_turn()


class Snake:
    def __init__(self, game):
        self.game = game
        self.body_size = game.BODY_SIZE
        self.coordinates = []
        self.squares = []

        start_x = 150

        for i in range(0, self.body_size):
            self.coordinates.append([start_x -(i * game.SPACE_SIZE), 0])
            print(self.coordinates)

        for x, y in self.coordinates:
            square = game.screen_game.create_rectangle(x, y, x + game.SPACE_SIZE, y + game.SPACE_SIZE, fill=game.SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self, game):
        self.game = game

        # food generate at a random place in an empty space
        while True:
            x = random.randint(0, (game.GAME_WIDTH/game.SPACE_SIZE) - 1) * game.SPACE_SIZE	
            y = random.randint(0, (game.GAME_HEIGHT/game.SPACE_SIZE)- 1) * game.SPACE_SIZE

            if [x, y] not in game.snake.coordinates:
                break

        self.coordinates = [x, y]
        # food shape
        game.screen_game.create_oval(x, y, x + game.SPACE_SIZE, y + game.SPACE_SIZE, fill=game.FOOD_COLOR, tag="food")


if __name__ == '__main__':
    game = Game()
    game.window.mainloop()