import tkinter as tk
import random

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
MOVE_INTERVAL = 200  # milliseconds

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Colors
BG_COLOR = "blue"
SNAKE_COLOR = "pink"
FOOD_COLOR = "green"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.canvas.pack()

        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.food = self.generate_food()

        self.root.bind("<Up>", self.change_direction)
        self.root.bind("<Down>", self.change_direction)
        self.root.bind("<Left>", self.change_direction)
        self.root.bind("<Right>", self.change_direction)

        self.score = 0
        self.game_over = False

        self.update()

    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def change_direction(self, event):
        if event.keysym == "Up" and self.direction != DOWN:
            self.direction = UP
        elif event.keysym == "Down" and self.direction != UP:
            self.direction = DOWN
        elif event.keysym == "Left" and self.direction != RIGHT:
            self.direction = LEFT
        elif event.keysym == "Right" and self.direction != LEFT:
            self.direction = RIGHT

    def move(self):
        head = (
            (self.snake[0][0] + self.direction[0]) % GRID_WIDTH,
            (self.snake[0][1] + self.direction[1]) % GRID_HEIGHT,
        )

        if head == self.food:
            self.snake.insert(0, head)
            self.food = self.generate_food()
            self.score += 1
        else:
            self.snake.insert(0, head)
            self.snake.pop()

        if head in self.snake[1:]:
            self.game_over = True

    def draw(self):
        self.canvas.delete("all")

        for segment in self.snake:
            x1 = segment[0] * GRID_SIZE
            y1 = segment[1] * GRID_SIZE
            x2 = x1 + GRID_SIZE
            y2 = y1 + GRID_SIZE
            self.canvas.create_rectangle(
                x1, y1, x2, y2, outline="white", fill=SNAKE_COLOR
            )

        x1 = self.food[0] * GRID_SIZE
        y1 = self.food[1] * GRID_SIZE
        x2 = x1 + GRID_SIZE
        y2 = y1 + GRID_SIZE
        self.canvas.create_oval(
            x1, y1, x2, y2, outline="white", fill=FOOD_COLOR
        )

    def update(self):
        if not self.game_over:
            self.move()
            self.draw()
            self.root.after(MOVE_INTERVAL, self.update)
        else:
            self.canvas.create_text(
                WIDTH // 2,
                HEIGHT // 2,
                text=f"Game Over\nScore: {self.score}",
                fill="white",
                font=("Helvetica", 24),
                anchor="center",
            )

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
