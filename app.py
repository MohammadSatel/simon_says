import tkinter as tk
import random
import time

# Define the colors and their corresponding buttons
COLORS = ["red", "blue", "green", "yellow"]

class SimonSaysGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Simon Says Game")

        # Initialize the game variables
        self.sequence = []
        self.user_sequence = []
        self.round = 0
        self.started = False
        self.game_over = False
        self.playing_sequence = False
        self.user_input_enabled = False

        # Create a frame to hold the color buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=0, column=0, padx=10, pady=10)

        # Create the buttons for each color and add them to the frame
        self.buttons = {}  # Store button objects in a dictionary
        for color in COLORS:
            button = tk.Button(button_frame, bg=color, width=10, height=5,
                               command=lambda c=color: self.check_sequence(c))
            button.grid(row=0, column=COLORS.index(color), padx=5, pady=5)
            button.config(state="disabled", bd=5)
            self.buttons[color] = button  # Store the button object

        # Create the Start button
        self.start_button = tk.Button(self.root, text="Start", width=30, height=2, command=self.start_game)
        self.start_button.grid(row=1, column=0, padx=5, pady=10)

        # Create a label to display the current round
        self.round_label = tk.Label(self.root, text="Round: 0", font=("Helvetica", 16))
        self.round_label.grid(row=2, column=0, padx=5, pady=10)

    def start_game(self):
        if not self.started or self.game_over:
            self.started = True
            self.round = 0
            self.game_over = False
            self.sequence = []
            self.user_sequence = []
            self.next_round()

    def next_round(self):
        self.sequence.append(random.choice(COLORS))
        self.user_sequence = []
        self.round += 1
        self.round_label.config(text=f"Round: {self.round}")
        self.play_sequence()

    def play_sequence(self):
        self.playing_sequence = True

        # Disable color buttons during playback
        for color in COLORS:
            button = self.buttons[color]
            button.config(state="disabled")
            self.root.update()

        self.root.after(1000, self.play_next_color, 0)

    def play_next_color(self, index):
        if index < len(self.sequence):
            color = self.sequence[index]
            button = self.buttons[color]
            button.config(relief="sunken", bg=color)
            self.root.update()
            self.root.after(1000, self.reset_color, button, index)
        else:
            # Enable color buttons for user input after sequence playback
            for color in COLORS:
                self.buttons[color].config(state="active", bg=color)
            self.user_input_enabled = True

    def reset_color(self, button, index):
        button.config(relief="raised")
        self.root.update()
        self.root.after(500, self.play_next_color, index + 1)

    def check_sequence(self, color):
        if self.started and not self.game_over and self.user_input_enabled:
            self.user_sequence.append(color)
            if self.user_sequence == self.sequence:
                if len(self.user_sequence) == len(self.sequence):
                    if len(self.user_sequence) == len(COLORS):
                        # User completed the sequence for this round
                        self.root.after(1000, self.next_round)  # Start next round after 1 second
            else:
                self.game_over = True
                self.round_label.config(text="Game Over!")
                self.reset_game()

    def reset_game(self):
        # Disable color buttons and reset game state
        for color in COLORS:
            self.buttons[color].config(state="disabled")
        self.user_input_enabled = False
        self.started = False

if __name__ == "__main__":
    root = tk.Tk()
    game = SimonSaysGame(root)
    root.mainloop()
