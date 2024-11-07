import random, time

import tkinter as tk
from tkinter import ttk, Canvas
from tkinter.constants import *


class Game():
    def __init__(self):
        # --- initialize Constant elements. ---
        # screen dimension
        self.GAME_WIDTH = 500
        self.GAME_HEIGHT = 500
        # objects colors & sizes
        self.SNAKE_COLOR = "green"
        self.FOOD_COLOR = "darkred"
        self.BACKGROUND_COLOR = "black"
        self.SPACE_SIZE = 50
        self.BODY_SIZE = 3 # base size of snake's body

        self.BASE_SPEED = 300 # default speed when game starts
        self.MIN_SPEED = 50   # Minimum speed (maximum difficulty)


        # --- set up the all screen ---
        self.window = tk.Tk()
        self.window.title('Snake')
        self.window.resizable(False, False)
        
        # Use grid for better control of placement
        self.top_frame = ttk.Frame(self.window)
        self.top_frame.pack(fill='x') 
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=0)
        self.top_frame.grid_columnconfigure(2, weight=1)

        # --- Initialize score label ---
        self.score_label = tk.Label(self.top_frame, text=f"Score: 0", font=('consolas', 15))
        self.score_label.grid(row=0, column=0, sticky='e', padx=50)  # Align to the left with padding

        # --- Initialize time label ---
        self.time_label = tk.Label(self.top_frame, text=f"Time: 00:00", font=('consolas', 15))
        self.time_label.grid(row=0, column=2, sticky='w', padx=50)  # Align to the right with padding


        # --- pause button ---
        self.is_game_paused = False
        self.pause_button = tk.Button(self.top_frame, text=f"Pause", font=('consolas', 15),
                                    command=self.tooggle_pause,
                                    bg="lightblue",
                                    fg="blue",
                                    relief="groove")

        # --- screen game set up ---
        self.screen_game = Canvas(self.window, bg=self.BACKGROUND_COLOR, width=self.GAME_WIDTH, height=self.GAME_HEIGHT)
        self.screen_game.pack()
        
        # --- create a start button for the game to start ---
        self.start_button = self.create_button("Start", self.start_game)
        self.start_button.place(relx=0.5, rely=0.5, anchor=CENTER)

        # --- creating a restart button when game over ---
        self.restart_button = self.create_button("Restart", self.restart_game)

        # --- creating a exit button to quit the game ---  
        exit_button = ttk.Button(self.window,
                                text='Exit',
                                command=lambda: self.window.quit()
                                )
        exit_button.pack(side=tk.BOTTOM, pady=1, ipadx=1, ipady=5, expand=True, anchor="s")

        self.center_window()
        self.bind_keys()
        

    def create_button(self, text, command):
        return tk.Button(self.window, text=text, command=command,
                        font=('consolas', 15, 'bold'),
                        fg="blue", bg="lightblue",
                        padx=10, pady=10,
                        borderwidth=1,
                        relief=RAISED,
                        overrelief=GROOVE,
                        activebackground="lightgray",
                        )
    

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


    def tooggle_pause(self):
        if not self.is_game_paused and self.is_game_over == False:
            self.is_game_paused = True
            self.pause_button.config(text="Resume")
            self.pause_time = time.time()
        else:
            self.is_game_paused = False
            self.pause_button.config(text="Pause")
            self.start_time += time.time() - self.pause_time
            self.next_turn()  
    

    def bind_keys(self):
        # set movement direction event
        self.window.bind('<Left>', lambda event: self.change_direction('left'))
        self.window.bind('<Right>', lambda event: self.change_direction('right'))
        self.window.bind('<Up>', lambda event: self.change_direction('up'))
        self.window.bind('<Down>', lambda event: self.change_direction('down'))

    
    def initialise_game(self):
        ''' instantiate/reset game objects, like Food, Snake, the score and time'''
        self.screen_game.delete("all")
        self.snake = Snake(self)
        self.food = Food(self)
        self.direction = "right"
        self.is_game_over = False
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")

        self.start_time = time.time()
        self.timer()


    def start_game(self):
        # self.is_game_started = True
        self.start_button.place_forget()  # remove the 'start' button.
        self.initialise_game()
        print("Game starts!\n")

        # initialize the pause button on screen after the game starts.
        self.pause_button.grid(row=0, column=1)

        self.next_turn()


    def timer(self):
        '''Update the timer display, stops when game is over.'''
        if not self.is_game_over and not self.is_game_paused:
            self.game_time = time.time() - self.start_time
            self.formatted_time = time.strftime("%M:%S", time.gmtime(self.game_time))
            self.time_label.config(text=f"Time: {self.formatted_time}")
            self.window.after(100, self.timer)

    
    def next_turn(self):

        if self.is_game_paused:
            return
        
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

        # if collision it stops the game, otherwise goes to next turn.
        if self.check_collision():
            self.game_over()
        else:
            # create the new snake's head
            square = self.screen_game.create_rectangle(
                x, y,
                x + self.SPACE_SIZE, y + self.SPACE_SIZE,
                fill="lightgreen", outline="green", width=3,
                tag="snake"
                )
            
            # Update previous head to body appearance
            if len(self.snake.squares) > 0:
                self.screen_game.itemconfig(
                    self.snake.squares[0],
                    fill=self.SNAKE_COLOR,
                    width=2,
                    outline="lightgreen",
                    tag="snake"
                )
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

            # setting a speed that increases (update faster) as the score increases
            self.SPEED = max(self.MIN_SPEED, self.BASE_SPEED - (self.score * 2))

            self.window.after((self.SPEED - (self.score*2)), self.next_turn)
            self.timer()


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
        print(f"** best score: {self.score} -- in {self.formatted_time}s **")

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
        print("\nRestarting the game!\n")
        self.initialise_game()
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

        for i, (x, y) in enumerate(self.coordinates):
            if i == 0:
                # create the snake's head.
                square = game.screen_game.create_rectangle(
                    x, y, x + game.SPACE_SIZE, y + game.SPACE_SIZE,
                    fill="lightgreen", outline="green", width=3,
                    tag="snake"
                    )
            else:
                # create snake's body.
                square = game.screen_game.create_rectangle(
                    x, y, x + game.SPACE_SIZE, y + game.SPACE_SIZE,
                    fill="green", outline="lightgreen", width=1,
                    tag="snake"
                    )
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
        # create the food shape to be on the canvas
        game.screen_game.create_oval(x+5, y+5, x + game.SPACE_SIZE -5 , (y + game.SPACE_SIZE) -5, fill=game.FOOD_COLOR, outline="purple", width=3, tag="food")


if __name__ == '__main__':
    game = Game()
    game.window.mainloop()
