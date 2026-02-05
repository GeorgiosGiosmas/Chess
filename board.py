import pawn

class Square():
    def __init__(self, rank, file, colour, piece_on_square: pawn = None):
        self.rank = rank
        self.file = file
        self.colour = colour
        self.piece_on_square = piece_on_square

    def __str__(self):
        return str(self.rank) + str(self.file)

    def is_empty(self):
        return self.piece_on_square is None


class Board():
    def __init__(self):
        rows = "abcdefgh"
        columns = "12345678"

        for row in rows:
            for col in columns:
                pass

    def print_board_state(self):
        #     -------------------------
        #  8  |  |  |  |  |  |  |  |  |
        #     -------------------------
        #  7  |  |  |  |  |  |  |  |  |
        #     -------------------------
        #  6  |  |  |  |  |  |  |  |  |
        #     -------------------------
        #  5  |  |  |  |  |  |  |  |  |
        #     -------------------------
        #  4  |  |  |  |  |  |  |  |  |
        #     -------------------------
        #  3  |  |  |  |  |  |  |  |  |
        #     -------------------------
        #  2  |  |  |  |  |  |  |  |  |
        #     -------------------------
        #  1  |  |  |  |  |  |  |  |  |
        #     -------------------------
        #      a  b  c  d  e  f  g  h  

        pass

if __name__ == "__main__":
    
    s = Square('a', 2, 'black')
    print(s)