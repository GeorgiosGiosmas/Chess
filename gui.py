"""
GUI module - Generates the Graphical User Interface
for the game.

Handles erasing and drawing of the canvas after every play, 
placing of the Pieces' subimages, the move making and the 
highlighting of squares.
"""
import tkinter as tk
from tkinter import PhotoImage
from board import *
from piece import *
import math

class ChessGameGUI():
    def __init__(self, root, board: Board):
        """ Initializes some game parameters and creates the History Frame, Canvas Frames and Button Frame. """
        #### Game Parameters
        self.board = board
        self.images = {}

        #### GUI Parameters
        self.board_width, self.board_height = 720, 720
        self.piece_width, self.piece_height = 80, 80
        root.title("Chess Game")

        # History Frame 
        self.historyFrame = tk.Frame(root)
        self.historyFrame.pack()
        self.historyText = tk.StringVar()
        self.historyLabel = tk.Label(self.historyFrame, textvariable=self.historyText, font='Arial 20', width=40, height=2)
        self.historyLabel.pack(fill='x')
        
        # Main/Canvas frame
        self.mainFrame = tk.Frame(root)
        self.mainFrame.pack()
        self.canvas = tk.Canvas(self.mainFrame, width = self.board_width, height = self.board_height, bg="#928777")
        self.canvas.pack(fill='both')
        self.canvas.bind("<Button-1>", self.move_piece)
        self.draw_board()

        # Button Frame
        self.buttonFrame = tk.Frame(root)
        self.buttonFrame.pack(fill='x')
        self.gameButton = tk.Button(self.buttonFrame, text="Game Start", bg='#efefef', command=self.start_game)
        self.gameButton.pack(side='left', fill='x', expand=1)
        self.restartButton = tk.Button(self.buttonFrame, text="Restart Game", bg="#efefef", command=self.game_restart)
        self.restartButton.pack(side='right', fill='x', expand=1)

    def subimage(self, l, t, r, b):
        """ Generates a subimage of the specified piece from the spritesheet. """
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', self.spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return dst

    def generate_images_from_sprite(self):
        """ Saves the subimages of the pieces into the images dictionary for future access. """
        self.spritesheet = PhotoImage(file="images/Chess_Pieces_Sprite.gif")
        self.pieces = ['K', 'Q', 'B', 'N', 'R', 'P']
        place = 0
        for c in "WB":
            for i, p in enumerate(self.pieces):
                self.images[p+c] = self.subimage(80*i, place, 80*(i+1), 80+place)
            place += 80
    
    def draw_board(self): 
        """ This method draws the 8x8 Board on the Canvas. """
        colour = 'white'
        for rank in range(8):
            if rank%2 == 0: colour = "#b58863"
            else: colour = "#f0d9b5"
            self.canvas.create_text(40, 80*rank + 40, text=self.board.from_index_get_rank(7-rank), font=("Times New Roman", 18), fill="#333333")
            for file in range(8):
                self.canvas.create_rectangle(80*(file+1), 80*rank, 80*(file+2), 80*(rank+1), fill=colour)
                if colour == "#f0d9b5": colour = "#b58863"
                else: colour = "#f0d9b5"
        
        for i in range(8):
            self.canvas.create_text(80*(i+1)+40, 680, text=self.board.from_index_get_file(i), font=("Times New Roman", 18), fill="#333333")

    def draw_pieces(self):
        """ This method accesses the images dictionary and draws all the pieces on the Canvas. """
        self.canvas.delete("all")
        self.draw_board()
        for rank in range(8):
            for file in range(8):
                piece = self.board.board[7-rank][file].piece_on_square
                if piece != None:
                    self.canvas.create_image(80*(file+1), 80*rank, image=self.images[piece.__str__()], anchor='nw') 

    def move_piece(self, event):
        """ 
        This method handles the selection and deselection of squares, the highlighting and unhighlighting of the selected Squares,
        and the performing of moves to the newly selected squares. It also, defines the sequence of plays between Black and Whites,
        through the current_turn variable and halts the game when the winner is found. """
        self.highlight_colour = "#f7ec59"
        self.position_x, self.position_y = event.x, event.y

        if(80 <= self.position_x <= 720 and 0 <= self.position_y <= 640):
            self.new_selected_square_x, self.new_selected_square_y  = math.floor(self.position_x/80.0), math.floor(self.position_y/80.0)
            self.new_selected_square_x, self.new_selected_square_y = self.from_gui_to_board(self.new_selected_square_x, self.new_selected_square_y)

            # If the game ended, stop all moves
            if(not(self.board.white_king_checkmate or self.board.black_king_checkmate or self.board.draw)):

                # If we don't have a selected square, select it if has a piece on top of it
                if(self.selected_square is None):
                    self.highlight_square(self.new_selected_square_x, self.new_selected_square_y)
                    if(self.selected_square is not None):
                        self.highlight_valid_moves_for_selected_piece(self.selected_square.piece_on_square)

                # Pick a new square or decide the move for the selected square
                else:
                    if(self.old_selected_square_x != self.new_selected_square_x or self.old_selected_square_y != self.new_selected_square_y):
                        # If we click on another square check if it is in valid moves. If so, make the move.
                        if(self.check_if_in_valid_moves(self.new_selected_square_x, self.new_selected_square_y)):
                            current_square = self.board.from_index_get_file(self.old_selected_square_x) + self.board.from_index_get_rank(self.old_selected_square_y)
                            future_square = self.board.from_index_get_file(self.new_selected_square_x) + self.board.from_index_get_rank(self.new_selected_square_y)
                            self.board.make_move(current_square, future_square, self.history)
                            self.unhighlight_valid_moves_for_selected_piece(self.selected_square.piece_on_square)
                            self.unhighlight_square(self.old_selected_square_x, self.old_selected_square_y)
                            self.draw_pieces()

                            # Unhighlight a King if he is in check before computing get_all_pieces_moves()
                            if self.board.white_king_check: self.unhighlight_king(self.board.white_king_square)
                            if self.board.black_king_check: self.unhighlight_king(self.board.black_king_square)

                            self.board.get_all_pieces_moves(self.history)
                            self.board.filter_legal_moves(self.history)
                            self.examine()
                            self.selected_square = None

                            # Change turn
                            if(self.current_turn == 'b'): self.current_turn = 'w'
                            else: self.current_turn = 'b'

                            self.print_info()

                        # Otherwise, highlight the new square and unhighlight the previous one
                        else:
                            self.unhighlight_valid_moves_for_selected_piece(self.selected_square.piece_on_square)
                            self.unhighlight_square(self.old_selected_square_x, self.old_selected_square_y)
                            self.highlight_square(self.new_selected_square_x, self.new_selected_square_y)
                            if(self.selected_square is not None):
                                self.highlight_valid_moves_for_selected_piece(self.selected_square.piece_on_square)
                    # If we click the same unhilight it
                    else:
                        self.unhighlight_valid_moves_for_selected_piece(self.selected_square.piece_on_square)
                        self.unhighlight_square(self.old_selected_square_x, self.old_selected_square_y)
                        self.selected_square = None


    def highlight_square(self, x, y):
        """ This method highlights the specified square. """
        self.selected_square = self.board.board[y][x]
        piece = self.selected_square.piece_on_square
        if(piece is not None and piece.colour == self.current_turn):
            self.new_selected_square_x, self.new_selected_square_y = self.from_board_to_gui(x, y)
            self.redraw_square(self.selected_square, self.new_selected_square_x, self.new_selected_square_y, self.highlight_colour)
            self.new_selected_square_x, self.new_selected_square_y = self.from_gui_to_board(self.new_selected_square_x, self.new_selected_square_y)
            self.old_selected_square_x, self.old_selected_square_y = self.new_selected_square_x, self.new_selected_square_y
        else:
            self.selected_square = None

    def unhighlight_square(self, x, y):
        """ This method unhighlights the specified square. """
        old_squares_colour = self.get_square_colour(y, x)
        self.old_selected_square_x, self.old_selected_square_y = self.from_board_to_gui(x, y)
        self.redraw_square(self.selected_square, self.old_selected_square_x, self.old_selected_square_y, old_squares_colour)
        self.old_selected_square_x, self.old_selected_square_y = self.new_selected_square_x, self.new_selected_square_y

    def highlight_king(self, king_s, colour):
        """ This method highlights the specified King. """
        x, y = self.board.from_file_get_index(king_s.file), self.board.from_rank_get_index(king_s.rank)
        gui_x, gui_y = self.from_board_to_gui(x, y)
        self.redraw_square(king_s, gui_x, gui_y, colour)

    def unhighlight_king(self, king_s):
        """ This method unhighlights the specified King. """
        x, y = self.board.from_file_get_index(king_s.file), self.board.from_rank_get_index(king_s.rank)
        old_kings_colour = self.get_square_colour(y, x)
        gui_x, gui_y = self.from_board_to_gui(x, y)
        self.redraw_square(king_s, gui_x, gui_y, old_kings_colour)

    def redraw_square(self, square, x, y, colour):
        """ This method redraws a Square on the canvas with the specified colour. """
        self.canvas.create_rectangle(80*x, 80*y, 80*(x+1), 80*(y+1), fill=colour)
        piece = square.piece_on_square
        if(piece is not None):
            self.canvas.create_image(80*x, 80*y, image=self.images[piece.__str__()], anchor='nw') 

    def from_gui_to_board(self, x, y):
        """ This methods transforms GUI Coordinates(Canvas Coordinates) to Board Coordinates. """
        return x - 1, 7 - y
    
    def from_board_to_gui(self, x, y):
        """ This method transforms Board Coordinates to GUI Coordinates(Canvas Coordinates). """
        return x + 1, 7 - y
    
    def get_square_colour(self, rank, file):
        """ This method returns the original colour for the specified Square. """
        if (rank + file) % 2 == 0:
            return "#f0d9b5"
        else:
            return "#b58863"
        
    def get_square_colour_highlight(self, rank, file):
        """ This method returns the highlighting colour for the specified Square. """
        if (rank + file) % 2 == 0:
            return "#aad751"
        else:
            return "#7db83a"
    
    def highlight_valid_moves_for_selected_piece(self, piece: Piece):
        """ This method is used to illustrate valid moves for the specified Piece. """
        self.highlighted_squares = []
        for move in piece.valid_moves:
            square = self.board.board_get_square(move)
            rank, file = move[1], move[0]
            y, x = self.board.from_rank_get_index(rank), self.board.from_file_get_index(file)
            self.highlighted_squares.append((x, y))
            colour = self.get_square_colour_highlight(y, x)
            x, y = self.from_board_to_gui(x, y)
            self.redraw_square(square, x, y, colour)

    def unhighlight_valid_moves_for_selected_piece(self, piece: Piece):
        """ This method is used to unhighlight valid moves for the previous specified Piece. """
        for x, y in self.highlighted_squares:
            square = self.board.board[y][x]
            colour = self.get_square_colour(y, x)
            x, y = self.from_board_to_gui(x, y)
            self.redraw_square(square, x, y, colour)
        self.highlighted_squares = []

    def check_if_in_valid_moves(self, x, y):
        """ This method checks if the selected Square is one of the highlighted Squares(valid moves)"""
        if((x, y) in self.highlighted_squares):
            return True
        
        return False
    
    def print_info(self):
        """ This method prints necessary information about the game on the History Frame. """
        if self.board.white_king_checkmate:
            self.historyText.set("The Black won! King in Checkmate")
        elif self.board.black_king_checkmate:
            self.historyText.set("The White won! King in Checkmate")
        elif self.board.draw:
            self.historyText.set("The Game ended with a draw")
        elif self.current_turn == "w":
            self.historyText.set("The Black played: " + self.history[-1][2:])
            if(self.board.white_king_check == True):
                prev_val = self.historyText.get()
                self.historyText.set(prev_val + "\nWhite King is in check you have to protect him!")
        elif self.current_turn == "b":
            self.historyText.set("The White played: " + self.history[-1][2:])
            if(self.board.black_king_check == True):
                prev_val = self.historyText.get()
                self.historyText.set(prev_val + "\nBlack King is in check you have to protect him!")

    # Examines if we have a Check, CheckMate, or Draw
    def examine(self):
        """ Examines if we have Promotion, Check, CheckMate, or Draw, when the GUI is used. """
        # Check if either one of the two Kings is in check. If so, add + to the last move
        if(self.board.black_king_check == True):
            self.history[-1] = self.history[-1] + "+"
            self.highlight_king(self.board.black_king_square, self.check_colour)

        if(self.board.white_king_check == True):
            self.history[-1] = self.history[-1] + "+"
            self.highlight_king(self.board.white_king_square, self.check_colour)

        # Check for promotion
        for i in range(8):
            # Check for white promotion
            if(self.board.board[7][i].piece_on_square is not None and self.board.board[7][i].piece_on_square.__str__()[0] == "P"):
                    new_piece = self.promote_pawn('w')
                    match new_piece:
                        case 'R':
                            self.board.board[7][i].piece_on_square = Rook('w')
                        case 'N':
                            self.board.board[7][i].piece_on_square = Knight('w')
                        case 'B':
                            self.board.board[7][i].piece_on_square = Bishop('w')
                        case 'Q':
                            self.board.board[7][i].piece_on_square = Queen('w')
                    self.draw_pieces()
                    self.board.get_all_pieces_moves(self.history)
                    self.board.filter_legal_moves(self.history)
                    break
                  
                    
            # Check for black promotion
            elif(self.board.board[0][i].piece_on_square is not None and self.board.board[0][i].piece_on_square.__str__()[0] == "P"):
                    new_piece = self.promote_pawn('b')
                    match new_piece:
                        case 'R':
                            self.board.board[0][i].piece_on_square = Rook('b')
                        case 'N':
                            self.board.board[0][i].piece_on_square = Knight('b')
                        case 'B':
                            self.board.board[0][i].piece_on_square = Bishop('b')
                        case 'Q':
                            self.board.board[0][i].piece_on_square = Queen('b')
                    self.draw_pieces()
                    self.board.get_all_pieces_moves(self.history)
                    self.board.filter_legal_moves(self.history)
                    break
            
        # Check for Checkmate or Draw for the White King
        if(not self.board.white_has_moves()):
            if(self.board.white_king_check == True):
                self.board.white_king_checkmate = True
                self.history[-1] = self.history[-1] + "#"
                self.highlight_king(self.board.white_king_square, self.checkmate_colour)
            else:
                self.highlight_king(self.board.white_king_square, self.draw_colour)
                self.highlight_king(self.board.black_king_square, self.draw_colour)
                self.board.draw = True

        # Check for Checkmate or Draw for the Black King
        if(not self.board.black_has_moves()):
            if(self.board.black_king_check == True):
                self.board.black_king_checkmate = True
                self.history[-1] = self.history[-1] + "#"
                self.highlight_king(self.board.black_king_square, self.checkmate_colour)
            else:
                self.highlight_king(self.board.white_king_square, self.draw_colour)
                self.highlight_king(self.board.black_king_square, self.draw_colour)
                self.board.draw = True

    def promote_pawn(self, colour):
        """ This method handles the promotion of a Pawn by popping up a window and asking from the User the new Piece. """
        popup = tk.Toplevel()
        popup.title("Pawn Promotion")
        popup.update_idletasks()
        popup.grab_set()  # Makes popup modal
        
        choice = tk.StringVar(value='Q')  # Default to Queen
        
        pieces = ['Q', 'R', 'B', 'N']
        for p in pieces:
            btn = tk.Button(popup, image=self.images[p + colour.upper()],
                            command=lambda piece=p: [choice.set(piece), popup.destroy()])
            btn.pack(side='left', padx=5, pady=5)
        
        popup.wait_window()  # Blocks until popup is closed

        return choice.get()

    def start_game(self):
        """ This method is connected with the Game Start Button and initializes the game. """
        self.history = []
        self.current_turn = 'w'
        self.selected_square = None
        self.check_colour = "#e84040"
        self.checkmate_colour = "#991a1a"
        self.draw_colour = "#5a7d9a"
        self.generate_images_from_sprite()
        self.board.board_initialize_pieces()
        self.draw_pieces()
        self.board.get_all_pieces_moves(self.history)
        self.board.filter_legal_moves(self.history)
        self.historyText.set("The White play first")

    def game_restart(self):
        """ This method is connected with the Restart Game Button and resets the game. """
        self.board.reset()
        self.start_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGameGUI(root)
    root.mainloop()