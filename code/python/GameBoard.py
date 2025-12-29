import math
from ChessPiece import *

class GameBoard:

    def __init__(self):
        self.boardState = [[None for i in range(8)] for i in range(8)]  # Format [colNum, rowNum]
        self.board_obs = [[0.0 for i in range(8)] for i in range(8)] # 0 = Unobserved | Decimal = Black | Whole = White
        self.counterValues = [[[0.0, 0.0] for i in range(8)] for i in range(8)] # [colNum, rowNum, alliance[W, B]]
        self.whiteCastle = True
        self.blackCastle = True

    def addPiece(self, chessPiece):
        self.boardState[chessPiece.col - 1][chessPiece.row - 1] = chessPiece
        # First time logging counter values
        if chessPiece.rank == 0:  # Pawn
            obs_col_L = chessPiece.col - 2
            obs_col_R = chessPiece.col
            # White or Black? Counter-able Squares
            if chessPiece.white_piece:
                obs_row = chessPiece.row
                if 0 <= obs_col_L <= 7:
                    self.counterValues[obs_col_L][obs_row][0] += chessPiece.atk
                if 0 <= obs_col_R <= 7:
                    self.counterValues[obs_col_R][obs_row][0] += chessPiece.atk
            else:
                obs_row = chessPiece.row - 2
                if 0 <= obs_col_L <= 7:
                    self.counterValues[obs_col_L][obs_row][1] += chessPiece.atk
                if 0 <= obs_col_R <= 7:
                    self.counterValues[obs_col_R][obs_row][1] += chessPiece.atk

    def Update(self, pieces, queen=False):
        self.board_obs = [[0.0 for i in range(8)] for i in range(8)]  # 0 = Unobserved | Decimal = Black | Whole = White
        spec_obs = [[0.0 for i in range(8)] for i in range(8)]
        for piece in pieces:
            # Evaluate Special Duration
            if piece.rank == 4 and piece.special_duration <= 0: # Queen
                for spec_piece in piece.special_targets:
                    spec_piece.hp -= 2
                    spec_piece.maxHp -= 2
                    spec_piece.atk -= 2
                    if spec_piece.hp <= 0:
                        spec_piece.hp = 1
                piece.special_targets = []
            if (piece.rank == 1 or piece.rank == 8) and piece.special_duration <= 0: # Rook
                piece.invincible = False

            if piece.active:
                # Check observations
                if piece.rank == 0: # Pawn
                    obs_col_L = piece.col - 2
                    obs_col_R = piece.col
                    # White or Black? Observed Squares
                    if piece.white_piece:
                        obs_row = piece.row
                        if 0 <= obs_col_L <= 7:
                            self.board_obs[obs_col_L][obs_row] += 1.0
                        if 0 <= obs_col_R <= 7:
                            self.board_obs[obs_col_R][obs_row] += 1.0
                    else:
                        obs_row = piece.row - 2
                        if 0 <= obs_col_L <= 7:
                            self.board_obs[obs_col_L][obs_row] += 0.01
                        if 0 <= obs_col_R <= 7:
                            self.board_obs[obs_col_R][obs_row] += 0.01

                if piece.rank == 1 or piece.rank == 8: # Rook
                    possibleAngles = [0, 2, 4, 6]
                    offLimitAngles = []
                    for r in range(1, 8, 1):
                        for angle in possibleAngles:
                            if offLimitAngles.count(angle) > 0:
                                continue
                            theta = angle * (math.pi / 4)
                            y_diff = -math.sin(theta) * r
                            x_diff = math.cos(theta) * r
                            obs_col = piece.col - 1 + round(x_diff)
                            obs_row = piece.row - 1 + round(y_diff)
                            if obs_col < 0 or obs_row < 0 or obs_col > 7 or obs_row > 7:
                                offLimitAngles.append(angle)
                                continue

                            if piece.white_piece is True:
                                self.board_obs[obs_col][obs_row] += 1.0
                            else:
                                self.board_obs[obs_col][obs_row] += 0.01

                            if self.boardState[obs_col][obs_row] is not None:
                                offLimitAngles.append(angle)

                if piece.rank == 2 or piece.rank == 7: # Horse
                    possibleAngles = [i for i in range(8)]
                    for angle in possibleAngles:
                        theta = ((int(angle / 2) * 90 - 30) + (angle % 2) * 60) * math.pi / 180
                        y_diff = -math.sin(theta) * math.sqrt(5)
                        x_diff = math.cos(theta) * math.sqrt(5)
                        obs_col = piece.col - 1 + round(x_diff)
                        obs_row = piece.row - 1 + round(y_diff)

                        if obs_col < 0 or obs_row < 0 or obs_col > 7 or obs_row > 7:
                            continue

                        if piece.white_piece is True:
                            self.board_obs[obs_col][obs_row] += 1.0
                        else:
                            self.board_obs[obs_col][obs_row] += 0.01


                if piece.rank == 3 or piece.rank == 6: # Bishop
                    possibleAngles = [1, 3, 5, 7]
                    offLimitAngles = []
                    for r in range(1, 8, 1):
                        for angle in possibleAngles:
                            if offLimitAngles.count(angle) > 0:
                                continue
                            theta = angle * (math.pi / 4)
                            y_diff = -math.sin(theta) * r
                            x_diff = math.cos(theta) * r
                            obs_col = piece.col - 1 + round(x_diff)
                            obs_row = piece.row - 1 + round(y_diff)
                            if obs_col < 0 or obs_row < 0 or obs_col > 7 or obs_row > 7:
                                offLimitAngles.append(angle)
                                continue

                            if piece.white_piece is True:
                                self.board_obs[obs_col][obs_row] += 1.0
                            else:
                                self.board_obs[obs_col][obs_row] += 0.01

                            if self.boardState[obs_col][obs_row] is not None:
                                offLimitAngles.append(angle)

                if piece.rank == 4: # Queen
                    # Queen can observe 8 possible angles, 0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°
                    # 0, pi/4, pi/2, 3pi/4, pi, 5pi/4, 3pi/2, 7pi/4
                    possibleAngles = [i for i in range(8)]
                    offLimitAngles = []
                    temp_obs = [[0.0 for i in range(8)] for i in range(8)]
                    for r in range(1, 8, 1):
                        for angle in possibleAngles:
                            if offLimitAngles.count(angle) > 0:
                                continue
                            theta = angle * (math.pi / 4)
                            y_diff = -math.sin(theta) * r
                            x_diff = math.cos(theta) * r
                            obs_col = piece.col - 1 + round(x_diff)
                            obs_row = piece.row - 1 + round(y_diff)
                            if obs_col < 0 or obs_row < 0 or obs_col > 7 or obs_row > 7:
                                offLimitAngles.append(angle)
                                continue

                            if piece.white_piece is True:
                                self.board_obs[obs_col][obs_row] += 1.0
                                temp_obs[obs_col][obs_row] += 1.0
                            else:
                                self.board_obs[obs_col][obs_row] += 0.01
                                temp_obs[obs_col][obs_row] += 0.01

                            if self.boardState[obs_col][obs_row] is not None:
                                offLimitAngles.append(angle)

                    for col in range(len(self.board_obs)):
                        for row in range(len(self.board_obs[0])):
                            spec_obs[col][row] += temp_obs[col][row]

                if piece.rank == 5: # King
                    possibleAngles = [i for i in range(8)]
                    for angle in possibleAngles:
                        theta = angle * 45 * math.pi / 180
                        y_diff = -math.sin(theta) * math.sqrt(2)
                        x_diff = math.cos(theta) * math.sqrt(2)
                        obs_col = piece.col - 1 + round(x_diff)
                        obs_row = piece.row - 1 + round(y_diff)

                        if obs_col < 0 or obs_row < 0 or obs_col > 7 or obs_row > 7:
                            continue

                        if piece.white_piece is True:
                            self.board_obs[obs_col][obs_row] += 1.0
                        else:
                            self.board_obs[obs_col][obs_row] += 0.01

        if queen is True:
            return spec_obs