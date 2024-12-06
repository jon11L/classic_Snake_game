import os
import json
import random, time, datetime


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

        self.BASE_SPEED = 500 # default speed when game starts
        self.MAX_SPEED = 50   # Minimum speed (maximum difficulty)

        self.game_version = None # initialize and track the game version

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

        # --- creating a restart button when game over ---
        self.restart_button = self.create_button("Restart", self.restart_game)

        # --- buttons to give in between the two different game's options 
        self.version_game_button_1 = self.create_button(
                                                    text="Version 1: Wall limitation / OFF.",
                                                    command=lambda: self.start_game_with_mode(1)
                                                    )
        self.version_game_button_1.place(relx=0.5, rely=0.45, anchor=CENTER)

        self.version_game_button_2 = self.create_button(
                                                    text="version 2: Wall limitation / ON. ",
                                                    command=lambda: self.start_game_with_mode(2)
                                                    )
        self.version_game_button_2.place(relx=0.5, rely=0.55, anchor=CENTER)

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
        # try:
            if not self.is_game_paused and self.is_game_over == False:
                print("Game paused.")
                self.is_game_paused = True
                self.pause_button.config(text="Resume")
                self.pause_time = time.time()
            else:
                print("Game resumed.")
                self.is_game_paused = False
                self.pause_button.config(text="Pause")
                self.start_time += time.time() - self.pause_time
                self.next_turn()
        # except Exception as e:
            # print(f"Game cannot be paused now.")
    

    def bind_keys(self):
        # set movement direction event
        self.window.bind('<Left>', lambda event: self.change_direction('left'))
        self.window.bind('<Right>', lambda event: self.change_direction('right'))
        self.window.bind('<Up>', lambda event: self.change_direction('up'))
        self.window.bind('<Down>', lambda event: self.change_direction('down'))


    def start_game_with_mode(self, version):
        """Start the game with selected mode"""
        self.game_version = version
        # Remove welcome screen
        self.version_game_button_1.place_forget()
        self.version_game_button_2.place_forget()

        # --- create a start button for the game to start ---
        self.start_button = self.create_button("Start", self.start_game)
        self.start_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    
    def initialise_game(self):
        ''' instantiate/reset game objects, like Food, Snake, the score and time'''
        self.screen_game.delete("all")
        self.snake = Snake(self) # Create a an instance of Snakes object
        self.food = Food(self) # Create a an instance of Food object
        self.direction = "right"
        self.is_game_over = False
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")

        self.start_time = time.time()
        # initialize the pause button on screen when the game starts.
        self.pause_button.grid(row=0, column=1)
        self.timer()


    def start_game(self):
        '''Remove the start button,
        call initialize_game() to initialize all objects for the game
        and call the next turn.
        '''
        self.start_button.place_forget()  # remove the 'start' button.
        self.initialise_game()
        print("Game starts!\n")

        self.next_turn() # first call to get the snake moving.


    def timer(self):
        '''Update the timer display, stops when game is over.'''
        if not self.is_game_over and not self.is_game_paused:
            self.game_time = time.time() - self.start_time
            self.formatted_time = time.strftime("%M:%S", time.gmtime(self.game_time))
            self.time_label.config(text=f"Time: {self.formatted_time}")
            self.window.after(100, self.timer)

    
    def next_turn(self):
        '''Move the snake in the current direction and check for collision,
            update the snake position on the canvas'''

        if self.is_game_paused:
            return
        
        # get the new validated direction from the snake
        next_direction = self.snake.send_direction()
        if next_direction:
            self.direction = next_direction

        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= self.SPACE_SIZE
        elif self.direction == "down":
            y += self.SPACE_SIZE
        elif self.direction == "left":
            x -= self.SPACE_SIZE
        elif self.direction == "right":
            x += self.SPACE_SIZE

        # if snake goes above the wall, it returns the opposite side
        if self.game_version == 1:
            if x < 0:
                x = self.GAME_WIDTH - self.SPACE_SIZE 
            elif x >= self.GAME_WIDTH:
                x = 0
        
            if y < 0:
                y = self.GAME_HEIGHT - self.SPACE_SIZE
            if y >= 500:
                y = 0

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

            # adjust the speed as the score increases.
            self.current_speed = max(self.MAX_SPEED, self.BASE_SPEED - (self.score * 5))

            self.window.after(self.current_speed, self.next_turn)
            self.timer()


    def check_collision(self):

        x, y = self.snake.coordinates[0]

        if self.game_version == 2:
        # --- wall collision is activated ---
            if x < 0 or x >= self.GAME_WIDTH:
                return True
            elif y < 0 or y >= self.GAME_HEIGHT:
                return True

        for body_part in self.snake.coordinates[1:]:
            if self.snake.coordinates[0] == body_part:
                return True

        return False


    def change_direction(self, new_direction):
        ''' send the new direction input to the snake queue direction for check validity'''
        self.snake.queue_direction(new_direction)



    def game_over(self):
        self.is_game_over = True
        print("\n", "-"*10, "Game over!", "-"*10)
        print(f"** score: {self.score} -- in {self.formatted_time}s **")
        self.pause_button.grid_remove()
        
        self.screen_game.create_text(self.screen_game.winfo_width()/2, self.screen_game.winfo_height()/2.5,
                            font=("consolas", 70),
                            text="Game Over",
                            fill="red",
                            tag="gameover",
                            )

        self.update_best_scores()
        self.show_top_score()

        # ---set the the restart button after a little delay---------------
        self.window.after(500, lambda: self.restart_button.place(relx=0.5, rely=0.75, anchor=CENTER))


    def load_best_scores(self, file_path="best_scores.json"):
        '''check if the best_scores file exists and load the top scores.
            If not it create the file
            '''

        print("\nSearching for Top-scores file.")
        if os.path.exists(file_path): # it will be in the current diretory
            with open(file_path, "r") as file:
                print("File found and loading.")
                # self.top_scores = json.load(file) # load the top scores from file
                return json.loads(file.read())
        else:
            # create file in the current directory
            with open(file_path, "w") as file:
                json.dump([], file)
            print("File missing or not found. --> file created with an empty list")
            return []
    

    def update_best_scores(self, file_path="best_scores.json"):
        '''check if the score is in the top 10.
        if so adds it to the list and remove the last one
        '''
        self.scores = self.load_best_scores(file_path)
        user = input("\nTo remember your score, enter your name : ").capitalize()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")  # Nicely formatted date

        # add the new score to the list
        self.scores.append({"user":user, "score":self.score, "time":self.formatted_time, "date":now}) # datetime.datetime()

        # sort the score list and keep the top 10
        self.scores = sorted(self.scores, key=lambda x: x["score"], reverse=True)[:10]

        # save the updated score list in the file
        print("Try updating the list.")
        with open(file_path, "w") as file:
            print("updating...")
            json.dump(self.scores, file, indent=4, separators=(',', ':'))
            print("updated...")


    def show_top_score(self): 
        '''Display the top3 scores.'''

        top_scores = self.scores[:3]
        print("\n --- Top 3 scores --- ")

        for i, item in enumerate(top_scores, start=1):
            print(f"{i}. {item['user']}: Score:{item['score']} -- time:{item['time']}s")
        print("-"*50)

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
        self.direction_queue = [] # Queue to handle rapid direction changes.

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


    def queue_direction(self, new_direction):
        '''add new direction to queue to check if move is valid'''
        if not self.direction_queue:
            current_direction =  self.game.direction
            print(current_direction) # debug purpose
        elif len(self.direction_queue) > 1:
            self.direction_queue.pop(1)
            current_direction = self.direction_queue[-1]
        else:
            current_direction = self.direction_queue[-1]

        # check if new direction is valid and not opposite to current direction.
        if ((new_direction == "left" and current_direction != "right") or
            (new_direction == "right" and current_direction != "left") or
            (new_direction == "up" and current_direction != "down") or
            (new_direction == "down" and current_direction!= "up")):

            # add the new direction to queue only if valid and if the queue is not 'full'
            if not self.direction_queue or (new_direction != current_direction and len(self.direction_queue) < 2):
                self.direction_queue.append(new_direction)
                print(self.direction_queue)  # debug purpose

    
    def send_direction(self):
        '''send the direction from the queue to the snake'''
        if self.direction_queue:
            return self.direction_queue.pop(0)
        else:
            return self.game.direction


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
    