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
        self.black_king_square = None
        self.white_king_square = None
        self.black_king_check = False
        self.white_king_check = False
        self.black_king_checkmate = False
        self.white_king_checkmate = False
        self.draw = False

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
        self.white_king_square = self.board[self.ranks.index('1')][self.files.index('e')]
        self.board[self.ranks.index('8')][self.files.index('e')].piece_on_square = King('b')
        self.black_king_square = self.board[self.ranks.index('8')][self.files.index('e')]

        # Initialize the Queens
        self.board[self.ranks.index('1')][self.files.index('d')].piece_on_square = Queen('w') 
        self.board[self.ranks.index('8')][self.files.index('d')].piece_on_square = Queen('b')

        # Initialize the Bishops
        self.board[self.ranks.index('1')][self.files.index('f')].piece_on_square = Bishop('w')
        self.board[self.ranks.index('1')][self.files.index('c')].piece_on_square = Bishop('w')
        self.board[self.ranks.index('8')][self.files.index('f')].piece_on_square = Bishop('b') 
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
    
    def get_all_pieces_moves(self, history):
        self.black_king_check = False
        self.white_king_check = False

        # First pass where we examine only the normal Piecies' moves
        for row in range(8):
            for col in range(8):
                if self.board[row][col].piece_on_square is not None and self.board[row][col].piece_on_square.__str__()[0] != 'K':
                    self.board[row][col].piece_on_square.piece_get_valid_moves(self.board[row][col] , self, history)

        # Second pass where we examine only the Kings' moves
        for row in range(8):
            for col in range(8):
                if self.board[row][col].piece_on_square is not None and self.board[row][col].piece_on_square.__str__()[0] == 'K':
                    self.board[row][col].piece_on_square.piece_get_valid_moves(self.board[row][col] , self, history)

    def is_square_attacked_by(self, square_str, colour):
        target_row = self.from_rank_get_index(square_str[1])
        target_col = self.from_file_get_index(square_str[0])
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col].piece_on_square
                if piece is not None and piece.colour == colour:
                    # For pawns, check diagonal attack squares directly
                    if piece.__str__()[0] == 'P':
                        if colour == 'w' and row + 1 == target_row and abs(col - target_col) == 1:
                            return True
                        elif colour == 'b' and row - 1 == target_row and abs(col - target_col) == 1:
                            return True
                    # For all other pieces, use valid_moves
                    elif square_str in piece.valid_moves:
                        return True
        return False
    
    def is_king_in_check_raw(self, king_pos, opponent):

        # Check from King's position if he is threatened by any piece of opponents colour 
        row, col = self.from_rank_get_index(king_pos[1]), self.from_file_get_index(king_pos[0])
        vertical_offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        diagonal_offsets = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        knights_offsets = [(1,2), (2,1), (2,-1), (1,-2), (-1,-2), (-2,-1), (-2,1), (-1,2)]
        pawns_offsets = [(-1, -1), (-1, 1)] if opponent == 'w' else [(1, -1), (1, 1)]
        kings_offsets = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for dr, dc in vertical_offsets:
            r, c = row + dr, col + dc
            while(0 <= r <= 7  and 0 <= c <= 7):
                if self.board[r][c].piece_on_square is not None:
                    if (self.board[r][c].piece_on_square.colour == opponent and self.board[r][c].piece_on_square.__str__()[0] in ('R', 'Q')):
                        return True
                    break 
                
                r += dr
                c += dc

        for dr, dc in diagonal_offsets:
            r, c = row + dr, col + dc
            while(0 <= r <= 7  and 0 <= c <= 7):
                if self.board[r][c].piece_on_square is not None:
                    if (self.board[r][c].piece_on_square.colour == opponent and self.board[r][c].piece_on_square.__str__()[0] in ('B', 'Q')):
                        return True
                    break 

                r += dr
                c += dc

        for dr, dc in knights_offsets:
            r, c = row + dr, col + dc
            if(0 <= r <= 7  and 0 <= c <= 7):
                if(self.board[r][c].piece_on_square is not None and self.board[r][c].piece_on_square.colour == opponent and self.board[r][c].piece_on_square.__str__()[0] == "N"):
                    return True

        for dr, dc in pawns_offsets:
            r, c = row + dr, col + dc
            if(0 <= r <= 7  and 0 <= c <= 7):
                if(self.board[r][c].piece_on_square is not None and self.board[r][c].piece_on_square.colour == opponent and self.board[r][c].piece_on_square.__str__()[0] == "P"):
                    return True
                
        for dr, dc in kings_offsets:
            r, c = row + dr, col + dc
            if(0 <= r <= 7  and 0 <= c <= 7):
                if(self.board[r][c].piece_on_square is not None and self.board[r][c].piece_on_square.colour == opponent and self.board[r][c].piece_on_square.__str__()[0] == "K"):
                    return True

        return False
    
    def filter_legal_moves(self, history):
        """After get_all_pieces_moves, remove any move that leaves own King in check."""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col].piece_on_square
                if piece is None:
                    continue
                
                legal_moves = []
                from_sq = self.from_index_get_file(col) + self.from_index_get_rank(row)
                
                for move in piece.valid_moves:
                    # 1. Save the current state
                    to_sq = self.board_get_square(move)
                    saved_piece = to_sq.piece_on_square
                    
                    # 2. Simulate the move
                    to_sq.piece_on_square = piece
                    self.board[row][col].piece_on_square = None
                    
                    # Update king square reference if it's a King moving
                    if piece.__str__()[0] == 'K':
                        if piece.colour == 'w':
                            old_king_sq = self.white_king_square
                            self.white_king_square = to_sq
                        else:
                            old_king_sq = self.black_king_square
                            self.black_king_square = to_sq
                    
                    # 3. Recalculate opponent attacks and check if own King is attacked
                    king_sq = self.white_king_square if piece.colour == 'w' else self.black_king_square
                    king_pos = king_sq.file + king_sq.rank
                    opponent = 'b' if piece.colour == 'w' else 'w'
                    
                    if not self.is_king_in_check_raw(king_pos, opponent):
                        legal_moves.append(move)
                    
                    # 4. Undo the move
                    self.board[row][col].piece_on_square = piece
                    to_sq.piece_on_square = saved_piece
                    
                    if piece.__str__()[0] == 'K':
                        if piece.colour == 'w':
                            self.white_king_square = old_king_sq
                        else:
                            self.black_king_square = old_king_sq
                
                piece.valid_moves = legal_moves

    def white_has_moves(self):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col].piece_on_square
                if piece is not None and piece.colour == "w" and len(piece.valid_moves) > 0:
                    return True
                
        return False

    def black_has_moves(self):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col].piece_on_square
                if piece is not None and piece.colour == "b" and len(piece.valid_moves) > 0:
                    return True
                
        return False
    
    def make_move(self, from_square: str, to_square: str, history: list):

        history_string = ""
        capture = ""
        castling = ""
        current_square = self.board_get_square(from_square)
        
        if(to_square in current_square.piece_on_square.valid_moves):
            future_square = self.board_get_square(to_square)

            if(future_square.piece_on_square is not None):
                capture = "x"
                if(future_square.piece_on_square.colour == 'b'):
                    self.captured_black_pawns.append(future_square.piece_on_square.__str__())
                else:
                    self.captured_white_pawns.append(future_square.piece_on_square.__str__())

            piece = current_square.piece_on_square.__str__()[0] # Identify only the piece. We don't care about the colour

            future_square.piece_on_square = current_square.piece_on_square
            current_square.piece_on_square = None

            # If we are castling the King, don't forget to also move the Rook
            if(piece=='K' and abs(self.files.index(to_square[0]) - self.files.index(from_square[0])) > 1):
                if(to_square == "g1"):
                    self.board[0][5].piece_on_square = self.board[0][7].piece_on_square
                    self.board[0][7].piece_on_square = None
                    castling = "0-0"
                elif(to_square == "c1"):
                    self.board[0][3].piece_on_square = self.board[0][0].piece_on_square
                    self.board[0][0].piece_on_square = None
                    castling = "0-0-0"
                elif(to_square == "g8"):
                    self.board[7][5].piece_on_square = self.board[7][7].piece_on_square
                    self.board[7][7].piece_on_square = None
                    castling = "0-0"
                elif(to_square == "c8"): 
                    self.board[7][3].piece_on_square = self.board[7][0].piece_on_square
                    self.board[7][0].piece_on_square = None
                    castling = "0-0-0"

            # If we have En Passant handle the Capture
            if(piece == 'P' and len(future_square.piece_on_square.en_passant) > 0):
                capture = "x"
                if(to_square == future_square.piece_on_square.en_passant[0]):
                    if(future_square.piece_on_square.colour == 'b'):
                        self.captured_white_pawns.append(self.board_get_square(future_square.piece_on_square.en_passant[1]).piece_on_square.__str__())
                    else:
                        self.captured_black_pawns.append(self.board_get_square(future_square.piece_on_square.en_passant[1]).piece_on_square.__str__())
                    self.board_get_square(future_square.piece_on_square.en_passant[1]).piece_on_square = None

            # Update this variable. Necassary for En Passant
            if(piece == "P" and future_square.piece_on_square.has_moved == True):
                future_square.piece_on_square.has_moved_twice = True

            # Update this variable. Necassary for En Passant and Castling
            if(piece == 'P' or piece == 'K' or piece == 'R'):
                future_square.piece_on_square.has_moved = True

            # Update the squares that point out the positions of the Kings, if they move
            if(piece == 'K' and future_square.piece_on_square.colour == 'w'):
                self.white_king_square = future_square
            if(piece == 'K' and future_square.piece_on_square.colour == 'b'):
                self.black_king_square = future_square

            # Save the new history variable
            if(piece == 'P' and capture == "x"):
                history_string = str(len(history)+1) + ". " + from_square[0] + capture + to_square + history_string
            elif(piece == 'P'):
                history_string = str(len(history)+1) + ". " + capture + to_square + history_string
            elif(castling != ""):
                history_string = str(len(history)+1) + ". " + castling + history_string
            else:
                history_string = str(len(history)+1) + ". " + piece + capture + to_square + history_string
            history.append(history_string)

            return 0
        else:
            return -1
        
    def reset(self):
        self.captured_black_pawns = []
        self.captured_white_pawns = []
        self.black_king_square = None
        self.white_king_square = None
        self.black_king_check = False
        self.white_king_check = False
        self.black_king_checkmate = False
        self.white_king_checkmate = False
        self.draw = False

        for row in range(8):
            for col in range(8):
                self.board[row][col].piece_on_square = None
        
if __name__ == "__main__":
    
    b = Board()
    b.board_initialize_pieces()
    b.print_board_state()
    a = b.board_get_square('f5')
    print(a)
    print(a.piece_on_square.piece_get_valid_moves(a ,b))