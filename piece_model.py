"""Holds all the data, methods, and logic of a chess game and the chess pieces.

Authors: Alec Mirambeau, Allison Scheffer, Lauren Mcguirk
"""

from __future__ import annotations
from enum import Enum
import abc
import pygame
from typing import *
import random


class Color(Enum):
    '''
    Enumeration class for color of chess pieces/players
    Statics:
        WHITE (int): An integer representing the enumerated value of the white static variable
        BLACK (int): An integer representing the enumerated value of the black static variable

    '''
    WHITE = 0
    BLACK = 1


class Piece(abc.ABC):
    """A chess piece.

    Hold methods and data associated with chess pieces.

    Attributes:
        color (Color): A static variable of Color representing the color of this chess piece."""
    # Make a static variable (not an instance variable) that holds the path to this image.
    # Have to make an images directory in the current directory that will hold the images of all the chess pieces.
    SPRITESHEET = pygame.image.load("./images/pieces.png")
    _game = 0

    @staticmethod
    def set_game(game: Game) -> None:
        """Static method to set the class variable.

        Sets the class variable _game to the game parameter passed.

        Params:
            _game (Game): A Game object to represent a Game instance.
            _image (Pygame): Image representing what this piece should look like.

        Raises:
            ValueError: A non-game instance was passed through the game parameter."""
        if not isinstance(game, Game):
            raise ValueError("You must provide a valid Game instance.")
        Piece._game = game

    def __init__(self, color: Color) -> None:
        """Initialize this Piece instance with the correct data (image and color passed as argument).

        Params:
            color (Color): A color representing the color of this chess piece."""
        self._color = color
        self._image = pygame.Surface((105, 105), pygame.SRCALPHA)

    @property
    def color(self) -> Color:
        """
        Returns:
             Color object representing the color of the player calling this method
        """
        return self._color

    def set_image(self, x: int, y: int) -> None:
        """
        Sets the image of the piece calling this method.

        Params:
            x (int): integer value to represent horizontal location on piece.png from ./images directory.
            y (int): integer value to represent vertical location on piece.png from ./images directory.
        """
        self._image.blit(Piece.SPRITESHEET, (0, 0), pygame.rect.Rect(x, y, 105, 105))

    def _diagonal_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int) -> list[tuple[int, int]]:
        """Returns all valid diagonal moves for a piece given it's position on the board.

        params:
            y (int): An integer representing the current y position on the board.
            x (int): An integer representing the current x position on the board.
            y_d (int): An integer representing the vertical direction from the piece's location to check.
            x_d (int): An integer representing the horizontal direction from the piece's location to check.
            distance (int): An integer that represents how far the (y,x) direction we want to check.

        Returns:
            valid_moves (list[tuple[int]]): The valid moves for the piece at this location."""
        # (y,x) is the way the tuples are formed
        valid_moves = []
        # this checks for when the piece is moving diagonal down and to the right.
        # We start the range loop at 1 because we don't want to check the spot where the piece
        # that is doing the moving is located. We end at distance + 1 because a queen can move 8
        # spaces at a time, and a pawn can only move 1. So, if we just used the distance value it
        # wouldn't work for a pawn because that would be a range loop from 1 to 1 (so nothing
        # would happen. With distance + 1 and with an if statement making sure only valid indexes
        # are going to be used we can then have this for loop work for queens and pawns.
        for i in range(1, (distance + 1)):
            # Checks diagonally down and to the right
            if y_d == 1 and x_d == 1:
                # make sure only valid indexes are checked.
                if 0 <= y + i < 8 and 0 <= x + i < 8:
                    # checks if there's a piece already at this location
                    if Piece._game.get((y + i), (x + i)) is None:
                        # If there isn't a piece, then this is a valid move so append it to the list
                        # of valid moves
                        valid_moves.append(((y + i), (x + i)))
                    # If there is a piece, check if it is the same color as the current moving piece.
                    elif Piece._game.get((y + i), (x + i)).color != self.color:
                        # If the piece aren't the same color, then this is a valid move and add it to
                        # the list.
                        valid_moves.append(((y + i), (x + i)))
                        break
                    else:
                        break
            # checks down and to the left diagonally.
            elif y_d == 1 and x_d == -1:
                # make sure only valid indexes are checked
                if 0 <= y + i < 8 and 0 <= x - i < 8:
                    # checks if there's already a piece at this location
                    if Piece._game.get((y + i), (x - i)) is None:
                        # If there isn't a piece, then this is a valid move so append it to the list
                        # of valid moves
                        valid_moves.append(((y + i), (x - i)))
                    # If there is a piece, check if it is the same color as the current moving piece.
                    elif Piece._game.get((y + i), (x - i)).color != self.color:
                        # If the piece aren't the same color, then this is a valid move and add it to
                        # the list.
                        valid_moves.append(((y + i), (x - i)))
                        break
                    else:
                        break
            # checks up and to the left diagonally.
            elif y_d == -1 and x_d == -1:
                # make sure only valid indexes are checked
                if 0 <= y - i < 8 and 0 <= x - i < 8:
                    # checks if there's already a piece at this location
                    if Piece._game.get((y - i), (x - i)) is None:
                        # If there isn't a piece, then this is a valid move so append it to the list
                        # of valid moves
                        valid_moves.append(((y - i), (x - i)))
                    # If there is a piece, check if it is the same color as the current moving piece.
                    elif Piece._game.get((y - i), (x - i)).color != self.color:
                        # If the piece aren't the same color, then this is a valid move and add it to
                        # the list.
                        valid_moves.append(((y - i), (x - i)))
                        break
                    else:
                        break
            # checks up and to the right diagonally.
            elif y_d == -1 and x_d == 1:
                # make sure only valid indexes are checked
                if 0 <= y - i < 8 and 0 <= x + i < 8:
                    # checks if there's already a piece at this location
                    if Piece._game.get((y - i), (x + i)) is None:

                        # If there isn't a piece, then this is a valid move so append it to the list
                        # of valid moves
                        valid_moves.append(((y - i), (x + i)))
                    # If there is a piece, check if it is the same color as the current moving piece.
                    elif Piece._game.get((y - i), (x + i)).color != self.color:
                        # If the piece aren't the same color, then this is a valid move and add it to
                        # the list.
                        valid_moves.append(((y - i), (x + i)))
                        break
                    else:
                        break
        return valid_moves

    def _horizontal_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int) -> list[tuple[int, int]]:
        """Returns all valid horizontal moves for a piece given it's position on the board.

        params:
            y (int): An integer representing the row number of the piece's current location
            x (int) An integer representing the column number of the piece' current location.
            y_d (int): An integer representing the vertical direction from the piece's location to check.
            x_d (int): An integer representing the horizontal direction from the piece's location to check.
            distance (int): An integer that represents how far the (y,x) direction we want to check.

        Returns:
            valid_moves (list[tuple[int]]): The valid moves for the piece at this location."""
        valid_moves = []
        for i in range(1, (distance + 1)):
            # Check spots to the right of this piece's current location.
            if x_d == 1:
                # make sure only valid indexes are checked.
                if 0 <= x + i < 8:
                    # checks if there's a piece already at this location
                    if Piece._game.get(y, (x + i)) is None:
                        # If there isn't a piece, then this is a valid move so append it to the list
                        # of valid moves
                        valid_moves.append((y, (x + i)))
                    # If there is a piece, check if it is the same color as the current moving piece.
                    elif Piece._game.get(y, (x + i)).color != self.color:
                        # If the piece aren't the same color, then this is a valid move and add it to
                        # the list.
                        valid_moves.append((y, (x + i)))
                        break
                    else:
                        break
            # Check spots to the left of this piece's current location.
            elif x_d == -1:
                # make sure only valid indexes are checked.
                if 0 <= x - i < 8:
                    # checks if there's a piece already at this location
                    if Piece._game.get(y, (x - i)) is None:
                        # If there isn't a piece, then this is a valid move so append it to the list
                        # of valid moves
                        valid_moves.append((y, (x - i)))
                    # If there is a piece, check if it is the same color as the current moving piece.
                    elif Piece._game.get(y, (x - i)).color != self.color:
                        # If the piece aren't the same color, then this is a valid move and add it to
                        # the list.
                        valid_moves.append((y, (x - i)))
                        break
                    else:
                        break
        return valid_moves

    def _vertical_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int) -> list[tuple[int, int]]:
        """Returns all valid vertical moves for a piece given it's position on the board.

        params:
            y (int): An integer representing the row number of the piece's current location
            x (int) An integer representing the column number of the piece' current location.
            y_d (int): An integer representing the vertical direction from the piece's location to check.
            x_d (int): An integer representing the horizontal direction from the piece's location to check.
            distance (int): An integer that represents how far the (y,x) direction we want to check.

        Returns:
            valid_moves (list[tuple[int]]): The valid moves for the piece at this location."""
        valid_moves = []
        for i in range(1, (distance + 1)):
            # Check spots below this piece's current location.
            if y_d == 1:
                # make sure only valid indexes are checked.
                if 0 <= y + i < 8:
                    # checks if there's a piece already at this location
                    if Piece._game.get((y + i), x) is None:
                        # If there isn't a piece, then this is a valid move so append it to the list
                        # of valid moves
                        valid_moves.append(((y + i), x))
                    # If there is a piece, check if it is the same color as the current moving piece.
                    elif Piece._game.get((y + i), x).color != self.color:
                        # If the piece aren't the same color, then this is a valid move and add it to
                        # the list.
                        valid_moves.append(((y + i), x))
                        break
                    else:
                        break
            # Check spots to above this piece's current location.
            elif y_d == -1:
                # make sure only valid indexes are checked.
                if 0 <= y - i < 8:
                    # checks if there's a piece already at this location
                    if Piece._game.get((y - i), x) is None:
                        # If there isn't a piece, then this is a valid move so append it to the list
                        # of valid moves
                        valid_moves.append(((y - i), x))
                    # If there is a piece, check if it is the same color as the current moving piece.
                    elif Piece._game.get((y - i), x).color != self.color:
                        # If the piece aren't the same color, then this is a valid move and add it to
                        # the list.
                        valid_moves.append(((y - i), x))
                        break
                    else:
                        break
        return valid_moves

    def get_diagonal_moves(self, y: int, x: int, distance: int) -> list[tuple[int, int]]:
        """Returns all valid diagonal moves of the chess piece calling this method.

        Given a specified position on the board, and the distance the piece calling this method can travel.
        This method will return all the allowable diagonal moves by this piece.

        Params:
            y (int): An integer representing the y position of this piece (the row number of this piece).
            x (int): An integer representing the x position of this piece (the colum number of this piece).
            distance (int): An integer representing the distance number this piece can travel.

        Returns:
                moves (list[tuple[int, int]]): A list containing tuples of two integers that represent the valid
                    moves in the diagonal direction by this chess piece."""
        moves = []
        moves += (self._diagonal_moves(y, x, -1, 1, distance))
        moves += (self._diagonal_moves(y, x, -1, -1, distance))
        moves += (self._diagonal_moves(y, x, 1, 1, distance))
        moves += (self._diagonal_moves(y, x, 1, -1, distance))
        return moves

    def get_horizontal_moves(self, y: int, x: int, distance: int) -> list[tuple[int, int]]:
        """Returns all valid horizontal moves of the chess piece calling this method.

        Given a specified position on the board, and the distance the piece calling this method can travel.
        This method will return all the allowable horizontal moves by this piece.

        Params:
            y (int): An integer representing the y position of this piece (the row number of this piece).
            x (int): An integer representing the x position of this piece (the colum number of this piece).
            distance (int): An integer representing the distance number this piece can travel.

        Returns:
                moves (list[tuple[int, int]]): A list containing tuples of two integers that represent the valid
                    moves in the horizontal direction by this chess piece."""
        moves = []
        # add moves to the left.
        moves += (self._horizontal_moves(y, x, 0, -1, distance))
        # add moves to the right.
        moves += (self._horizontal_moves(y, x, 0, 1, distance))
        return moves

    def get_vertical_moves(self, y: int, x: int, distance: int) -> list[tuple[int, int]]:
        """Returns all valid vertical moves of the chess piece calling this method.

        Given a specified position on the board, and the distance the piece calling this method can travel.
        This method will return all the allowable vertical moves by this piece.

        Params:
            y (int): An integer representing the y position of this piece (the row number of this piece).
            x (int): An integer representing the x position of this piece (the colum number of this piece).
            distance (int): An integer representing the distance number this piece can travel.

        Returns:
                moves (list[tuple[int, int]]): A list containing tuples of two integers that represent the
                    location of each valid move in the vertical direction by this chess piece."""
        moves = []
        # Check moves in the up direction
        moves += (self._vertical_moves(y, x, -1, 0, distance))
        # Check moves in the down direction.
        moves += (self._vertical_moves(y, x, 1, 0, distance))
        return moves

    @abc.abstractmethod
    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """Returns all the valid moves for this piece type at it's given location.

        Params:
            y (int): An integer representing the row number of this piece.
            x (int): An integer representing the column number of this piece.

        Returns:
            valid_moves (list[tuple[int, int]]): A list containing tuples of two integers representing the
            (row number, column number) of each of the valid moves that can be done by this piece."""
        pass

    @abc.abstractmethod
    def copy(self):
        """Copies the state of the board with all the pieces and their current location."""
        pass


