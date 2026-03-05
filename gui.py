import tkinter as tk
from tkinter import PhotoImage
from board import *
from piece import *

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


    def game_restart(self):
        pass

    def start_game(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGameGUI(root)
    root.mainloop()