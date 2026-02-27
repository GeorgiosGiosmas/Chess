class Piece():
    def __init__(self, colour):
        self.colour = colour
        self.valid_moves = []

    def piece_get_valid_moves(self, current_square, board, history):
        pass


class Pawn(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.has_moved = False
        self.has_moved_twice = False
        self.en_passant = []

    def __str__(self):
        return str("P" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board, history):
        self.valid_moves = []
        self.en_passant = []

        if(current_square.piece_on_square is None):
            print("Empty square")
            return
        
        rank, file = current_square.square_rank_file()
        row, col = board.from_rank_get_index(rank), board.from_file_get_index(file)

        # The white pawns move vertically upwards
        if(current_square.piece_on_square.colour == 'w'):

            if (row + 1) <= 7 and board.board[row + 1][col].piece_on_square is None:
                self.valid_moves.append(board.from_index_get_file(col) + board.from_index_get_rank(row + 1))
            
                # If pawn hasn't moved yet it can go up two squares if it is desired 
                if(row == 1):
                    if board.board[row + 2][col].piece_on_square is None:
                        self.valid_moves.append(board.from_index_get_file(col) + board.from_index_get_rank(row + 2))

            # The pawn captures diagonally
            if (row + 1) <= 7 and (col + 1) <= 7 and board.board[row + 1][col + 1].piece_on_square is not None and board.board[row + 1][col + 1].piece_on_square.colour != current_square.piece_on_square.colour:
                # Examine if this move checks the opponent's King
                if(board.board[row+1][col+1].piece_on_square.__str__()[0] == "K" and board.board[row+1][col+1].piece_on_square.colour != current_square.piece_on_square.colour):
                    if(current_square.piece_on_square.colour == 'w'):
                        board.black_king_check = True
                    else:
                        board.white_king_check = True
                self.valid_moves.append(board.from_index_get_file(col + 1) + board.from_index_get_rank(row + 1))
            if (row + 1) <= 7 and (col - 1) >= 0 and board.board[row + 1][col - 1].piece_on_square is not None and board.board[row + 1][col - 1].piece_on_square.colour != current_square.piece_on_square.colour:
                # Examine if this move checks the opponent's King
                if(board.board[row+1][col-1].piece_on_square.__str__()[0] == "K" and board.board[row+1][col-1].piece_on_square.colour != current_square.piece_on_square.colour):
                    if(current_square.piece_on_square.colour == 'w'):
                        board.black_king_check = True
                    else:
                        board.white_king_check = True
                self.valid_moves.append(board.from_index_get_file(col - 1) + board.from_index_get_rank(row + 1))

            # En Passant
            if(row == 4 and len(history) > 0):
                if(col - 1 >= 0):
                    ep1 = board.from_index_get_file(col-1) + rank
                    if(history[-1].split()[-1] == ep1 and board.board[row][col-1].piece_on_square.has_moved_twice == False):
                        self.valid_moves.append(board.from_index_get_file(col - 1) + board.from_index_get_rank(row + 1))
                        self.en_passant.append(board.from_index_get_file(col - 1) + board.from_index_get_rank(row + 1))  # Append en passant move en_passant[0]
                        self.en_passant.append(board.from_index_get_file(col - 1) + board.from_index_get_rank(row)) # Append pawn to be captured en_passant[1]

                if(col + 1 <= 7):
                    ep2 = board.from_index_get_file(col+1) + rank
                    if(history[-1].split()[-1] == ep2 and board.board[row][col+1].piece_on_square.has_moved_twice == False):
                        self.valid_moves.append(board.from_index_get_file(col + 1) + board.from_index_get_rank(row + 1))
                        self.en_passant.append(board.from_index_get_file(col + 1) + board.from_index_get_rank(row + 1))  # Append en passant move en_passant[0]
                        self.en_passant.append(board.from_index_get_file(col + 1) + board.from_index_get_rank(row)) # Append pawn to be captured en_passant[1]

        # The black pawns move vertically downwards
        else:

            if (row - 1) >= 0 and board.board[row - 1][col].piece_on_square is None:
                self.valid_moves.append(board.from_index_get_file(col) + board.from_index_get_rank(row - 1))
            
                # If pawn hasn't moved yet it can go up two squares if it is desired 
                if(row == 6):
                    if board.board[row - 2][col].piece_on_square is None:
                        self.valid_moves.append(board.from_index_get_file(col) + board.from_index_get_rank(row - 2))

            # The pawn captures diagonally
            if (row - 1) >= 0 and (col - 1) >= 0 and board.board[row - 1][col - 1].piece_on_square is not None and board.board[row - 1][col - 1].piece_on_square.colour != current_square.piece_on_square.colour:
                # Examine if this move checks the opponent's King
                if(board.board[row-1][col-1].piece_on_square.__str__()[0] == "K" and board.board[row-1][col-1].piece_on_square.colour != current_square.piece_on_square.colour):
                    if(current_square.piece_on_square.colour == 'w'):
                        board.black_king_check = True
                    else:
                        board.white_king_check = True    
                self.valid_moves.append(board.from_index_get_file(col - 1) + board.from_index_get_rank(row - 1))
            if (row - 1) >= 0 and (col + 1) <= 7 and board.board[row - 1][col + 1].piece_on_square is not None and board.board[row - 1][col + 1].piece_on_square.colour != current_square.piece_on_square.colour:
                # Examine if this move checks the opponent's King
                if(board.board[row-1][col+1].piece_on_square.__str__()[0] == "K" and board.board[row-1][col+1].piece_on_square.colour != current_square.piece_on_square.colour):
                    if(current_square.piece_on_square.colour == 'w'):
                        board.black_king_check = True
                    else:
                        board.white_king_check = True
                self.valid_moves.append(board.from_index_get_file(col + 1) + board.from_index_get_rank(row - 1))

            # En Passant
            if(row == 3 and len(history) > 0):
                if(col - 1 >= 0):
                    ep1 = board.from_index_get_file(col-1) + rank
                    if(history[-1].split()[-1] == ep1 and board.board[row][col-1].piece_on_square.has_moved_twice == False):
                        self.valid_moves.append(board.from_index_get_file(col - 1) + board.from_index_get_rank(row - 1))
                        self.en_passant.append(board.from_index_get_file(col - 1) + board.from_index_get_rank(row - 1))  # Append en passant move en_passant[0]
                        self.en_passant.append(board.from_index_get_file(col - 1) + board.from_index_get_rank(row)) # Append pawn to be captured en_passant[1]

                if(col + 1 <= 7):
                    ep2 = board.from_index_get_file(col+1) + rank
                    if(history[-1].split()[-1] == ep2 and board.board[row][col+1].piece_on_square.has_moved_twice == False):
                        self.valid_moves.append(board.from_index_get_file(col + 1) + board.from_index_get_rank(row - 1))
                        self.en_passant.append(board.from_index_get_file(col + 1) + board.from_index_get_rank(row - 1))  # Append en passant move en_passant[0]
                        self.en_passant.append(board.from_index_get_file(col + 1) + board.from_index_get_rank(row)) # Append pawn to be captured en_passant[1]

        return self.valid_moves

class Bishop(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("B" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board, history):
        self.valid_moves = []

        if(current_square.piece_on_square is None):
            print("Empty square")
            return

        offsets = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        rank, file = current_square.square_rank_file()
        row, col = board.from_rank_get_index(rank), board.from_file_get_index(file)

        for dr, dc in offsets:
            r, c = row + dr, col + dc

            while 0 <= r <= 7 and 0 <= c <= 7:
                if board.board[r][c].piece_on_square is not None:
                    # If you find a piece of the same colour stop checking, you can't move this way -> Break the iteration
                    if board.board[r][c].piece_on_square.colour == current_square.piece_on_square.colour:
                        break

                    # If you find a piece of the opposite colour -> Append the square occupied by the piece in the list, Break the iteration
                    else:
                        # Examine if this move checks the opponent's King
                        if(board.board[r][c].piece_on_square.__str__()[0] == "K" and board.board[r][c].piece_on_square.colour != current_square.piece_on_square.colour):
                            if(current_square.piece_on_square.colour == 'w'):
                                board.black_king_check = True
                            else:
                                board.white_king_check = True
                            self.valid_moves.append(board.from_index_get_file(c) + board.from_index_get_rank(r))
                        else:
                            self.valid_moves.append(board.from_index_get_file(c) + board.from_index_get_rank(r))
                            break

                # Otherwise keep adding every square as a valid move until the end of the iteration
                else:
                    self.valid_moves.append(board.from_index_get_file(c) + board.from_index_get_rank(r))

                r += dr
                c += dc

        return self.valid_moves

class Knight(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("N" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board, history):
        self.valid_moves = []

        if(current_square.piece_on_square is None):
            print("Empty square")
            return

        rank, file = current_square.square_rank_file()
        row, col = board.from_rank_get_index(rank), board.from_file_get_index(file)

        # Check which of the 8 possible moves are valid
        offsets = [(1,2), (2,1), (2,-1), (1,-2), (-1,-2), (-2,-1), (-2,1), (-1,2)]
        for da, db in offsets:
            a, b = row + da, col + db
            if(0 <= a <= 7  and 0 <= b <= 7):
                # Examine if this move checks the opponent's King
                if(board.board[a][b].piece_on_square is not None and board.board[a][b].piece_on_square.__str__()[0] == "K" and board.board[a][b].piece_on_square != current_square.piece_on_square.colour):
                    if(current_square.piece_on_square.colour == 'w'):
                        board.black_king_check = True
                    else:
                        board.white_king_check = True
                if board.board[a][b].piece_on_square is None or board.board[a][b].piece_on_square.colour != current_square.piece_on_square.colour:
                    self.valid_moves.append(board.from_index_get_file(b) + board.from_index_get_rank(a))

        return self.valid_moves

class Rook(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.has_moved = False

    def __str__(self):
        return str("R" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board, history) -> list:
        self.valid_moves = []

        if(current_square.piece_on_square is None):
            print("Empty square")
            return
        
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        rank, file = current_square.square_rank_file()
        row, col = board.from_rank_get_index(rank), board.from_file_get_index(file)

        for dr, dc in offsets:
            r, c = row + dr, col + dc

            while 0 <= r <= 7 and 0 <= c <= 7:
                if board.board[r][c].piece_on_square is not None:
                    # If you find a piece of the same colour stop checking, you can't move this way -> Break the iteration
                    if board.board[r][c].piece_on_square.colour == current_square.piece_on_square.colour:
                        break

                    # If you find a piece of the opposite colour -> Append the square occupied by the piece in the list, Break the iteration
                    else:
                        # Examine if this move checks the opponent's King
                        if(board.board[r][c].piece_on_square.__str__()[0] == "K" and board.board[r][c].piece_on_square.colour != current_square.piece_on_square.colour):
                            if(current_square.piece_on_square.colour == 'w'):
                                board.black_king_check = True
                            else:
                                board.white_king_check = True
                            self.valid_moves.append(board.from_index_get_file(c) + board.from_index_get_rank(r))
                        else:
                            self.valid_moves.append(board.from_index_get_file(c) + board.from_index_get_rank(r))
                            break

                # Otherwise keep adding every square as a valid move until the end of the iteration
                else:
                    self.valid_moves.append(board.from_index_get_file(c) + board.from_index_get_rank(r))

                r += dr
                c += dc

        return self.valid_moves

class Queen(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Q" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board, history):
        self.valid_moves = []

        if(current_square.piece_on_square is None):
            print("Empty square")
            return

        rank, file = current_square.square_rank_file()
        row, col = board.from_rank_get_index(rank), board.from_file_get_index(file)
        
        offsets = [(1, 1), (1, -1), (-1, -1), (-1, 1), (1, 0), (-1, 0), (0, 1), (0, -1)]

        rank, file = current_square.square_rank_file()
        row, col = board.from_rank_get_index(rank), board.from_file_get_index(file)

        for dr, dc in offsets:
            r, c = row + dr, col + dc

            while 0 <= r <= 7 and 0 <= c <= 7:
                if board.board[r][c].piece_on_square is not None:
                    # If you find a piece of the same colour stop checking, you can't move this way -> Break the iteration
                    if board.board[r][c].piece_on_square.colour == current_square.piece_on_square.colour:
                        break

                    # If you find a piece of the opposite colour -> Append the square occupied by the piece in the list, Break the iteration
                    else:
                        # Examine if this move checks the opponent's King
                        if(board.board[r][c].piece_on_square.__str__()[0] == "K" and board.board[r][c].piece_on_square.colour != current_square.piece_on_square.colour):
                            if(current_square.piece_on_square.colour == 'w'):
                                board.black_king_check = True
                            else:
                                board.white_king_check = True
                            self.valid_moves.append(board.from_index_get_file(c) + board.from_index_get_rank(r))
                        else:
                            self.valid_moves.append(board.from_index_get_file(c) + board.from_index_get_rank(r))
                            break

                # Otherwise keep adding every square as a valid move until the end of the iteration
                else:
                    self.valid_moves.append(board.from_index_get_file(c) + board.from_index_get_rank(r))

                r += dr
                c += dc

        return self.valid_moves

class King(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.has_moved = False

    def __str__(self):
        return str("K" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board, history):
        self.valid_moves = []

        if(current_square.piece_on_square is None):
            print("Empty square")
            return

        rank, file = current_square.square_rank_file()
        row, col = board.from_rank_get_index(rank), board.from_file_get_index(file)

        # Check which of the 8 possible moves are valid
        offsets = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for da, db in offsets:
            a, b = row + da, col + db
            if(0 <= a <= 7  and 0 <= b <= 7):
                if(board.board[a][b].piece_on_square is None or board.board[a][b].piece_on_square.colour != current_square.piece_on_square.colour):
                    if(self.colour == 'w' and not board.is_square_attacked_by(board.from_index_get_file(b) + board.from_index_get_rank(a), 'b')):
                        self.valid_moves.append(board.from_index_get_file(b) + board.from_index_get_rank(a))
                    elif(self.colour == 'b' and not board.is_square_attacked_by(board.from_index_get_file(b) + board.from_index_get_rank(a), 'w')):
                        self.valid_moves.append(board.from_index_get_file(b) + board.from_index_get_rank(a))

        # Check fo Castling if available
        if(not self.has_moved):
            if(self.colour == 'w' and not board.white_king_check):
                if(board.board_get_square("f1").piece_on_square is None and not board.is_square_attacked_by('f1', 'b') and board.board_get_square("g1").piece_on_square is None and not board.is_square_attacked_by('g1', 'b')):
                    h1 = board.board_get_square("h1").piece_on_square
                    if(h1 is not None and h1.__str__()[0] == "R" and h1.has_moved == False and h1.colour == "w"):
                        self.valid_moves.append(board.from_index_get_file(6) + board.from_index_get_rank(0))
                if(board.board_get_square("d1").piece_on_square is None and not board.is_square_attacked_by('d1', 'b') and board.board_get_square("c1").piece_on_square is None and not board.is_square_attacked_by('c1', 'b') and board.board_get_square("b1").piece_on_square is None):
                    a1 = board.board_get_square("a1").piece_on_square
                    if(a1 is not None and a1.__str__()[0] == "R" and a1.has_moved == False and a1.colour == "w"):
                        self.valid_moves.append(board.from_index_get_file(2) + board.from_index_get_rank(0))
            elif(self.colour == 'b' and not board.black_king_check):
                if(board.board_get_square("f8").piece_on_square is None and not board.is_square_attacked_by('f8', 'w') and board.board_get_square("g8").piece_on_square is None and not board.is_square_attacked_by('g8', 'w')):
                    h8 = board.board_get_square("h8").piece_on_square
                    if(h8 is not None and h8.__str__()[0] == "R" and h8.has_moved == False and h8.colour == "b"):
                        self.valid_moves.append(board.from_index_get_file(6) + board.from_index_get_rank(7))
                if(board.board_get_square("d8").piece_on_square is None and not board.is_square_attacked_by('d8', 'w') and board.board_get_square("c8").piece_on_square is None and not board.is_square_attacked_by('c8', 'w') and board.board_get_square("b8").piece_on_square is None):
                    a8 = board.board_get_square("a8").piece_on_square
                    if(a8 is not None and a8.__str__()[0] == "R" and a8.has_moved == False and a8.colour == "b"):
                        self.valid_moves.append(board.from_index_get_file(2) + board.from_index_get_rank(7))

        return self.valid_moves

if __name__ == "__main__":
    pass