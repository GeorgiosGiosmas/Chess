class Piece():
    def __init__(self, colour):
        self.colour = colour

    def piece_get_valid_moves(self, current_square, board):
        pass

    def has_moved(self):
        pass



class Pawn(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.moved = False

    def __str__(self):
        return str("Pa" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board):
        piece_valid_moves = []

        if(current_square.piece_on_square is None):
            print("Empty square")
            return

        rank, file = current_square.square_rank_file()
        row, col = board.from_rank_get_index(rank), board.from_file_get_index(file)

        # The white pawns move vertically upwards
        if(current_square.piece_on_square.colour == 'w'):

            if (row + 1) <= 7 and board.board[row + 1][col].piece_on_square is None:
                piece_valid_moves.append(board.from_index_get_file(col) + board.from_index_get_rank(row + 1))
            
                # If pawn hasn't moved yet it can go up two squares if it is desired 
                if(row == 1):
                    if board.board[row + 2][col].piece_on_square is None:
                        piece_valid_moves.append(board.from_index_get_file(col) + board.from_index_get_rank(row + 2))

            # The pawn captures diagonally
            if (row + 1) <= 7 and (col + 1) <= 7 and board.board[row + 1][col + 1].piece_on_square is not None and board.board[row + 1][col + 1].piece_on_square.colour != current_square.piece_on_square.colour:
                    piece_valid_moves.append(board.from_index_get_file(col + 1) + board.from_index_get_rank(row + 1))
            if (row + 1) <= 7 and (col - 1) >= 0 and board.board[row + 1][col - 1].piece_on_square is not None and board.board[row + 1][col - 1].piece_on_square.colour != current_square.piece_on_square.colour:
                    piece_valid_moves.append(board.from_index_get_file(col - 1) + board.from_index_get_rank(row + 1))

            # En Passant -> Later ...

            # Promotion -> Later ...

        # The black pawns move vertically downwards
        else:

            if (row - 1) >= 0 and board.board[row - 1][col].piece_on_square is None:
                piece_valid_moves.append(board.from_index_get_file(col) + board.from_index_get_rank(row - 1))
            
                # If pawn hasn't moved yet it can go up two squares if it is desired 
                if(row == 6):
                    if board.board[row - 2][col].piece_on_square is None:
                        piece_valid_moves.append(board.from_index_get_file(col) + board.from_index_get_rank(row - 2))

            # The pawn captures diagonally
            if (row - 1) >= 0 and (col - 1) >= 0 and board.board[row - 1][col - 1].piece_on_square is not None and board.board[row - 1][col - 1].piece_on_square.colour != current_square.piece_on_square.colour:
                    piece_valid_moves.append(board.from_index_get_file(col - 1) + board.from_index_get_rank(row - 1))
            if (row - 1) >= 0 and (col + 1) <= 7 and board.board[row - 1][col + 1].piece_on_square is not None and board.board[row - 1][col + 1].piece_on_square.colour != current_square.piece_on_square.colour:
                    piece_valid_moves.append(board.from_index_get_file(col + 1) + board.from_index_get_rank(row - 1))


            # En Passant -> Later ...

            # Promotion -> Later ...

        return piece_valid_moves
    
    def has_moved(self):
        return self.moved

class Bishop(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Bi" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board):
        piece_valid_moves = []

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
                        piece_valid_moves.append(board.from_index_get_file(c) + board.from_index_get_rank(r))
                        break

                # Otherwise keep adding every square as a valid move until the end of the iteration
                else:
                    piece_valid_moves.append(board.from_index_get_file(c) + board.from_index_get_rank(r))

                r += dr
                c += dc

        return piece_valid_moves
    
    def has_moved(self):
        pass

class Knight(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Kn" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board):
        piece_valid_moves = []

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
                if board.board[a][b].piece_on_square is None or board.board[a][b].piece_on_square.colour != current_square.piece_on_square.colour:
                    piece_valid_moves.append(board.from_index_get_file(b) + board.from_index_get_rank(a))

        return piece_valid_moves
    
    def has_moved(self):
        pass

class Rook(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.moved = False

    def __str__(self):
        return str("Rk" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board) -> list:
        piece_valid_moves = []

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
                        piece_valid_moves.append(board.from_index_get_file(c) + board.from_index_get_rank(r))
                        break

                # Otherwise keep adding every square as a valid move until the end of the iteration
                else:
                    piece_valid_moves.append(board.from_index_get_file(c) + board.from_index_get_rank(r))

                r += dr
                c += dc

        return piece_valid_moves
        
    
    def has_moved(self):
        return self.moved

class Queen(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Qu" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board):
        piece_valid_moves = []

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
                        piece_valid_moves.append(board.from_index_get_file(c) + board.from_index_get_rank(r))
                        break

                # Otherwise keep adding every square as a valid move until the end of the iteration
                else:
                    piece_valid_moves.append(board.from_index_get_file(c) + board.from_index_get_rank(r))

                r += dr
                c += dc

        return piece_valid_moves

    
    def has_moved(self):
        pass

class King(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.moved = False

    def __str__(self):
        return str("Ki" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board):
        piece_valid_moves = []

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
                if board.board[a][b].piece_on_square is None or board.board[a][b].piece_on_square.colour != current_square.piece_on_square.colour:
                    piece_valid_moves.append(board.from_index_get_file(b) + board.from_index_get_rank(a))

        return piece_valid_moves
    
    def has_moved(self):
        return self.moved


if __name__ == "__main__":
    pass