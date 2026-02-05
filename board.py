import piece

class Square():
    def __init__(self, rank, file, colour, piece_on_square: piece = None):
        self.rank = rank
        self.file = file
        self.colour = colour
        self.piece_on_square = piece_on_square

    def __str__(self):
        return str(self.rank) + str(self.file) + str(self.colour)

    def is_empty(self):
        return self.piece_on_square is None
    
    def is_highlighted(self):
        pass


class Board():
    def __init__(self):
        self.captured_black_pawns = []
        self.captured_white_pawns = []
        self.board = []

        self.ranks = "abcdefgh"
        self.files = "12345678"

        for col in range(len(self.files)):
            r = []
            if col%2 == 0: colour = "b"
            else: colour = "w"
            for row in range(len(self.ranks)):
                square = Square(self.ranks[row], self.files[col], colour)
                r.append(square)
                if colour == "b": colour = "w"
                else: colour = "b"
            self.board.append(r)
                

    def print_board_state(self):
        #     -------------------------------------------------
        #  8  | a8w | b8b | c8w | d8b | e8w | f8b | g8w | h8b |
        #     -------------------------------------------------
        #  7  | a7b | b7w | c7b | d7w | e7b | f7w | g7b | h7w |
        #     -------------------------------------------------
        #  6  | a6w | b6b | c6w | d6b | e6w | f6b | g6w | h6b |
        #     -------------------------------------------------
        #  5  | a5b | b5w | c5b | d5w | e5b | f5w | g5b | h5w |
        #     -------------------------------------------------
        #  4  | a4w | b4b | c4w | d4b | e4w | f4b | g4w | h4b |
        #     -------------------------------------------------
        #  3  | a3b | b3w | c3b | d3w | e3b | f3w | g3b | h3w |
        #     -------------------------------------------------
        #  2  | a2w | b2b | c2w | d2b | e2w | f2b | g2w | h2b |
        #     -------------------------------------------------
        #  1  | a1b | b1w | c1b | d1w | e1b | f1w | g1b | h1w |
        #     -------------------------------------------------
        #        a     b     c     d     e     f     g     h  

        print("     -------------------------------------------------")
        for col in range(8):
            print(f"  {8-col}  |", end="")
            for row in range(8):
                print(f" {self.board[7-col][row]} |", end="")
            print()
            print("     -------------------------------------------------")
        print("        a     b     c     d     e     f     g     h   ")

    def board_get_square(self, square: str) -> Square:
        return self.board[self.files.index(square[1])][self.ranks.index(square[0])]

if __name__ == "__main__":
    
    b = Board()
    b.print_board_state()
    a = b.board_get_square('e6')
    print(a)