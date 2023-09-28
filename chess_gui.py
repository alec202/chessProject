import pygame as pg
import pygame_gui as gui
from piece_model import *


class GUI:
    """Displays the state of the chessboard.

    Attributes:
        _game (Game): Game object holding logic of chess game.
        _screen (Display): Display for the chess game
        _pieces (image): hold image of all the pieces.
        _ui_manager (gui.UIManager): houses reset, undo, and text
        _side_box (elements): An element to be a text widget
        _undo_button (elements): Element to be a button for user to undo last performed move.
        _restart_button (elements): Element to be the button for user to restart the chess game.
        _piece_selected (bool): Boolean representing if piece has been selected.
        _first_selected (tuple[int, int]): Tuple representing the location on the board of the
             piece that's been selected.
        _valid_moves (list[tuple[int, int]]): A list of tuples representing all the valid moves for this piece.
    """
    def __init__(self) -> None:
        """Initializes the GUI instance with its components and correct initialization data.
        """
        pg.init()
        self._game = Game()
        self._screen = pg.display.set_mode((1440, 900))
        pg.display.set_caption("Chess!!!")
        self._pieces = pg.image.load("./images/pieces.png")
        self._ui_manager = gui.UIManager((1440, 900))
        self._side_box = gui.elements.UITextBox('<b>Chess!!!</b><br /><br />White moves first.<br />', relative_rect=pg.Rect((1000, 100), (400, 500)),
                                 manager=self._ui_manager)
        self._undo_button = gui.elements.UIButton(relative_rect = pg.Rect((1000, 50), (100, 50)), text='Undo',
                                     manager=self._ui_manager)
        self._restart_button = gui.elements.UIButton(relative_rect = pg.Rect((1200, 50), (100, 50)), text='Reset',
                                     manager=self._ui_manager)
        self._piece_selected = False
        self._first_selected = (0, 0)
        self._valid_moves = []

    def run_game(self) -> None:
        """Method to run the actual game"""
        running = True
        time_delta = 0
        clock = pg.time.Clock()
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    y, x = self.__get_coords__(y, x)
                    piece = self._game.get(y, x)
                    if not self._piece_selected and piece:
                        if piece.color != self._game.current_player:
                            continue
                        self._piece_selected = True
                        self._first_selected = y, x
                        self._valid_moves = piece.valid_moves(y, x)
                        self._piece_selected = piece
                    elif self._piece_selected and (y, x) in self._valid_moves:
                        target = self._game.get(y, x)
                        moved = self._game.move(self._piece_selected, self._first_selected[0], self._first_selected[1], y, x)
                        if moved:
                            self._side_box.append_html_text(self._piece_selected.color.name + ' moved '
                                                  + str(type(self._piece_selected).__name__))
                            if target:
                                self._side_box.append_html_text(' and captures ' + str(type(target).__name__))
                            self._side_box.append_html_text('<br />')
                            # computer_message = self._game._computer_move()
                            # if computer_message:
                            #     self._side_box.append_html_text(computer_message)
                        else:
                            self._side_box.append_html_text('Invalid move.  Would leave '
                                                            + str(self._piece_selected.color.name) + ' in check.<br />')
                        # if self._game.check(Color.WHITE):
                        #     self._side_box.append_html_text("WHITE is in CHECK!<br />")
                        if self._game.check(Color.BLACK):
                            self._side_box.append_html_text("BLACK is in CHECK!<br />")
                        # if self._game.mate(Color.WHITE):
                        #     self._side_box.append_html_text("WHITE is in CHECKMATE!<br />GAME OVER!")
                        if self._game.mate(Color.BLACK):
                            self._side_box.append_html_text("BLACK is in CHECKMATE!<br />GAME OVER!")
                        else:
                            if moved and not self._game.mate(Color.BLACK):
                                computer_message = self._game._computer_move()
                        if computer_message and not self._game.mate(Color.BLACK):
                            self._side_box.append_html_text(computer_message)
                        if self._game.check(Color.WHITE):
                            self._side_box.append_html_text("WHITE is in CHECK!<br />")
                        if self._game.mate(Color.WHITE):
                            self._side_box.append_html_text("WHITE is in CHECKMATE!<br />GAME OVER!")
                        self._piece_selected = False
                    else:
                        self._piece_selected = False
                if event.type == gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self._restart_button:
                        self._game.reset()
                        self._side_box.set_text("Restarting game...<br />")
                    if event.ui_element == self._undo_button:
                        if self._game.undo():
                            self._side_box.append_html_text('Undoing move.<br />')
                        else:
                            self._side_box.append_html_text('Nothing to undo.<br />')
            self._ui_manager.process_events(event)

            self._screen.fill((255, 255, 255))
            self.__draw_board__()
            self._ui_manager.draw_ui(self._screen)
            self._ui_manager.update(time_delta)

            pg.display.flip()
            time_delta = clock.tick(30) / 1000.0

    def __get_coords__(self, y: int, x: int) -> tuple[int, int]:
        """Returns two integers representing the coordinates the user clicked in a (y, x) format

        Returns: tuple of two integers that represent the coordinates of where was clicked.
            The tuple of two integers is one such that the integer at the 0th location is the y/vertical location,
            and the integer at the 1st location is the x/horizontal location."""
        grid_x = x // 105
        grid_y = y // 105
        return grid_y, grid_x

    def __draw_board__(self) -> None:
        """Draw/create board with correct colors in correct corresponding spots."""
        count = 0
        color = (255, 255, 255)
        for y in range(0, 8):
            for x in range(0, 8):
                if count % 2 == 0:
                    color = (255, 255, 255)
                else:
                    color = (127, 127, 127)
                count = count + 1
                pg.draw.rect(self._screen, color, pg.rect.Rect(x * 105, y * 105, 105, 105))
                if self._piece_selected and (y, x) == self._first_selected:
                    pg.draw.rect(self._screen, (255, 0, 0), pg.rect.Rect(x * 105, y * 105, 105, 105), 2)
                if self._valid_moves and self._piece_selected and (y, x) in self._valid_moves:
                    pg.draw.rect(self._screen, (0, 0, 255), pg.rect.Rect(x * 105, y * 105, 105, 105), 2)
                if self._game.get(y, x):
                    self._screen.blit(self._game.get(y, x)._image, (x * 105, y * 105))
            count = count + 1
        pg.draw.line(self._screen, (0, 0, 0), (0, 840), (840, 840))
        pg.draw.line(self._screen, (0, 0, 0), (840, 840), (840, 0))


def main() -> None:
    """Main function."""
    g = GUI()
    g.run_game()


if __name__ == '__main__':
    main()
