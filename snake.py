"""
Classical Snake game is written in Python3 with Tkinter
"""

import math
from random import randrange
from typing import List, Dict, Union, Tuple, Optional

try:
    import Tkinter as tk  # noqa: N813
    from Tkinter import messagebox
except ImportError:
    import tkinter as tk
    from tkinter import messagebox


class SnakeDataContainer:
    """
    This class works as a data container for Snake elements.
    It contains the coordinates and direction of rendered ovals on the canvas.
    """

    elements: List[Dict[str, Union[str, int]]] = []

    @classmethod
    def add_element(cls, x_pos, y_pos, direction) -> None:
        """
        Adding a new element for the element list.
        Mainly this new element is the head of the Snake.
        :param x_pos: X coordinate of new oval object.
        :param y_pos: Y coordinate of new oval object.
        :param direction: Direction of new oval object.
                          This direction says where the snake should move.
        :return: None
        """

        SnakeDataContainer.elements.append({"X": x_pos, "Y": y_pos, "D": direction})

    @classmethod
    def get_elements(cls) -> List[Dict[str, Union[str, int]]]:
        """
        Providing all elements of Snake (Body as well as head).
        :return: List[Dict[str, Union[str, int]]]
        """

        return SnakeDataContainer.elements

    @classmethod
    def get_last_direction(cls) -> str:
        """
        Providing the last direction. Where the head should move.
        :return: String (UP, DOWN, LEFT, RIGHT).
        """

        return SnakeDataContainer.elements[-1]["D"]

    @classmethod
    def clear_all_data(cls) -> None:
        """
        Clear the complete container.
        It is needed when the user wants to start a new game.
        :return: None
        """

        SnakeDataContainer.elements.clear()

    @classmethod
    def get_all_coordinates(cls) -> List[Tuple[int, int]]:
        """
        Providing the coordinates of all elements of the snake.
        :return: List[Tuple[int, int]]
        """

        return [(x["X"], x["Y"]) for x in SnakeDataContainer.elements]

    @classmethod
    def get_score(cls) -> int:
        """
        Providing the current score of user.
        Actually it is the number of body elements (The head is not counted).
        :return: Number of body elements as an integer.
        """

        return len(SnakeDataContainer.elements) - 1


class SnakeConfig(tk.Tk):
    """
    This class visualise the first window where the configuration options are available for the
    user.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Init method of 'SnakeConfig' class.
        :param args: Arguments
        :param kwargs: Key-word arguments.
        """

        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("200x200")
        self.speed_variable = tk.StringVar(self)
        self.speed_variable.set("Medium")  # default value
        self.create_elements()

    def create_elements(self) -> None:
        """
        Rendering the graphical element for the window.
        :return: None
        """

        tk.Label(self, text="Speed").pack()
        tk.OptionMenu(self, self.speed_variable, "Slow", "Medium", "Fast").pack()
        tk.Button(self, text="START", command=self.start_game).pack()
        tk.Button(self, text="EXIT", command=self.destroy).pack()

    def start_game(self) -> None:
        """
        Start the Snake game in a top-level window.
        :return: None
        """

        SnakeGame(width=400, height=300, speed=self.speed_variable.get())