# STEP 2


class King(Piece):
    """A King Chess piece.

    Holds the methods and data associated with a king chess piece for a chess game to
    correctly function.

    Attributes:
        See base class."""

    def __init__(self, color: Color):
        """Initialize this King instance with the correct data."""
        super().__init__(color)
        self.set_image(0, color.value * 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """see base class."""
        valid_moves = []
        valid_moves += (self.get_diagonal_moves(y, x, 1))
        valid_moves += (self.get_horizontal_moves(y, x, 1))
        valid_moves += self.get_vertical_moves(y, x, 1)
        return valid_moves

    def copy(self) -> 'King':
        """Returns a king instance of the same color as the piece calling this method."""
        return King(self.color)


class Queen(Piece):
    """A Queen Chess piece.

    Holds the methods and data associated with a Queen chess piece for a chess game to function
    correctly.

    Attributes:
        see base class."""

    def __init__(self, color: Color):
        """Initialize this queen instance with the correct data.

        Params:
            see base class."""
        super().__init__(color)
        self.set_image(105, color.value * 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """see base class."""
        valid_moves = []
        valid_moves += (self.get_diagonal_moves(y, x, 8))
        valid_moves += (self.get_horizontal_moves(y, x, 8))
        valid_moves += self.get_vertical_moves(y, x, 8)
        return valid_moves

    def copy(self) -> 'Queen':
        """Returns a Queen instance of the same color as the piece calling this method."""
        return Queen(self.color)


class Bishop(Piece):
    """A Bishop chess piece.

    Holds the methods and data associated with a Bishop chess piece for a chess game to function
    correctly.

    Attributes:
        see base class
 """

    def __init__(self, color: Color) -> None:
        """Initializes this Bishop instance with the correct data.

        Params:
            see base class."""
        super().__init__(color)
        self.set_image(210, color.value * 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """see base class."""
        valid_moves = []
        valid_moves += self.get_diagonal_moves(y, x, 8)
        return valid_moves

    def copy(self) -> 'Bishop':
        """Returns a Bishop instance of the same color as the piece calling this method."""
        return Bishop(self.color)


class Knight(Piece):
    """A Knight Chess Piece.

    Holds the methods and data associated with a Knight chess piece for a chess game to function
    correctly.

    Attributes:
        see base class."""

    def __init__(self, color: Color) -> None:
        """Initializes this Knight instance with the correct data.

        Params:
            see base class."""
        super().__init__(color)
        self.set_image(315, color.value * 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        '''
        :param y: int y position on chess board (horizontal)
        :param x: int x position on chess board (vertical)
        :return: list of tuples of all valid moves for piece passed through parameters
        '''
        valid_moves = []
        for a in range(-2, 3):
            if a == -1:
                if 0 <= x + a < 8 and 0 <= y + 2 < 8:
                    valid_moves.append((y + 2, x + a))
                if 0 <= x + a < 8 and 0 <= y - 2 < 8:
                    valid_moves.append((y - 2, x + a))
            if a == 1:
                if 0 <= x + a < 8 and 0 <= y + 2 < 8:
                    valid_moves.append((y + 2, x + a))
                if 0 <= x + a < 8 and 0 <= y - 2 < 8:
                    valid_moves.append((y - 2, x + a))
            if a == 2:
                if 0 <= x + a < 8 and 0 <= y + 1 < 8:
                    valid_moves.append((y + 1, x + a))
                if 0 <= x + a < 8 and 0 <= y - 1 < 8:
                    valid_moves.append((y - 1, x + a))
            if a == -2:
                if 0 <= x + a < 8 and 0 <= y + 1 < 8:
                    valid_moves.append((y + 1, x + a))
                if 0 <= x + a < 8 and 0 <= y - 1 < 8:
                    valid_moves.append((y - 1, x + a))

        real_valid_moves = []
        # this is where it will all fall apart
        # filters out only the valid moves from the valid moves list.
        for element in valid_moves:
            y1, x1 = element
            if Piece._game.get(y1, x1) is None:
                real_valid_moves.append(element)
            elif Piece._game.get(y1, x1).color != self.color:
                real_valid_moves.append(element)

        return real_valid_moves

        # elif Piece._game.get(y1, x1) is not None:
        #     valid_moves.remove(element)

    def copy(self) -> 'Knight':
        """Returns a Knight instance of the same color as the piece calling this method."""
        return Knight(self.color)


class Rook(Piece):
    """A Rook Chess Piece.

    Holds the methods and data associated with a Rook chess piece for a chess game to function
    correctly.

    Attributes:
        see base class."""

    def __init__(self, color: Color) -> None:
        """Initializes this Rook instance with the correct data.

        Params:
            see base class."""
        super().__init__(color)
        self.set_image(420, color.value * 105)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """see base class."""
        valid_moves = []
        valid_moves += self.get_vertical_moves(y, x, 8)
        valid_moves += self.get_horizontal_moves(y, x, 8)
        return valid_moves

    def copy(self) -> 'Rook':
        """Returns a Bishop instance of the same color as the piece calling this method."""
        return Rook(self.color)


class Pawn(Piece):
    """A Pawn Chess Piece.

    Holds the methods and data associated with a Pawn chess piece for a chess game to function
    correctly.

    Attributes:
        see base class."""

    def __init__(self, color: Color) -> None:
        """Initializes this Pawn instance with the correct data.

        Params:
            first_move (bool): A Boolean to represent if this is this pawns first move or not.
            forward (int): To represent the direction this pawn will move.
            see base class."""
        super().__init__(color)
        self.set_image(525, color.value * 105)
        self._first_move = True
        if self.color == Color.WHITE:
            self._forward = -1
        else:
            self._forward = 1

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """see base class."""
        valid_moves = []
        # adds moves two in front of this pawn
        if self._first_move == True and Piece._game.get((self._forward * 2), x) is None:
            valid_moves += self._vertical_moves(y, x, self._forward, 0, 2)
        # add moves right in front of this pawn
        # if Piece._game.get(self._forward, x) is None:
        valid_moves += self._vertical_moves(y, x, self._forward, 0, 1)

        real_valid_moves = []
        for move in valid_moves:
            y1, x2 = move
            if Piece._game.get(y1, x2) is None:
                real_valid_moves.append(move)

        # diaganol left
        if 0 <= y + self._forward < 8 and 0 <= (x + 1) < 8:
            if Piece._game.get(y + self._forward, x + 1) is not None and Piece._game.get(y + self._forward,
                                                                                         x + 1).color != self.color:
                real_valid_moves += [((y + self._forward), (x + 1))]
        # diaganol left
        if 0 <= y + self._forward < 8 and 0 <= (x - 1) < 8:
            if Piece._game.get(y + self._forward, x - 1) is not None and Piece._game.get(y + self._forward,
                                                                                         x - 1).color != self.color:
                real_valid_moves += [((y + self._forward), (x - 1))]
        return real_valid_moves

    def copy(self) -> 'Pawn':
        """Returns a Pawn instance of the same color as the piece calling this method."""
        r_pawn = Pawn(self.color)
        r_pawn._first_move = self._first_move
        r_pawn._forward = self._forward
        return r_pawn


"""For pawn class have another instance variable for direction for instance, 1 if the pawn is black
since pawns can only move forward, and -1 if the pawn is white since pawns can only move forward and a
white pawn will only move up and a black pawn will only move down.
"""


class Game:
    """The game logic.

    This class holds all the logic for the a chess game.

    Attributes:
        _board (list): A list to represent the current board status.
        current_player (Color): A Color to represent which team color is the current player.
        _prior_states (list[list[None | tuple[int, int]]): An array to hold all of the previous board states."""

    def __init__(self) -> None:
        '''
        initializes game with correct pieces in position on chess board, length of previous boards list is empty
        '''
        Piece.set_game(self)
        self._board = [[None for i in range(0, 8)] for i in range(0, 8)]
        self.current_player = Color.WHITE
        # this will serve as the stack data structure.
        self._prior_states: list[list[None | tuple[int, int]]] = []
        self.reset()

    def reset(self) -> None:
        """Resets the chess game to its default state."""
        # self._board = [[None for i in range(0, 8)] for i in range(0, 8)]

        # This will reset the board to the defaults by setting all the pieces
        # back where they start

        # could also write line:
        self._board = [[None for i in range(0, 8)] for i in range(0, 8)]
        # and then call setup_pieces, deleting nested loop

        self._setup_pieces()
        # for row in range(2, 6):
        #     for col in range(8):
        #         self._board[row][col] = None
        self._prior_states = []
        self.current_player = Color.WHITE

    def _setup_pieces(self) -> None:
        '''
        sets up all chess pieces on the board and initilizes top pieces to color
        black and bottom pieces to color white initializes all other chess squares to None
        '''
        # Black pieces
        self._board[0][0] = Rook(Color.BLACK)
        self._board[0][1] = Knight(Color.BLACK)
        self._board[0][2] = Bishop(Color.BLACK)
        self._board[0][3] = Queen(Color.BLACK)
        self._board[0][4] = King(Color.BLACK)
        self._board[0][5] = Bishop(Color.BLACK)
        self._board[0][6] = Knight(Color.BLACK)
        self._board[0][7] = Rook(Color.BLACK)
        for i in range(8):
            self._board[1][i] = Pawn(Color.BLACK)

        # This code would set the middle squares to None
        # for row in range(2, 6):
        #     for col in range(8):
        #         self._board[row][col] = None

        # White pieces
        self._board[7][0] = Rook(Color.WHITE)
        self._board[7][1] = Knight(Color.WHITE)
        self._board[7][2] = Bishop(Color.WHITE)
        self._board[7][3] = Queen(Color.WHITE)
        self._board[7][4] = King(Color.WHITE)
        self._board[7][5] = Bishop(Color.WHITE)
        self._board[7][6] = Knight(Color.WHITE)
        self._board[7][7] = Rook(Color.WHITE)

        for i in range(8):
            self._board[6][i] = Pawn(Color.WHITE)

    def get(self, y: int, x: int) -> Optional[Piece]:
        """Returns the element at the passed location.

        Params:
            y (int): An integer representing the row number on the chess board.
            x (int): An integer representing the column number on the chess board

        Returns:
            The element at the (y,x) location passed when calling this method. If there's a
            subclass of the Piece class, that subclass instance will be returned. Otherwise None will
            be returned"""
        if not (0 <= y < 8) or not (0 <= x < 8):
            pass
        else:
            return self._board[y][x]

    def switch_player(self) -> None:
        """
        Method that switches the current player to the opposing player.
        """

        if self.current_player == Color.WHITE:
            self.current_player = Color.BLACK
        else:
            self.current_player = Color.WHITE

    def undo(self) -> bool:
        '''
        undoes the most recent move from the board if possible

        checks if the length of list of prior board states is not equal to zero
            if length of prior_states is 0, returns False meaning the undo method failed.
            if length is not zero, sets board to value of previous board and switches the player color, and
            returns True meaning the undo method was successfully executed.

        :returns: a boolean representing if undoing the most recent move is possible
        '''
        # if len(self._prior_states) >= 2:
        #     self._prior_states.pop()
        #     self._board = self._prior_states.pop()
        # len(self._prior_states) != 0:
        #     self._board = self._prior_states.pop()
        #     return True
        # return False
        if len(self._prior_states) != 0:
            self._board = self._prior_states.pop()
            self.switch_player()
            return True
        return False

    def copy_board(self) -> list[list[None | Piece]]:
        """Returns a copied version of the current board.

        Returns:
            _prior_board (list[list[None | Piece]]): A list of lists containing
                None or a Piece subclass to represent a copied version of the current board"""
        _prior_board = [[None for i in range(0, 8)] for i in range(0, 8)]
        for i in range(0, 8):
            for j in range(0, 8):
                if self._board[i][j] is not None:
                    _prior_board[i][j] = self._board[i][j].copy()
        return _prior_board

    def move(self, piece: Piece, y: int, x: int, y2: int, x2: int) -> bool:
        """Performs the move for the piece from the current location to the passed location

        Params:
            piece (Piece): A Piece instance to represent a chess piece.
            y (int): An integer representing the row number that the piece is currently located.
            x (int): An integer representing the column number the piece is currently located.
            y2 (int): An integer representing the new row number to move this piece.
            x2 (int): An integer representing the new column number to move this piece to.

        Returns:
            A boolean representing if a successful move occurred. True if a move successfully took place, false
            if not.
            """
        self._prior_states.append(self.copy_board())

        # if self.check(piece.color):
        #     check_valid_moves = []
        #     for move in piece.valid_moves(y, x):
        #         yy, xx = move
        #         self._board[yy][xx] = piece
        #         if not self.check(piece.color):
        #             check_valid_moves.append(move)
        #         self.undo()
        #     piece.valid_moves = check_valid_moves

        # if isinstance(piece, Pawn) and piece._first_move == True:
        #     if (y2, x2) in piece.valid_moves(y, x):
        #         self._board[y2][x2] = piece
        #         self._board[y][x] = None
        #         if self.check(piece.color):
        #             self._board = self._prior_states.pop()
        #             return False
        #     piece._first_move = False

        if (y2, x2) in piece.valid_moves(y, x):
            self._board[y2][x2] = piece
            self._board[y][x] = None
            if self.check(piece.color):
                self._board = self._prior_states.pop()
                return False
            if isinstance(piece, Pawn) and piece._first_move is True:
                piece._first_move = False

        if isinstance(piece, Pawn) and piece.color == Color.WHITE and y2 == 0:
            self._board[y2][x2] = Queen(piece.color)
        elif isinstance(piece, Pawn) and piece.color == Color.BLACK and y2 == 7:
            self._board[y2][x2] = Queen(piece.color)

        self.switch_player()
        return True

    def get_piece_locations(self, color: Color) -> list[tuple[int, int]]:
        """Returns a list[tuple[int, int]] representing all the locations of each piece of the passed color."""
        all_piece_locations = []
        for y in range(0, 8):
            for x in range(0, 8):
                if self._board[y][x] is not None and self._board[y][x].color == color:
                    all_piece_locations.append((y, x))
        return all_piece_locations

    def find_king(self, color: Color) -> tuple[int, int]:
        """Returns a tuple of two integers representing the location of the king of the passed color."""
        for y in range(0, 8):
            for x in range(0, 8):
                if self._board[y][x] is not None and isinstance(self._board[y][x], King) and self._board[y][
                    x].color == color:
                    return (y, x)

    def check(self, color: Color) -> bool:
        """Returns a boolean representing if the king of the passed color is in check or not."""
        if color == Color.WHITE:
            opponent_color = Color.BLACK
        else:
            opponent_color = Color.WHITE
        opponent_piece_locations = self.get_piece_locations(opponent_color)
        ky, kx = self.find_king(color)

        for piece in opponent_piece_locations:
            all_valid_moves = []
            y, x = piece
            all_valid_moves += self._board[y][x].valid_moves(y, x)
            if (ky, kx) in all_valid_moves:
                return True
        return False

    def mate(self, color: Color) -> bool:
        """Returns a boolean representing if this piece is in checkmate.

        Params:
            color (Color): A Color instance variable representing the color of the chess piece
                we will be checking to see if is in checkmate."""
        # checks if this color is in check
        if self.check(color):
            # if this color is in check we then check for if it's in checkmate

            # if the color we're checking for is white then the opponent is black color
            if color == Color.WHITE:
                opponent_color = Color.BLACK
            else:
                # if the color we're checking for is black then the opponent color is white
                opponent_color = Color.WHITE
            # get all the locations of the opponents pieces
            opponent_piece_locations = self.get_piece_locations(opponent_color)

            all_opponent_valid_moves = []
            # get the location of the king of the passed color
            ky, kx = self.find_king(color)
            # loop over all of the opponents pieces
            for piece in opponent_piece_locations:
                # assign y and x to the location of the piece.
                y, x = piece
                # add all of the possible moves that this piece can do and add them to the valid_moves list.
                all_opponent_valid_moves += self._board[y][x].valid_moves(y, x)
            # get all of the kings valid moves.
            king_valid_moves = self._board[ky][kx].valid_moves(ky, kx)
            # Check all the moves for the king piece
            for move in king_valid_moves:
                # checks if this move that the king can do is not in the opponents valid moves
                if move not in all_opponent_valid_moves:
                    king_success_move = self.move(self._board[ky][kx], ky, kx, move[0], move[1])
                    if king_success_move is True:
                        self.undo()
                        # if a king can make a move that isn't in the opponents moves, then he isn't in check.
                        # so return False
                        return False

            # Get all the moves that this player could make
            for y in range(0, 8):
                for x in range(0, 8):
                    # assign all_valid_moves to an empty list for each x shift.
                    all_valid_moves = []
                    # makes sure that the element at this spot is not None and that it's the same color as the passed color.
                    if self._board[y][x] is not None and self._board[y][x].color == color:
                        # if there is a piece of the passed color. assign current_piece to that location.
                        current_piece = self._board[y][x]
                        # all_valid_moves is equal to the list of the valid moves for this piece.
                        all_valid_moves += current_piece.valid_moves(y, x)
                        # loop through each valid move for this piece
                        for movee in all_valid_moves:
                            ny, nx = movee
                            success_or_fail = self.move(current_piece, y, x, ny, nx)
                            # If the move was a success, then True was returned, so that means the king won't be in
                            # check.
                            if success_or_fail == True:
                                # The move was a success so the move actually took place so we need to undo that
                                # move so the actual game board doesn't get changed
                                self._board = self._prior_states.pop()
                                return False

            return True
        # king was never in check so we return false.
        return False

    def ai_checkmate(self) -> tuple[tuple[int, int] | None, tuple[int, int] | None, bool]:
        """This method does the check move for the AI.

                Returns:
                    A tuple of None, None, and False or a tuple that contains another tuple
                    with the location of the piece that will do the move to put the
                    white team in checkmate, and the next element in the tuple is the
                    location of the move that will be done to put white team in checkmate,
                    and the last element of the tuple is a boolean representing the fact
                    that the black team found a way to put white team in checkmate."""
        all_locations = self.get_piece_locations(Color.BLACK)
        for loc in all_locations:
            y, x = loc
            moves = self._board[y][x].valid_moves(y, x)
            for move in moves:
                y2, x2 = move
                # gets if the move was a success or not
                move_success_or_fail = self.move(self._board[y][x], y, x, y2, x2)
                # if the move worked then we see if it caused the white player to be put into checkmate
                if move_success_or_fail:
                    mate_success_or_fail = self.mate(Color.WHITE)
                    # If the white player was put in checkmate we want to return the location of the piece,
                    # and the move it made, and a success boolean.
                    if mate_success_or_fail:
                        self.undo()
                        return (y, x), (y2, x2), True
                    # If the move didn't checkmate the white player, then we need to undo the move
                    # so it doesn't get done.
                    else:
                        self.undo()
        return None, None, False

    def ai_check(self) -> tuple[tuple[int, int] | None, tuple[int, int] | None, bool]:
        """This method does the check move for the AI.

                Returns:
                    A tuple of None, None, and False or a tuple that contains another tuple
                    with the location of the piece that will do the move to put the
                    white team in checkmate, and the next element in the tuple is the
                    location of the move that will be done to put white team in checkmate,
                    and the last element of the tuple is a boolean representing the fact
                    that the black team found a way to put white team in checkmate."""
        # We get all of the black pieces
        all_black_pieces = self.get_piece_locations(Color.BLACK)
        # we loop over all of the black pieces.
        for piece in all_black_pieces:
            # assign the current piece's location to py, px
            py, px = piece
            # gets all of the valid moves for this piece
            this_pieces_valid_moves = self._board[py][px].valid_moves(py, px)
            # loops over all of the moves for this piece to try each one and see if it causes black to check the white team.
            for move in this_pieces_valid_moves:
                # assigns the move to be tested and its coordinates to y2 and x2.
                y2, x2 = move
                # tries the move and see if it resulted in a success or failure (if the move was executed or not).
                move_success_or_fail = self.move(self.get(py, px), py, px, y2, x2)
                # if the move was a success and was moved:
                if move_success_or_fail:
                    # see if the move just done caused black to put white in check.
                    check_succ_or_fail = self.check(Color.WHITE)
                    # if the move put white in check, return the correct values.
                    if check_succ_or_fail:
                        # undo the move first because the move hasn't been executed in the computer move method.
                        self.undo()
                        # return the piece that will do the move, and the move it will do and a boolean of True meaning
                        # black can do a move to put white in check.
                        return piece, move, True
                    # if the move didn't put white in check, we still have to undo the move since it's not a move we
                    # want to execute since white wasn't put in check.
                    else:
                        self.undo()
        # If none of the possible moves we could do could put white in check, we return None, None, False.
        return None, None, False

    # type hint needed for return values
    def ai_capture_queen(self) -> tuple[tuple[int, int] | None, tuple[int, int] | None, bool]:
        '''Allows the AI to capture the queen if that's a valid outcome for the AI.

        returns: - tuple representing location of enemy queen
                 - tuple representing move used to capture queen
                 - boolean representing if the move can be made by black team

        '''
        queen_locations = []
        for y in range(0, 8):
            for x in range(0, 8):
                if isinstance(self._board[y][x], Queen) and self._board[y][x].color == Color.WHITE:
                    queen_locations.append((y, x))
        all_locations = self.get_piece_locations(Color.BLACK)
        for loc in all_locations:
            y, x = loc
            moves = self._board[y][x].valid_moves(y, x)
            for queen_loc in queen_locations:
                if queen_loc in moves:
                    move_success_or_not = self.move(self._board[y][x], y, x, queen_loc[0], queen_loc[1])
                    if move_success_or_not:
                        self.undo()
                        # I think we can just return the queen_loc
                        return (y, x), moves[moves.index(queen_loc)], True
        return None, None, False

    def ai_capture_bishop(self) -> tuple[tuple[int, int] | None, tuple[int, int] | None, bool]:
        '''Allows the AI to capture the bishop if that's a valid possibility for the AI.

        returns: - tuple representing location of enemy bishop
                 - tuple representing move used to capture bishop
                 - boolean representing if the move can be made by black team

        '''
        bishop_locations = []
        for y in range(0, 8):
            for x in range(0, 8):
                if isinstance(self._board[y][x], Bishop) and self._board[y][x].color == Color.WHITE:
                    bishop_locations.append((y, x))
        all_locations = self.get_piece_locations(Color.BLACK)
        for loc in all_locations:
            y, x = loc
            moves = self._board[y][x].valid_moves(y, x)
            for bishop_loc in bishop_locations:
                if bishop_loc in moves:
                    move_success_or_not = self.move(self._board[y][x], y, x, bishop_loc[0], bishop_loc[1])
                    if move_success_or_not:
                        self.undo()
                        # I think we can just return the queen_loc
                        return (y, x), moves[moves.index(bishop_loc)], True
        return None, None, False

    def ai_capture_knight(self) -> tuple[tuple[int, int] | None, tuple[int, int] | None, bool]:
        '''Allows the AI to capture a knight if that's a valid possibility for it.

        returns: - tuple representing location of enemy knight
                 - tuple representing move used to capture knight
                 - boolean representing if the move can be made by black team

        '''
        knight_locations = []
        for y in range(0, 8):
            for x in range(0, 8):
                if isinstance(self._board[y][x], Knight) and self._board[y][x].color == Color.WHITE:
                    knight_locations.append((y, x))
        all_locations = self.get_piece_locations(Color.BLACK)
        for loc in all_locations:
            y, x = loc
            moves = self._board[y][x].valid_moves(y, x)
            for knight_loc in knight_locations:
                if knight_loc in moves:
                    move_success_or_not = self.move(self._board[y][x], y, x, knight_loc[0], knight_loc[1])
                    if move_success_or_not:
                        self.undo()
                        # I think we can just return the queen_loc
                        return (y, x), moves[moves.index(knight_loc)], True
        return None, None, False

    def ai_capture_rook(self) -> tuple[tuple[int, int] | None, tuple[int, int] | None, bool]:
        '''Allows the AI to capture a rook if that's a valid outcome for the AI.

        returns: - tuple representing location of enemy rook
                 - tuple representing move used to capture rook
                 - boolean representing if the move can be made by black team

        '''
        rook_locations = []
        for y in range(0, 8):
            for x in range(0, 8):
                if isinstance(self._board[y][x], Rook) and self._board[y][x].color == Color.WHITE:
                    rook_locations.append((y, x))
        all_locations = self.get_piece_locations(Color.BLACK)
        for loc in all_locations:
            y, x = loc
            moves = self._board[y][x].valid_moves(y, x)
            for rook_loc in rook_locations:
                if rook_loc in moves:
                    move_success_or_not = self.move(self._board[y][x], y, x, rook_loc[0], rook_loc[1])
                    if move_success_or_not:
                        self.undo()
                        # I think we can just return the queen_loc
                        return (y, x), moves[moves.index(rook_loc)], True
        return None, None, False

    def ai_capture_pawn(self) -> tuple[tuple[int, int] | None, tuple[int, int] | None, bool]:
        '''Allows the AI to capture a pawn if that's a valid move available to the AI.

        returns: - tuple representing location of enemy pawn
                 - tuple representing move used to capture pawn
                 - boolean representing if the move can be made by black team

        '''
        pawn_locations = []
        for y in range(0, 8):
            for x in range(0, 8):
                if isinstance(self._board[y][x], Pawn) and self._board[y][x].color == Color.WHITE:
                    pawn_locations.append((y, x))
        all_locations = self.get_piece_locations(Color.BLACK)
        for loc in all_locations:
            y, x = loc
            moves = self._board[y][x].valid_moves(y, x)
            for pawn_loc in pawn_locations:
                if pawn_loc in moves:
                    move_success_or_not = self.move(self._board[y][x], y, x, pawn_loc[0], pawn_loc[1])
                    if move_success_or_not:
                        self.undo()
                        # I think we can just return the queen_loc
                        return (y, x), moves[moves.index(pawn_loc)], True
        return None, None, False

    def _computer_move(self) -> str:
        """Performs the move for the AI."""

        # we need to loop until the computer makes a valid move because if they make an invalid move then nothing
        # happened for the turn, could this cause the game to be unplayable? Since we're waiting for the black
        # color to make a move but they never did since it wasn't in a loop.

        # gets the piece location, the checkmate move location, and there was a succesful checkmate move found.
        # piece_loc, mate_move, success_or_fail = self.ai_mate()
        # py, px = piece_loc
        # my, mx = mate_move
        # if success_or_fail:
        #     self.move(self._board[py][px], py, px, my, mx)
        #     return
        # # this does the check movement
        # piece_loc, check_move, success_or_fail = self.ai_check()
        # py, px = piece_loc
        # cy, cx = check_move
        # elif success_or_fail:
        #     self.move(self._board[py][px], py, px, cy, cx)
        #     return
        # gets the result for the checkmate move
        piece_for_checkmate, move_for_checkmate_loc, checkmate_success_or_fail = self.ai_checkmate()
        # gets the result for the check move
        piece_for_check_loc, move_for_check_loc, check_success_or_fail = self.ai_check()
        # gets the result for the queen capture.
        queen_piece_loc, queen_capture, queen_success_or_fail = self.ai_capture_queen()
        # gets the result for the bishop capture.
        bishop_piece_loc, bishop_capture, bishop_success_or_fail = self.ai_capture_bishop()
        # gets the result for the knight capture
        knight_piece_loc, knight_capture, knight_success_or_fail = self.ai_capture_knight()
        # gets the result for the rook capture.
        rook_piece_loc, rook_capture, rook_success_or_fail = self.ai_capture_rook()
        # gets the result for the pawn capture
        pawn_piece_loc, pawn_capture, pawn_success_or_fail = self.ai_capture_pawn()
        if piece_for_checkmate is not None:
            py, px = piece_for_checkmate
            my, mx = move_for_checkmate_loc
            if checkmate_success_or_fail:
                eaten_piece = self.get(my, mx)
                self.move(self.get(py, px), py, px, my, mx)
                return
        elif piece_for_check_loc is not None:
            py, px = piece_for_check_loc
            ky, kx = move_for_check_loc
            if check_success_or_fail:
                eaten_piece = self.get(ky, kx)
                self.move(self._board[py][px], py, px, ky, kx)
                # return f"BLACK moved {type(self.get(qy, qx)).__name__} and captures " + f"{type(eaten_piece).__name__}\n"
                return
        # this does capture queen move
        elif queen_piece_loc is not None:
            py, px = queen_piece_loc
            qy, qx = queen_capture
            if queen_success_or_fail:
                eaten_piece = self.get(py, px)
                self.move(self._board[py][px], py, px, qy, qx)
                return f"BLACK moved {type(self.get(qy, qx)).__name__} and captures " + f"{type(eaten_piece).__name__}\n"
        # this does capture bishop move
        elif bishop_piece_loc is not None:
            py, px = bishop_piece_loc
            by, bx = bishop_capture
            if bishop_success_or_fail:
                eaten_piece = self.get(by, bx)
                self.move(self._board[py][px], py, px, by, bx)
                return f"BLACK moved {type(self.get(by, bx)).__name__} and captures " + f"{type(eaten_piece).__name__}\n"
        # this does capture knight move
        elif knight_piece_loc is not None:
            py, px = knight_piece_loc
            ky, kx = knight_capture
            if knight_success_or_fail:
                eaten_piece = self.get(ky, kx)
                self.move(self._board[py][px], py, px, ky, kx)
                return f"BLACK moved {type(self.get(ky, kx)).__name__} and captures " + f"{type(eaten_piece).__name__}\n"
        # this does capture rook move
        elif rook_piece_loc is not None:
            py, px = rook_piece_loc
            ry, rx = rook_capture
            if rook_success_or_fail:
                eaten_piece = self.get(ry, rx)
                self.move(self._board[py][px], py, px, ry, rx)
                return f"BLACK moved {type(self.get(ry, rx)).__name__} and captures " + f"{type(eaten_piece).__name__}\n"
        # this does capture pawn move
        elif pawn_piece_loc is not None:
            py, px = pawn_piece_loc
            pay, pax = pawn_capture
            if pawn_success_or_fail:
                eaten_piece = self.get(pay, pax)
                self.move(self._board[py][px], py, px, pay, pax)
                return f"BLACK moved {type(self.get(pay, pax)).__name__} and captures " + f"{type(eaten_piece).__name__}\n"
        # #
        # #
        # #
        # #
        else:
            # generate a random move
            # sets success_or_fail to false so the while loop will run.
            success_or_fail = False
            # get all of the locations of the ai pieces.
            ai_piece_locations = self.get_piece_locations(Color.BLACK)
            # since success_or_fail is set to false the while loop is ran
            while not success_or_fail:
                # set the ai's valid moves to the empty list.
                all_ai_valid_moves: list[tuple[int, int]] = []
                # gets the index that will be used to pick which of the ai's pieces will be moved. This is picked by
                # getting a random index from 0 to the number of the total pieces on the board.
                index_for_piece_to_be_randomly_moved = random.randint(0, len(ai_piece_locations) - 1)
                # gets the actual location of the randomly picked piece to be moved.
                piece_to_be_moved_location = ai_piece_locations[index_for_piece_to_be_randomly_moved]
                # assigns y, and x from the location of the actual piece to be moved.
                y, x = piece_to_be_moved_location
                # Allows us to refer to the piece that has been raandomly picked by variable name actual_piece_to_be_
                # moved
                actual_piece_to_be_moved = self.get(y, x)
                # gets all the valid moves for this piece
                all_ai_valid_moves += actual_piece_to_be_moved.valid_moves(y, x)
                # if this piece has no valid moves, we will pick a random piece again. So, we will keep picking a random
                # piece until we find one that has valid moves that can be made.
                if len(all_ai_valid_moves) == 0:
                    ai_piece_locations.remove((y, x))
                    continue
                # Gets the index that will be used to pick a random move from 0 to the number of moves this piece can
                # make.
                index_for_random_move = random.randint(0, len(all_ai_valid_moves) - 1)
                # assigns the actual move that has been randomly picked to actual_random_move variable.
                actual_random_move = all_ai_valid_moves[index_for_random_move]
                # y2, x2 is the y and x location of the actual random move to be made.
                y2, x2 = actual_random_move
                # If the move was a success, then the success_or_fail variable is changed to True and the loop is exited.
                # if the move was a failure, then the move method should've undone the move that was executed
                # and success_or_fail is still false, so the loop will happen again until a move was a success meaning
                # the success_or_fail variable was changed to True.
                target = self.get(y2, x2)
                success_or_fail = self.move(actual_piece_to_be_moved, y, x, y2, x2)
            if target:
                return f"BLACK moved {type(self.get(y2, x2)).__name__} and captures " + f"{type(target).__name__}\n"
            else:
                return f"BLACK moved {type(self.get(y2, x2)).__name__}\n"

    def no_moves_left(self, color: Color) -> bool:
        """Returns a boolean representing if this color has no more possible moves left.

        Returns True if the team of this color has no more possible moves left, otherwise it returns False if there are
        still moves this team can do.

        Params:
            color (Color): A color object representing the color of the team we will be checking for."""

        # start by making sure this color isn't in check because if this color is in check then this wouldn't
        # result in a tie since check/checkmate occurred.
        if self.check(color):
            return False
        # this color isn't in check, so let's check if there's a valid move they can make.
        all_pieces = self.get_piece_locations(color)
        move_count = 0
        for piece in all_pieces:
            all_moves = piece.valid_moves(piece[0], piece[1])
            for move in all_moves:
                move_succ_or_fail = self.move(self._board[piece[0]][piece[1]], piece[0], piece[1], move[0], move[1])
                # if the move was successfully done, then undo the move so it isn't shown on the actual game board
                # and return False because this means that there is a valid move that this team color can do.
                if move_succ_or_fail:
                    self.undo()
                    return False
        return True

