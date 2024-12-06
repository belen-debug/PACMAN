"""
Created by GFB in nov 2024
Universidad Carlos III de Madrid
"""
import constants
class Character2:
    """This class is simple example of how to represent a character for the final project.
    This character moves automatically"""

    def __init__(self, x: int, y: int, dir: int):
        """ This method creates the Character object
        :param x : the initial x of the character
        :param y : the initial y of the character
        """
        self.x = x
        self.y = y
        self.dir = dir
        # The sprite will be always the same, so no parameter is needed
        # The tuple is (image_bank, starting_x, starting_y, horizontal_size, vertical_size)
        # It would be a good idea to make the sprite read-only, we will see how to do it in lectures
        self.sprite = constants.CHARACTER2_SPRITE

    # Creating properties and setters for the Character's attributes
    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def dir(self) -> int:
        return self.__dir

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError ("The x must be an integer " + str(type(x)) + "is provided")
        elif x < 0:
            raise ValueError("The x must be a non negative number")
        else:
            self.__x = x

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError ("The y must be an integer " + str(type(y)) + "is provided")
        elif y < 0:
            raise ValueError("The y must be a non negative number")
        else:
            self.__y = y

    @dir.setter
    def dir(self, dir: int):
        if not isinstance(dir, int):
            raise TypeError(
                "The dir must be an integer " + str(type(dir)) + "is provided")
        elif dir < 0:
            raise ValueError("The dir must be a non negative number")
        else:
            self.__dir = dir

    def move(self, board_x_size: int, board_y_size: int):
        """ This is an example of how to move the character horizontally. No obstacles in the board
        are considered.
        :param direction: a string which can be left or right
        :param board_x_size: the horizontal size of the board, to check the limits
        """
        # Local variable to store the width of the character to check collisions with right border
        # of the board
        x_size = self.sprite[3]
        y_size = self.sprite[4]
        if self.dir == 0:
            if (self.x + x_size < board_x_size):
                self.x += 1
            else:
                self.dir = 1
        elif self.dir == 1:
            if (self.y + y_size < board_y_size):
                self.y += 1
            else:
                self.dir = 2
        elif self.dir == 2:
            if (self.x > 0):
                self.x -= 1
            else:
                self.dir = 3
        elif self.dir == 3:
            if (self.y > 0):
                self.y -= 1
            else:
                self.dir = 0
