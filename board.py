from piece import King, Knight, Queen, Bishop, Rook, Pawn, Piece

class Square():
    def __init__(self, rank, file, colour, piece_on_square: Piece = None):
        self.rank = rank
        self.file = file
        self.colour = colour
        self.piece_on_square = piece_on_square

    def __str__(self):
        return str(self.rank) + str(self.file) + str(self.colour)
    
    def square_rank_file(self):
        return self.rank, self.file
    
    def occupied_by_piece(self):
        if self.piece_on_square is None: return ' E '
        else: return self.piece_on_square
    
    def is_highlighted(self):
        pass


class Board():
    def __init__(self):
        self.captured_black_pawns = []
        self.captured_white_pawns = []
        self.board = []

        self.files = "abcdefgh"
        self.ranks = "12345678"

        for row in range(len(self.ranks)):
            r = []
            if row%2 == 0: colour = "b"
            else: colour = "w"
            for col in range(len(self.files)):
                square = Square(self.ranks[row], self.files[col], colour)
                r.append(square)
                if colour == "b": colour = "w"
                else: colour = "b"
            self.board.append(r)

    def board_initialize_pieces(self):
        # Initialize the Kings
        self.board[self.ranks.index('1')][self.files.index('e')].piece_on_square = King('w')
        self.board[self.ranks.index('8')][self.files.index('e')].piece_on_square = King('b')

        # Initialize the Queens
        self.board[self.ranks.index('1')][self.files.index('d')].piece_on_square = Queen('w')
        self.board[self.ranks.index('8')][self.files.index('d')].piece_on_square = Queen('b')

        # Initialize the Bishops
        self.board[self.ranks.index('1')][self.files.index('f')].piece_on_square = Bishop('w')
        self.board[self.ranks.index('1')][self.files.index('c')].piece_on_square = Bishop('w')
        self.board[self.ranks.index('5')][self.files.index('h')].piece_on_square = Bishop('b') # ??????????????????????????????????
        self.board[self.ranks.index('8')][self.files.index('c')].piece_on_square = Bishop('b')

        # Initialize the Knights
        self.board[self.ranks.index('1')][self.files.index('g')].piece_on_square = Knight('w') 
        self.board[self.ranks.index('1')][self.files.index('b')].piece_on_square = Knight('w')
        self.board[self.ranks.index('8')][self.files.index('g')].piece_on_square = Knight('b')
        self.board[self.ranks.index('8')][self.files.index('b')].piece_on_square = Knight('b')

        # Initialize the Rooks
        self.board[self.ranks.index('1')][self.files.index('h')].piece_on_square = Rook('w') 
        self.board[self.ranks.index('1')][self.files.index('a')].piece_on_square = Rook('w')
        self.board[self.ranks.index('8')][self.files.index('h')].piece_on_square = Rook('b')
        self.board[self.ranks.index('8')][self.files.index('a')].piece_on_square = Rook('b')

        # Initialize the Pawns
        for i in range(0, 8):
            self.board[self.ranks.index('2')][i].piece_on_square = Pawn('w')
            self.board[self.ranks.index('7')][i].piece_on_square = Pawn('b')

    def demo_initialize(self):
        self.board[self.ranks.index('6')][self.files.index('e')].piece_on_square = Pawn('w')
        self.board[self.ranks.index('5')][self.files.index('f')].piece_on_square = Pawn('b')
        self.board[self.ranks.index('5')][self.files.index('d')].piece_on_square = Pawn('w')
        self.board[self.ranks.index('4')][self.files.index('e')].piece_on_square = Pawn('b')

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
        for row in range(8):
            print(f"  {8-row}  |", end="")
            for col in range(8):
                print(f" {self.board[7-row][col].occupied_by_piece()} |", end="")
            print()
            print("     -------------------------------------------------")
        print("        a     b     c     d     e     f     g     h   ")

    def board_get_square(self, square: str) -> Square:
        return self.board[self.ranks.index(square[1])][self.files.index(square[0])]
    
    def from_rank_get_index(self, rank):
        return self.ranks.index(rank)
    
    def from_index_get_rank(self, index):
        return self.ranks[index]
    
    def from_file_get_index(self, file):
        return self.files.index(file)
    
    def from_index_get_file(self, file):
        return self.files[file]
    
    def make_move(self, from_square: Square, to_square: Square):
        pass

if __name__ == "__main__":
    
    b = Board()
    b.board_initialize_pieces()
    b.demo_initialize()
    b.print_board_state()
    a = b.board_get_square('h5')
    print(a)
    print(a.piece_on_square.piece_get_valid_moves(a ,b))