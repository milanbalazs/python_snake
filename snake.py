from random import randrange
import math

try:
    import Tkinter as tk  # noqa: N813
    from Tkinter import messagebox
except ImportError:
    import tkinter as tk
    from tkinter import messagebox


class SnakeItself:
    elements = []

    @classmethod
    def add_element(cls, x_pos, y_pos, direction):
        SnakeItself.elements.append({"X": x_pos, "Y": y_pos, "D": direction})

    @classmethod
    def get_elements(cls):
        return SnakeItself.elements

    @classmethod
    def get_last_direction(cls):
        return SnakeItself.elements[-1]["D"]

    @classmethod
    def clear_all_data(cls):
        SnakeItself.elements = []

    @classmethod
    def get_all_coords(cls):
        return [(x["X"], x["Y"]) for x in SnakeItself.elements]

    @classmethod
    def get_score(cls):
        return len(SnakeItself.elements) - 1


class SnakeConfig(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("200x200")
        self.create_elements()
        self.top_level = None

    def create_elements(self):
        start_button = tk.Button(self, text="START", command=self.start_game)
        start_button.pack()

    def start_game(self):
        self.top_level = SnakeGame(width=400, height=300)


class SnakeGame(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.geometry("{}x{}".format(kwargs["width"], kwargs["height"]))
        self.snake_canvas = SnakeCanvas(
            self, width=kwargs["width"] - 100, height=kwargs["height"], bg="CadetBlue1",
        )
        tk.Label(self, text="SCORE").pack()
        self.score_label = tk.Label(self, text=SnakeItself.get_score())
        self.score_label.pack()
        self.increment_score()
        self.init_snake()

        self.bind("<Left>", lambda x: self.update_direction("LEFT"))
        self.bind("<Right>", lambda x: self.update_direction("RIGHT"))
        self.bind("<Up>", lambda x: self.update_direction("UP"))
        self.bind("<Down>", lambda x: self.update_direction("DOWN"))

        self.direction = "UP"

        self.update_elements()

    def increment_score(self):
        self.score_label.configure(text=SnakeItself.get_score())

    def update_direction(self, direction):
        vertical = ["UP", "DOWN"]
        horizontal = ["LEFT", "RIGHT"]
        if (self.direction in vertical and direction in vertical) or (
            self.direction in horizontal and direction in horizontal
        ):
            return
        self.direction = direction

    @staticmethod
    def update_config_with_moving(elem):
        if elem["D"] == "UP":
            elem["Y"] -= 10
        elif elem["D"] == "DOWN":
            elem["Y"] += 10
        elif elem["D"] == "LEFT":
            elem["X"] -= 10
        elif elem["D"] == "RIGHT":
            elem["X"] += 10

    def update_elements(self):
        self.increment_score()
        for idx, elem in enumerate(SnakeItself.elements):
            if idx + 1 == len(SnakeItself.elements):
                elem["D"] = self.direction
            else:
                elem["D"] = SnakeItself.elements[idx + 1]["D"]
            self.update_config_with_moving(elem)

        self.move()
        self.after(150, self.update_elements)

    def init_snake(self):
        self.update()
        window_height = self.winfo_height()
        window_width = self.winfo_width()
        canvas_width = window_width - 100
        SnakeItself.add_element(
            x_pos=int(math.ceil(canvas_width // 2 / 10.0)) * 10,
            y_pos=int(math.ceil(window_height // 2 / 10.0)) * 10,
            direction="UP",
        )
        self.move()

    def move(self):
        if self.snake_canvas.move_oval():
            self.destroy()
            SnakeItself.clear_all_data()


class SnakeCanvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.pack(side=tk.LEFT)
        self.update()
        self.feed = False
        self.feed_x = None
        self.feed_y = None

    def move_oval(self):
        self.delete("all")
        head = True
        for elem in reversed(SnakeItself.elements):
            if head:
                if self.check_if_wall(elem):
                    return True
                if self.check_if_bite(elem):
                    return True
            if head:
                self.create_oval(
                    elem["X"] - 5, elem["Y"] - 5, elem["X"] + 5, elem["Y"] + 5, fill="red"
                )
            else:
                self.create_oval(
                    elem["X"] - 5, elem["Y"] - 5, elem["X"] + 5, elem["Y"] + 5, fill="green"
                )
            if not self.feed:
                self.add_new_feed()
                self.feed = True
            if head:
                self.check_if_eat(elem)
            self.create_oval(
                self.feed_x - 5, self.feed_y - 5, self.feed_x + 5, self.feed_y + 5, fill="black"
            )
            head = False

    def add_new_feed(self):
        int(math.ceil(randrange(20, self.winfo_height() - 20) / 10.0)) * 10
        self.feed_x = int(math.ceil(randrange(20, self.winfo_width() - 20) / 10.0)) * 10
        self.feed_y = int(math.ceil(randrange(20, self.winfo_height() - 20) / 10.0)) * 10
        if (self.feed_x, self.feed_y) in SnakeItself.get_all_coords():
            self.add_new_feed()

    def check_if_eat(self, elem):
        x_p = y_p = None
        if (
            elem["X"] + 3 >= self.feed_x - 3
            and self.feed_x + 3 >= elem["X"] - 3
            and elem["Y"] + 3 >= self.feed_y - 3
            and self.feed_y + 3 >= elem["Y"] - 3
        ):
            self.feed = False

            if elem["D"] == "UP":
                x_p = elem["X"]
                y_p = elem["Y"] - 10
            elif elem["D"] == "DOWN":
                x_p = elem["X"]
                y_p = elem["Y"] + 10
            elif elem["D"] == "LEFT":
                x_p = elem["X"] - 10
                y_p = elem["Y"]
            elif elem["D"] == "RIGHT":
                x_p = elem["X"] + 10
                y_p = elem["Y"]
            else:
                print("WRONG PARAMETER")

            SnakeItself.add_element(
                x_pos=x_p, y_pos=y_p, direction=SnakeItself.get_last_direction()
            )

    def check_if_wall(self, elem):
        if (
            elem["X"] + 5 >= self.winfo_width()
            or elem["X"] - 5 <= 0
            or elem["Y"] + 5 >= self.winfo_height()
            or elem["Y"] - 5 <= 0
        ):
            return self.show_game_over()

    def check_if_bite(self, elem):
        if (elem["X"], elem["Y"]) in SnakeItself.get_all_coords()[:-1]:
            return self.show_game_over()

    @staticmethod
    def show_game_over():
        messagebox.showerror(
            "Game Over", "Game Over\nYour score: {}".format(SnakeItself.get_score())
        )
        return True


def main():
    snake = SnakeConfig()
    snake.mainloop()


if __name__ == "__main__":
    main()
