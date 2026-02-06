class Piece():
    def __init__(self, colour):
        self.colour = colour

    def piece_get_valid_moves(self):
        pass

    def has_moved(self):
        pass



class Pawn(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.moved = False

    def __str__(self):
        return str("Pa" + self.colour.upper())

    def piece_get_valid_moves(self):
        pass
    
    def has_moved(self):
        return self.moved

class Bishop(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Bi" + self.colour.upper())

    def piece_get_valid_moves(self):
        pass
    
    def has_moved(self):
        pass

class Knight(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Kn" + self.colour.upper())

    def piece_get_valid_moves(self):
        pass
    
    def has_moved(self):
        pass

class Rook(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.moved = False

    def __str__(self):
        return str("Rk" + self.colour.upper())
    
    def piece_get_valid_moves(self):
        pass
    
    def has_moved(self):
        return self.moved

class Queen(Piece):
    def __init__(self, colour):
        super().__init__(colour)

    def __str__(self):
        return str("Qu" + self.colour.upper())

    def piece_get_valid_moves(self):
        pass
    
    def has_moved(self):
        pass

class King(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.moved = False

    def __str__(self):
        return str("Ki" + self.colour.upper())

    def piece_get_valid_moves(self):
        pass
    
    def has_moved(self):
        return self.moved


if __name__ == "__main__":
    pass