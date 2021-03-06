import pieces, ai

class Board:

    WIDTH = 8
    HEIGHT = 8

    def __init__(self, pieces, white_king_moved, black_king_moved):
        self.pieces = pieces
        self.white_king_moved = white_king_moved
        self.black_king_moved = black_king_moved

    @classmethod
    def clone(cls, board):
        pieces = [[0 for x in range(Board.WIDTH)] for y in range(Board.HEIGHT)]
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = board.pieces[x][y]
                if (piece != 0):
                    pieces[x][y] = piece.clone()
        return cls(pieces, board.white_king_moved, board.black_king_moved)

    @classmethod
    def new(cls):
        chess_pieces = [[0 for x in range(Board.WIDTH)] for y in range(Board.HEIGHT)]
        # Create pawns.
        for y in range(Board.WIDTH):
            chess_pieces[1][y] = pieces.Pawn(1, y, pieces.Piece.WHITE)
            chess_pieces[Board.WIDTH-2][y] = pieces.Pawn(Board.WIDTH-2, y, pieces.Piece.BLACK)

        # Create rooks.
        chess_pieces[0][0] = pieces.Rook(0, 0, pieces.Piece.WHITE)
        chess_pieces[0][Board.HEIGHT-1] = pieces.Rook(0, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-1][0] = pieces.Rook(Board.WIDTH-1, 0, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-1][Board.HEIGHT-1] = pieces.Rook(Board.WIDTH-1, Board.HEIGHT-1, pieces.Piece.BLACK)

        # Create Knights.
        chess_pieces[0][1] = pieces.Knight(0, 1, pieces.Piece.WHITE)
        chess_pieces[0][Board.HEIGHT-2] = pieces.Knight(0, Board.HEIGHT-2, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-1][1] = pieces.Knight(Board.WIDTH-1, 1, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-1][Board.HEIGHT-2] = pieces.Knight(Board.WIDTH-1, Board.HEIGHT-2, pieces.Piece.BLACK)

        # Create Bishops.
        chess_pieces[0][2] = pieces.Bishop(0, 2, pieces.Piece.WHITE)
        chess_pieces[0][Board.HEIGHT-3] = pieces.Bishop(0, Board.HEIGHT-3, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-1][2] = pieces.Bishop(Board.WIDTH-1, 2, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-1][Board.HEIGHT-3] = pieces.Bishop(Board.WIDTH-1, Board.HEIGHT-3, pieces.Piece.BLACK)

        # Create King & Queen.
        chess_pieces[0][3] = pieces.King(0, 3, pieces.Piece.WHITE)
        chess_pieces[0][Board.HEIGHT-4] = pieces.Queen(0, Board.HEIGHT-4, pieces.Piece.WHITE)
        chess_pieces[Board.WIDTH-1][3] = pieces.King(Board.WIDTH-1, 3, pieces.Piece.BLACK)
        chess_pieces[Board.WIDTH-1][Board.HEIGHT-4] = pieces.Queen(Board.WIDTH-1, Board.HEIGHT-4, pieces.Piece.BLACK)

        return cls(chess_pieces, False, False)

    def get_possible_moves(self, color):
        moves = []
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = self.pieces[x][y]
                if (piece != 0):
                    if (piece.color == color):
                        moves += piece.get_possible_moves(self)

        return moves

    def perform_move(self, move):
        piece = self.pieces[move.xfrom][move.yfrom]
        piece.x = move.xto
        piece.y = move.yto
        self.pieces[move.xto][move.yto] = piece
        self.pieces[move.xfrom][move.yfrom] = 0

        if (piece.piece_type == pieces.Pawn.PIECE_TYPE):
            if (piece.x == 0 or piece.x == Board.WIDTH-1):
                self.pieces[piece.x][piece.y] = pieces.Queen(piece.x, piece.y, piece.color)

        if (move.castling_move):
            if (move.yto < move.yfrom):
                rook = self.pieces[move.xfrom][0]
                rook.y = 2
                self.pieces[move.xfrom][2] = rook
                self.pieces[move.xfrom][0] = 0
            if (move.yto > move.yfrom):
                rook = self.pieces[move.xfrom][Board.HEIGHT-1]
                rook.y = Board.HEIGHT-4
                self.pieces[move.xfrom][Board.HEIGHT-4] = rook
                self.pieces[move.xfrom][Board.HEIGHT-1] = 0

        if (piece.piece_type == pieces.King.PIECE_TYPE):
            if (piece.color == pieces.Piece.WHITE):
                self.white_king_moved = True
            else:
                self.black_king_moved = True

    # Returns if the given color is checked.
    def is_check(self, color):
        other_color = pieces.Piece.WHITE
        if (color == pieces.Piece.WHITE):
            other_color = pieces.Piece.BLACK

        for move in self.get_possible_moves(other_color):
            copy = Board.clone(self)
            copy.perform_move(move)

            king_found = False
            for x in range(Board.WIDTH):
                for y in range(Board.HEIGHT):
                    piece = copy.pieces[x][y]
                    if (piece != 0):
                        if (piece.color == color and piece.piece_type == pieces.King.PIECE_TYPE):
                            king_found = True

            if (not king_found):
                return True

        return False

    # Returns piece at given position or 0 if: No piece or out of bounds.
    def get_piece(self, x, y):
        if (not self.in_bounds(x, y)):
            return 0

        return self.pieces[x][y]

    def in_bounds(self, x, y):
        return (x >= 0 and y >= 0 and x < Board.WIDTH and y < Board.HEIGHT)

    def to_string(self):
        string =  "   0  1  2  3  4  5  6  7\n"
        string += "   -----------------------\n"
        for y in range(Board.HEIGHT-1, -1, -1):
            string += str(y) + "| "
            for x in range(Board.WIDTH):
                piece = self.pieces[x][y]
                if (piece != 0):
                    string += piece.to_string()
                else:
                    string += "-- "
            string += "\n"
        return string + "\n"
