import math
import pygame

from GameBoard import *

ASPECT_RATIO = 0.9


class ChessPiece:
    """
    Stores info regarding a chess piece
    PAWN = 0
    ROOK = 1
    HORSE = 2
    BISHOP = 3
    QUEEN = 4
    KING = 5
    BISHOP = 6
    HORSE = 7
    ROOK = 8
    """

    def __init__(self, row, col, rank, white_piece):
        """
        Constructor
        :param row: Integer - row number
        :param col: Integer - col number
        :param rank: Integer - Piece type
        :param white_piece: Boolean - white or black piece
        """
        self.row = row
        self.col = col
        self.rank = rank
        self.white_piece = white_piece
        self.movementVector = [0, 0]
        self.active = True
        self.firstMove = True
        self.invincible = False
        self.doubleMove = False
        self.special_duration = 0
        self.special_targets = []

        if self.white_piece:
            addon = "W"
        else:
            addon = "B"

        if rank == 0:
            self.img = pygame.image.load("assets/images/Pawn" + addon + ".png")
            self.hp = 2
            self.atk = 1
            self.name = "Pawn"
            self.desc = "Sacrificial Promotion:\nTemporarily promote to another piece until the end of next turn, then die"
            self.worth = 10
            self.maxHp = 2
        elif rank == 1 or rank == 8:
            self.img = pygame.image.load("assets/images/Rook" + addon + ".png")
            self.hp = 5
            self.atk = 2
            self.name = "Rook"
            self.desc = "Indomitability:\nGain invincibility at the end of the turn which lasts until for 4 total turns"
            self.worth = 50
            self.maxHp = 5
        elif rank == 2 or rank == 7:
            self.img = pygame.image.load("assets/images/Knight" + addon + ".png")
            self.hp = 3
            self.atk = 2
            self.name = "Knight"
            self.desc = "Double Charge:\nGain the ability to move twice; half damage if an attack is launched on the second move"
            self.worth = 20
            self.maxHp = 3
        elif rank == 3 or rank == 6:
            self.img = pygame.image.load("assets/images/Bishop" + addon + ".png")
            self.hp = 3
            self.atk = 2
            self.name = "Bishop"
            self.desc = "Healing Prayer:\nHeal any unit by hp equal to the Bishop's attack value"
            self.worth = 20
            self.maxHp = 3
        elif rank == 4:
            self.img = pygame.image.load("assets/images/Queen" + addon + ".png")
            self.hp = 6
            self.atk = 3
            self.name = "Queen"
            self.desc = "Charismatic Aura:\nBuffs all visible ally units within range of Queen's observation, by double hp and double attack, for 6 total turns"
            self.worth = 100
            self.maxHp = 6
        elif rank == 5:
            self.img = pygame.image.load("assets/images/King" + addon + ".png")
            self.hp = 9
            self.atk = 1
            self.name = "King"
            self.desc = "Tactical Exchange:\nPermits positional swap with any single ally unit"
            self.worth = 0
            self.maxHp = 9

    # Special abilities

    def special(self, arg=None):
        if self.rank == 0: # Pawn
            return self.sac_promotion(4)
        elif self.rank == 1 or self.rank == 8: # Rook
            return self.indomitability()
        elif self.rank == 2 or self.rank == 7: # Knight
            return self.charge(arg)
        elif self.rank == 3 or self.rank == 6: # Bishop
            return self.heal(arg)
        elif self.rank == 4: # Queen
            return self.aura(arg)
        elif self.rank == 5: # King
            return [True, None]

    def sac_promotion(self, new_rank):  # Pawn
        # currently fixed, new_rank will be a base piece in the rework for copying purposes
        self.rank = new_rank
        self.img = pygame.image.load("assets/images/Queen" + ("W" if self.white_piece is True else "B") + ".png")
        self.atk = 10
        self.hp = 10
        self.maxHp = 10
        return [True, None]

    def heal(self, target): # Bishop
        if target is None:
            return [False, None]
        else:
            target.hp += self.atk
            return [True, None]

    def indomitability(self): # Rook
        self.special_duration = 4
        self.invincible = True
        return [True, None]

    def charge(self, args): # Knight
        if args is None:
            self.doubleMove = True
            return [True, None]
        elif len(args) == 2:
            self.doubleMove = False
            col = args[1][0]
            row = args[1][1]
            result = self.move(col, row, args[0], args[0].boardState[col - 1][row - 1])
            return [False, result]
        elif len(args) == 3:
            col = args[2][0]
            row = args[2][1]
            result = self.move(col, row, args[0], args[0].boardState[col - 1][row - 1])
            return [True, result]

    def aura(self, args): # Queen
        """
        :param args: List
        [board, all_pieces]
        :return:
        [Result, Additional Info]
        """
        if args is None:
            return [False, None]
        board = args[0]
        allPieces = args[1]
        queen_obs = board.Update(allPieces, True)
        self.special_duration = 7
        for piece in allPieces:
            if piece.white_piece is not self.white_piece:
                continue
            if 1 > queen_obs[piece.col - 1][piece.row - 1] > 0 and piece.white_piece is False:
                piece.atk += 2
                piece.hp += 2
                piece.maxHp += 2
                self.special_targets.append(piece)
            elif queen_obs[piece.col - 1][piece.row - 1] > 0 and piece.white_piece is True:
                piece.atk += 2
                piece.hp += 2
                piece.maxHp += 2
                self.special_targets.append(piece)
        return [True, None]

    def render(self, surface):
        if self.active:
            temp_img = pygame.transform.scale(self.img.copy(), (100 * ASPECT_RATIO * 0.85, 100 * ASPECT_RATIO * 0.85))
            centreX = (self.col - 1) * 100 * ASPECT_RATIO + 100 * ASPECT_RATIO / 2
            centreY = (self.row - 1) * 100 * ASPECT_RATIO + 100 * ASPECT_RATIO / 2
            new_X = centreX - temp_img.get_width() / 2
            new_Y = centreY - temp_img.get_height() / 2
            surface.blit(temp_img, (new_X, new_Y))

    def castle(self, target, gameB):
        target = ChessPiece(target)
        # Fails if either piece already moved
        if not self.firstMove or not target.firstMove:
            return False
        # Fails if there are still pieces in between
        col_diff = self.col - target.col
        pathState = []
        pathObs = []
        for i in range(0, col_diff if col_diff != 0 else 1, 1 if col_diff >= 0 else -1):
            pathState.append(gameB.boardState[target.col - 1 + i][self.row - 1])
            pathObs.append(gameB.board_obs[target.col - 1 + i][self.row - 1])
        if pathState.count(None) != len(pathState):
            return False
        # Fails if any spots are currently being observed by the opponent
        if self.white_piece:
            for obs in pathObs:
                if int(obs) != obs:
                    return False
        else:
            for obs in pathObs:
                if obs > 1:
                    return False

        kingMove = self.col + (target.col - self.col / abs(target.col - self.col)) * 2
        rookMove = self.col + target.col - self.col / abs(target.col - self.col)

        gameB.boardState[self.col - 1][self.row - 1] = None
        gameB.boardState[target.col - 1][target.row - 1] = None
        self.col = kingMove
        target.col = rookMove
        gameB.boardState[self.col - 1][self.row - 1] = self
        gameB.boardState[target.col - 1][target.row - 1] = target
        self.firstMove = False
        target.firstMove = False

    def evalCounter(self, board, currentCol, currentRow, newCol, newRow):
        old_col_L = currentCol - 2
        old_col_R = currentCol
        new_col_L = newCol - 2
        new_col_R = newCol
        # White or Black? Counter-able Squares
        if self.white_piece:
            old_row = currentRow
            new_row = newRow
            if 0 <= old_col_L <= 7:
                board.counterValues[old_col_L][old_row][0] -= self.atk
            if 0 <= old_col_R <= 7:
                board.counterValues[old_col_R][old_row][0] -= self.atk
            if 0 <= new_col_L <= 7:
                board.counterValues[new_col_L][new_row][0] += self.atk
            if 0 <= new_col_R <= 7:
                board.counterValues[new_col_R][new_row][0] += self.atk
        else:
            old_row = currentRow - 2
            new_row = newRow - 2
            if 0 <= old_col_L <= 7:
                board.counterValues[old_col_L][old_row][1] -= self.atk
            if 0 <= old_col_R <= 7:
                board.counterValues[old_col_R][old_row][1] -= self.atk
            if 0 <= new_col_L <= 7:
                board.counterValues[new_col_L][new_row][1] += self.atk
            if 0 <= new_col_R <= 7:
                board.counterValues[new_col_R][new_row][1] += self.atk

    def adjustAtk(self, adjustment):
        self.atk += adjustment

    def move(self, posX, posY, gameB, taking_piece=None):
        """
        Moves the piece to the position pos
        :param posX: integer - column number
        :param posY: integer - row number
        :return: null
        """

        # Check for non-valid movement for each rank
        if self.rank == 0:
            row_diff = self.row - posY
            col_diff = self.col - posX
            pathState = []

            # Regardless of White or Black, move piece only in the same column
            if self.col != posX:
                # UNLESS IT'S TO TAKE A PIECE
                if (posY == self.row + 1 and self.white_piece and abs(col_diff) == 1 and taking_piece is not None) or \
                        (posY == self.row - 1 and not self.white_piece and abs(
                            col_diff) == 1 and taking_piece is not None):
                    if taking_piece.white_piece == self.white_piece or taking_piece.invincible is True:
                        return False
                    taking_piece.hp -= self.atk
                    # Counter-attack
                    self.hp -= gameB.counterValues[posX - 1][posY - 1][int(self.white_piece)]
                    if taking_piece.hp <= 0:
                        taking_piece.active = False

                else:
                    return False
            else:
                # White First move
                if self.firstMove and abs(posY - self.row) > 2:
                    return False

                # White Subsequent moves
                if posY != self.row + 1 and self.white_piece and self.row != 2:
                    return False
                # Black Subsequent moves
                if posY != self.row - 1 and not self.white_piece and self.row != 7:
                    return False

                for tempR in range(0, row_diff, int(row_diff / abs(row_diff))):
                    pathState.append(gameB.boardState[posX - 1][posY - 1 + tempR])

                # Check for Road Blocks
                if pathState.count(None) != len(pathState):
                    return False

        if self.rank == 1 or self.rank == 8:
            row_diff = self.row - posY
            col_diff = self.col - posX
            pathState = []
            # At least one of the row or column has to match the original
            if self.row != posY and self.col != posX:
                return False

            for j in range(0, col_diff if col_diff != 0 else 1, 1 if col_diff >= 0 else -1):
                for i in range(0, row_diff if row_diff != 0 else 1, 1 if row_diff >= 0 else -1):
                    pathState.append(gameB.boardState[posX - 1 + j][posY - 1 + i])

            pathState.pop(0)

            if pathState.count(None) != len(pathState):
                return False

            if taking_piece is not None:
                if taking_piece.white_piece == self.white_piece or taking_piece.invincible is True:
                    return False
                taking_piece.hp -= self.atk
                # Counter-attack
                self.hp -= gameB.counterValues[posX - 1][posY - 1][int(self.white_piece)]
                if taking_piece.hp <= 0:
                    taking_piece.active = False

        if self.rank == 2 or self.rank == 7:
            # Hypoteneuse ^ 2 is 5
            row_diff = self.row - posY
            col_diff = self.col - posX
            pathState = []
            if row_diff ** 2 + col_diff ** 2 != 5:
                return False

            pathState.append(gameB.boardState[posX - 1][posY - 1])

            if pathState.count(None) != len(pathState) and taking_piece is not None:
                if taking_piece.white_piece == self.white_piece or taking_piece.invincible is True:
                    return False
                taking_piece.hp -= self.atk
                # Counter-attack
                self.hp -= gameB.counterValues[posX - 1][posY - 1][int(self.white_piece)]
                if taking_piece.hp <= 0:
                    taking_piece.active = False

        if self.rank == 3 or self.rank == 6:
            # row_diff and col_diff has to be the same
            row_diff = self.row - posY
            col_diff = self.col - posX
            pathState = []

            if abs(row_diff) != abs(col_diff):
                return False

            row_pathing = int(row_diff / abs(row_diff))
            col_pathing = int(col_diff / abs(col_diff))

            for i in range(0, abs(col_diff), 1):
                pathState.append(gameB.boardState[posX - 1 + col_pathing * i][posY - 1 + row_pathing * i])

            pathState.pop(0)

            if pathState.count(None) != len(pathState):
                # 1 possibility - getting blocked
                return False

            if taking_piece is not None:
                if taking_piece.white_piece == self.white_piece or taking_piece.invincible is True:
                    return False
                taking_piece.hp -= self.atk
                # Counter-attack
                self.hp -= gameB.counterValues[posX - 1][posY - 1][int(self.white_piece)]
                if taking_piece.hp <= 0:
                    taking_piece.active = False

        if self.rank == 4:
            # row_diff and col_diff has to be the same or only one gets changed
            row_diff = self.row - posY
            col_diff = self.col - posX
            pathState = []
            if abs(row_diff) != abs(col_diff) and (row_diff != 0 and col_diff != 0):
                return False

            theta = math.atan2(-row_diff, col_diff)
            rad = int(math.sqrt(row_diff ** 2 + col_diff ** 2))

            for r in range(0, rad):
                row = round(math.sin(theta) * r)
                col = round(math.cos(theta) * r)
                pathState.append(gameB.boardState[posX - 1 + col][posY - 1 - row])

            pathState.pop(0)

            if pathState.count(None) != len(pathState):
                return False

            if taking_piece is not None:
                if taking_piece.white_piece == self.white_piece or taking_piece.invincible is True:
                    return False
                taking_piece.hp -= self.atk
                # Counter-attack
                self.hp -= gameB.counterValues[posX - 1][posY - 1][int(self.white_piece)]
                if taking_piece.hp <= 0:
                    taking_piece.active = False

        if self.rank == 5:
            # only 1 square move
            row_diff = self.row - posY
            col_diff = self.col - posX
            if row_diff ** 2 + col_diff ** 2 > 2:
                # Exception: When castling

                return False

            if taking_piece is not None:
                if taking_piece.white_piece == self.white_piece or taking_piece.invincible is True:
                    return False
                taking_piece.hp -= self.atk
                # Counter-attack
                self.hp -= gameB.counterValues[posX - 1][posY - 1][int(self.white_piece)]
                if taking_piece.hp <= 0:
                    taking_piece.active = False

        self.firstMove = False
        if taking_piece is None or taking_piece.active is False:
            if self.rank == 0:
                self.evalCounter(gameB, self.col, self.row, posX, posY)
            gameB.boardState[self.col - 1][self.row - 1] = None
            self.row = posY
            self.col = posX
            gameB.boardState[self.col - 1][self.row - 1] = self

        # Dies to counter-attack
        if self.hp <= 0:
            self.active = False

        for col in gameB.counterValues:
            text = ""
            for row in col:
                text += str(int(row[1]))
        return True
