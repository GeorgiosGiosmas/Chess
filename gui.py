import tkinter as tk
from tkinter import PhotoImage

class ChessGameGUI():
    def __init__(self, root):
        #### Game Parameters


        #### GUI Parameters
        self.board_width, self.board_height = 640, 640
        self.piece_width, self.piece_height = 80, 80
        root.title("Chess Game")
        self.historyFrame = tk.Frame(root)
        self.historyFrame.pack()
        self.historyText = tk.StringVar()
        self.historyLabel = tk.Label(self.historyFrame, textvariable=self.historyText, font='Arial 20', width=40)
        self.historyLabel.pack()
        self.mainFrame = tk.Frame(root)
        self.mainFrame.pack()
        self.canvas = tk.Canvas(self.mainFrame, width = self.board_width, height = self.board_height, bg='grey')
        self.canvas.pack()
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
        self.num_sprites = 6
        self.pieces = []
        place = 0
        self.images = {}
        for x in "WB":
            self.images[x] = [self.subimage(45*i, place, 45*(i+1), 45+place) for i in range(self.num_sprites)]
            place += 45

    def game_restart(self):
        pass

    def start_game(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGameGUI(root)
    root.mainloop()