class SnakeGame(tk.Toplevel):
    """
    This class visualise a Top-level object.
    The moving/timing/init are handled in this class.
    """

    AFTER_TIMES: Dict[str, int] = {"Fast": 100, "Medium": 150, "Slow": 250}

    def __init__(self, *args, **kwargs) -> None:
        """
        Init method of 'SnakeConfig' class.
        :param args: Arguments
        :param kwargs: Key-word arguments.
        """

        self.snake_speed = kwargs.pop("speed")
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.geometry("{}x{}".format(kwargs["width"], kwargs["height"]))
        self.title("Python Snake Game")
        self.snake_canvas: SnakeCanvas = SnakeCanvas(
            self, width=kwargs["width"] - 100, height=kwargs["height"], bg="CadetBlue1",
        )
        tk.Label(self, text="SCORE").pack()
        self.score_label: tk.Label = tk.Label(self, text=SnakeDataContainer.get_score())
        self.score_label.pack()
        self.increment_score()
        self.init_snake()
        self.set_bindings()

        self.direction: str = "UP"

        self.update_elements()

    def set_bindings(self) -> None:
        """
        Setting the key bindings for the Snake moving.
        :return: None
        """

        self.bind("<Left>", lambda x: self.update_direction("LEFT"))
        self.bind("<Right>", lambda x: self.update_direction("RIGHT"))
        self.bind("<Up>", lambda x: self.update_direction("UP"))
        self.bind("<Down>", lambda x: self.update_direction("DOWN"))

    def increment_score(self) -> None:
        """
        Incrementing the current score (And updating the label object on the Top-level).
        It is calculated from the number of elements of body of Snake.
        :return: None
        """

        self.score_label.configure(text=SnakeDataContainer.get_score())

    def update_direction(self, direction) -> None:
        """
        Set the current direction.
        This direction says that the snake where should move.
        The direct direction change is not possible (Eg.: UP -> DOWN or LEFT -> RIGHT)
        If the user wants an impossible direction change the game does nothing.
        :param direction: The required direction from the user.
        :return: None
        """

        vertical: List[str] = ["UP", "DOWN"]
        horizontal: List[str] = ["LEFT", "RIGHT"]
        if (self.direction in vertical and direction in vertical) or (
            self.direction in horizontal and direction in horizontal
        ):
            return
        self.direction: str = direction

    @staticmethod
    def update_config_with_moving(elem) -> None:
        """
        Incrementing the coordinates of elements based on the direction.
        :param elem: The actual checking element (X, Y, D data)
        :return: None
        """

        if elem["D"] == "UP":
            elem["Y"] -= 10
        elif elem["D"] == "DOWN":
            elem["Y"] += 10
        elif elem["D"] == "LEFT":
            elem["X"] -= 10
        elif elem["D"] == "RIGHT":
            elem["X"] += 10

    def update_elements(self) -> None:
        """
        This method is the engine of the game.
        This method calls itself periodically and it handles the automatic moving.
        :return: None
        """

        self.increment_score()
        idx: int
        elem: Dict[Union[str, int]]
        for idx, elem in enumerate(SnakeDataContainer.elements):
            if idx + 1 == len(SnakeDataContainer.elements):
                elem["D"]: str = self.direction
            else:
                elem["D"]: str = SnakeDataContainer.elements[idx + 1]["D"]
            self.update_config_with_moving(elem)

        self.move()
        self.after(SnakeGame.AFTER_TIMES[self.snake_speed], self.update_elements)

    def init_snake(self) -> None:
        """
        Creating the head of the Snake.
        This element is the first one on the canvas as well as in the Data Container.
        The coordinates of head is calculated based on the size of window/canvas.
        :return: None
        """

        self.update()
        window_height: int = int(self.winfo_height())
        window_width: int = int(self.winfo_width())
        canvas_width: int = window_width - 100
        SnakeDataContainer.add_element(
            x_pos=int(math.ceil(canvas_width // 2 / 10.0)) * 10,
            y_pos=int(math.ceil(window_height // 2 / 10.0)) * 10,
            direction="UP",
        )
        self.move()

    def move(self) -> None:
        """
        Call the oval moving mechanism from the GUI (canvas) handler.
        It the snake bite itself or it touches the wall this method will destroy the Top-level
        window and clear the Data Container.
        :return: None
        """

        if self.snake_canvas.move_oval():
            self.destroy()
            SnakeDataContainer.clear_all_data()


class SnakeCanvas(tk.Canvas):
    """
    This class handles the canvas object on the Top-level window.
    It makes the oval moving and adding the new elements of snake.
    Furthermore this class handles the self-bite and wall touching.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Init method of 'SnakeConfig' class.
        :param args: Arguments
        :param kwargs: Key-word arguments.
        """
        tk.Canvas.__init__(self, *args, **kwargs)
        self.pack(side=tk.LEFT)
        self.update()
        self.feed: bool = False
        self.feed_x: int = 0
        self.feed_y: int = 0

    def move_oval(self) -> Optional[bool]:
        """
        Clearing the screen and rendering the object to the canvas (elements of snake and food).
        The elements are generated based on the Data container.
        :return: True in case of self-biting or wall touching else None
        """

        self.delete("all")
        head: bool = True
        for elem in reversed(SnakeDataContainer.elements):
            element_color: str = "green"
            if head:
                if self.check_if_wall(elem):
                    return True
                if self.check_if_bite(elem):
                    return True
                element_color = "red"

            self.create_oval(
                elem["X"] - 5, elem["Y"] - 5, elem["X"] + 5, elem["Y"] + 5, fill=element_color
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

    def add_new_feed(self) -> None:
        """
        Calculation the coordinates of a new food if the Snake has been ate the previous one.
        :return: None
        """

        self.feed_x: int = int(math.ceil(randrange(20, self.winfo_width() - 20) / 10.0)) * 10
        self.feed_y: int = int(math.ceil(randrange(20, self.winfo_height() - 20) / 10.0)) * 10
        # Calculation new coordinates if the food would be generated "into" the snake body.
        if (self.feed_x, self.feed_y) in SnakeDataContainer.get_all_coordinates():
            self.add_new_feed()

    def check_if_eat(self, elem) -> None:
        """
        Checking if the Snake has been eat the food in this period (move).
        :param elem: Data of head (X, Y, D)
        :return: None
        """

        x_p: int = 0
        y_p: int = 0
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

            SnakeDataContainer.add_element(
                x_pos=x_p, y_pos=y_p, direction=SnakeDataContainer.get_last_direction()
            )

    def check_if_wall(self, elem) -> Optional[bool]:
        """
        Checking if the Snake has been touched the wall in this period (move).
        :param elem: Data of head (X, Y, D)
        :return: True if the Snake has been touched the wall else None
        """

        if (
            elem["X"] + 5 >= self.winfo_width()
            or elem["X"] - 5 <= 0
            or elem["Y"] + 5 >= self.winfo_height()
            or elem["Y"] - 5 <= 0
        ):
            return self.show_game_over()

    def check_if_bite(self, elem) -> Optional[bool]:
        """
        Checking if the Snake has been bite itself in this period (move).
        :param elem: Data of head (X, Y, D)
        :return: True if the Snake has bite itself else None
        """

        if (elem["X"], elem["Y"]) in SnakeDataContainer.get_all_coordinates()[:-1]:
            return self.show_game_over()

    @staticmethod
    def show_game_over() -> bool:
        """
        Show the "Game OVer" window with the current score.
        :return: True in every case. This return value should be handled upper levels.
        """

        messagebox.showerror(
            "Game Over", "Game Over\nYour score: {}".format(SnakeDataContainer.get_score())
        )
        return True


def main() -> None:
    """
    Create the instance of main window and starting the mainloop.
    :return: None
    """

    snake: SnakeConfig = SnakeConfig()
    snake.mainloop()


if __name__ == "__main__":
    main()
