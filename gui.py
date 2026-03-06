import tkinter as tk
from tkinter import PhotoImage
from board import *
from piece import *
import math

class ChessGameGUI():
    def __init__(self, root, board: Board):
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
        self.historyLabel = tk.Label(self.historyFrame, textvariable=self.historyText, font='Arial 20', width=40)
        self.historyLabel.pack(fill='x')
        
        # Main/Canvas frame
        self.mainFrame = tk.Frame(root)
        self.mainFrame.pack()
        self.canvas = tk.Canvas(self.mainFrame, width = self.board_width, height = self.board_height, bg="#928777")
        self.canvas.pack(fill='both')
        self.canvas.bind("<Button-1>", self.move_piece)
        self.draw_board()
        self.draw_pieces()

        # Button Frame
        self.buttonFrame = tk.Frame(root)
        self.buttonFrame.pack(fill='x')
        self.gameButton = tk.Button(self.buttonFrame, text="Game Start", bg='#efefef', command=self.start_game)
        self.gameButton.pack(side='left', fill='x', expand=1)
        self.restartButton = tk.Button(self.buttonFrame, text="Restart Game", bg="#efefef", command=self.game_restart)
        self.restartButton.pack(side='right', fill='x', expand=1)

    def subimage(self, l, t, r, b):
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', self.spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return dst

    def generate_images_from_sprite(self):
        self.spritesheet = PhotoImage(file="Chess_Pieces_Sprite.gif")
        self.pieces = ['K', 'Q', 'B', 'N', 'R', 'P']
        place = 0
        for c in "WB":
            for i, p in enumerate(self.pieces):
                self.images[p+c] = self.subimage(80*i, place, 80*(i+1), 80+place)
            place += 80
    
    def draw_board(self):
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
        self.generate_images_from_sprite()
        self.board.board_initialize_pieces()

        for rank in range(8):
            for file in range(8):
                piece = self.board.board[7-rank][file].piece_on_square
                if piece != None:
                    self.canvas.create_image(80*(file+1), 80*rank, image=self.images[piece.__str__()], anchor='nw') 

    def move_piece(self, event):
        self.highlight_colour = "#f7ec59"
        self.position_x, self.position_y = event.x, event.y

        if(80 <= self.position_x <= 720 and 0 <= self.position_y <= 640):
            self.new_selected_square_x, self.new_selected_square_y  = math.floor(self.position_x/80.0), math.floor(self.position_y/80.0)
            self.new_selected_square_x, self.new_selected_square_y = self.from_gui_to_board(self.new_selected_square_x, self.new_selected_square_y)

            # If we don't have a selected square select it if has a piece on top of it
            if(self.selected_square is None):
                self.selected_square = self.board.board[self.new_selected_square_y][self.new_selected_square_x]
                piece = self.selected_square.piece_on_square
                if(piece is not None):
                    self.redraw_square(self.selected_square, self.new_selected_square_x, self.new_selected_square_y, self.highlight_colour)
                    self.old_selected_square_x, self.old_selected_square_y = self.new_selected_square_x, self.new_selected_square_y

            # Pick a new square or decide the move for the selected square
            else:
                # If we click on another square with our piece highlight it and reverse the highlighted square to its original colour



            # Check if it already highlighted. If it is reverse it to its original colour
            if(self.highlight_colour == self.squares_colour):
                self.new_selected_square_x, self.new_selected_square_y = self.from_board_to_gui(self.new_selected_square_x, self.new_selected_square_y)
                self.redraw_square(self.selected_square, self.new_selected_square_x, self.new_selected_square_y, self.squares_original_colour)
                
            # If square it is not highlighed, highlight it
            else:
                self.new_selected_square_x, self.new_selected_square_y = self.from_board_to_gui(self.new_selected_square_x, self.new_selected_square_y)
                self.redraw_square(self.selected_square, self.new_selected_square_x, self.new_selected_square_y, self.highlight_colour)
                self.squares_original_colour = self.squares_colour
            
            # If the square is not the highlighted square, reverse the highlighed square to its original colour and highlight the new one

    def redraw_square(self, square, x, y, colour):
        self.canvas.create_rectangle(80*x, 80*y, 80*(x+1), 80*(y+1), fill=colour)
        piece = square.piece_on_square
        if(piece is not None):
            self.canvas.create_image(80*x, 80*y, image=self.images[piece.__str__()], anchor='nw') 

    def from_gui_to_board(self, x, y):
        return x - 1, 7 - y
    
    def from_board_to_gui(self, x, y):
        return x + 1, 7 - y
    
    def get_square_colour(self, rank, file):
        if (rank + file) % 2 == 0:
            return "#b58863"
        else:
            return "#f0d9b5"

    def start_game(self):
        pass

    def game_restart(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGameGUI(root)
    root.mainloop()