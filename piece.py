from board import Square, Board

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
        pass
    
    def has_moved(self):
        return self.moved

class Bishop(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Bi" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board):
        pass
    
    def has_moved(self):
        pass

class Knight(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Kn" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board):
        pass
    
    def has_moved(self):
        pass

class Rook(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.moved = False

    def __str__(self):
        return str("Rk" + self.colour.upper())

    def piece_get_valid_moves(self, current_square: Square, board: Board) -> list:
        piece_valid_moves = []

        if(current_square.piece_on_square != Rook()):
            print("This square doesn't contain a Rook")
            return piece_valid_moves
        
        rank, file = current_square.square_rank_file()
        row, col = board.board_get_square(f"{file}{rank}") # ???????????????????????????????????????

        # Check the all the squares right of the square
        for i in range(row, 9):
            # If you find a piece of the same colour stop checking, you can't move this way -> Break the iteration

            # If you find a piece of the opposite colour -> Append the square occupied by the piece in the list, Break the iteration

            # Otherwise keep adding every square as a valid move until the end of the iteration
            pass

        # Check the all the squares left of the square
        for i in range(row, 0, -1):
            # If you find a piece of the same colour stop checking, you can't move this way -> Break the iteration

            # If you find a piece of the opposite colour -> Append the square occupied by the piece in the list, Break the iteration

            # Otherwise keep adding every square as a valid move until the end of the iteration
            pass
        
        # Check the all the squares above the square
        for j in range(col, 9):
            # If you find a piece of the same colour stop checking, you can't move this way -> Break the iteration

            # If you find a piece of the opposite colour -> Append the square occupied by the piece in the list, Break the iteration

            # Otherwise keep adding every square as a valid move until the end of the iteration
            pass

        # Check the all the squares below the square
        for j in range(col, 0, -1):
            # If you find a piece of the same colour stop checking, you can't move this way -> Break the iteration

            # If you find a piece of the opposite colour -> Append the square occupied by the piece in the list, Break the iteration

            # Otherwise keep adding every square as a valid move until the end of the iteration
            pass

        return piece_valid_moves
        
    
    def has_moved(self):
        return self.moved

class Queen(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Qu" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board):
        pass
    
    def has_moved(self):
        pass

class King(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.moved = False

    def __str__(self):
        return str("Ki" + self.colour.upper())

    def piece_get_valid_moves(self, current_square, board):
        pass
    
    def has_moved(self):
        return self.moved


if __name__ == "__main__":
    pass