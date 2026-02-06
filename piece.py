class Piece():
    def __init__(self, colour):
        self.colour = colour

    def piece_get_valid_moves(self):
        pass

    def move(self):
        pass


class Pawn(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Pa" + self.colour)

    def piece_get_valid_moves(self):
        pass
    
    def move(self):
        pass

class Bishop(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Bi" + self.colour)

    def piece_get_valid_moves(self):
        pass
    
    def move(self):
        pass

class Knight(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Kn" + self.colour)

    def piece_get_valid_moves(self):
        pass
    
    def move(self):
        pass

class Rook(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Rk" + self.colour)
    
    def piece_get_valid_moves(self):
        pass
    
    def move(self):
        pass

class Queen(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Qu" + self.colour)

    def piece_get_valid_moves(self):
        pass
    
    def move(self):
        pass

class King(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Ki" + self.colour)

    def piece_get_valid_moves(self):
        pass
    
    def move(self):
        pass


if __name__ == "__main__":
    pass