import pygame
import time
from ChessPiece import *
from GameBoard import *
from MainMenu import *
from enum import IntEnum

ASPECT_RATIO = 0.9
INDEX_TO_GRID = ["A", "B", "C", "D", "E", "F", "G", "H"]


class STATE(IntEnum):
    MENU = 1
    OPTION = 2
    STRATEGY = 3
    GAME = 4
    QUIT = 5
    TARGET = 6


def init():
    """
    This is an initialization Function
    :return: Null
    Establish the parameters / Variables and load all necessary Packages
    """
    # Preload all Packages
    pygame.init()

    # Declaration of Global Variables
    global WHITE, GREY, BLACK, RED, BROWN, TAN, NEW_BROWN, CHARTREUSE, globalClock, currentState, turnCounter, board, \
        alteredHP, alteredAtk, whiteSpecialGauge, blackSpecialGauge, whiteTimer, blackTimer, selectedPiece, gameStarted, \
        allPieces, turnHistory, specialCost

    WHITE = (255, 255, 255)
    GREY = (220, 220, 220)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BROWN = (139, 80, 39)
    TAN = (210, 180, 140)
    NEW_BROWN = (107, 62, 30)
    CHARTREUSE = (110, 255, 0)

    globalClock = pygame.time.Clock()
    currentState = STATE.MENU
    turnCounter = 0
    board = GameBoard()

    whiteTimer = 600
    blackTimer = 600
    alteredHP = 0
    alteredAtk = 0
    whiteSpecialGauge = 0
    blackSpecialGauge = 0
    specialCost = [100, 150, 150, 160, 200, 250, 150, 160, 150]
    turnHistory = 0

    selectedPiece = None
    gameStarted = False
    allPieces = []

    # Load in-game music
    # pygame.mixer.music.load("assets/BG_Music.wav")
    # pygame.mixer.music.set_volume(0)
    # pygame.mixer.music.play(-1)
    print("------------------------------------------------------------------------------------")
    print("Input 'p' to pause the music")
    print("Input 'r' to resume the music")

    for i in range(1, 9, 1):
        # Load the white pawns
        tempPiece = ChessPiece(2, i, 0, True)
        allPieces.append(tempPiece)
        board.addPiece(tempPiece)

        # Load the white backline
        tempPiece = ChessPiece(1, i, i, True)
        allPieces.append(tempPiece)
        board.addPiece(tempPiece)

        # Load the black pawns
        tempPiece = ChessPiece(7, i, 0, False)
        allPieces.append(tempPiece)
        board.addPiece(tempPiece)

        # Load the black backline
        tempPiece = ChessPiece(8, i, i, False)
        allPieces.append(tempPiece)
        board.addPiece(tempPiece)

# Description display
def desc(text, pos):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font_stats.size(' ')[0]  # The width of a space.
    max_width, max_height = screen.get_size()
    x, y = pos
    for line in words:
        for word in line:
            text = font_desc.render(word, False, (0, 0, 0))
            word_width, word_height = text.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            screen.blit(text, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row

if __name__ == "__main__":
    init()
    size = (int(1124 * ASPECT_RATIO), int(800 * ASPECT_RATIO))
    screen = pygame.display.set_mode(size)
    pygame.display.set_icon(pygame.image.load("assets/images/KnightW.png").copy())
    pygame.display.set_caption("Chess+")
    HP = pygame.image.load("assets/images/HP.png")
    SWORD = pygame.image.load("assets/images/Sword.png")
    CONTINUE = pygame.image.load("assets/images/continue.png")
    CONTINUE = pygame.transform.scale(CONTINUE, (
    CONTINUE.get_width() * 2 * ASPECT_RATIO, CONTINUE.get_height() * 2 * ASPECT_RATIO))
    continueRect = CONTINUE.get_rect()
    center_align = (screen.get_width() + 823 * ASPECT_RATIO) / 2

while currentState != STATE.QUIT:
    if currentState == STATE.MENU:
        currentState = STATE(main_menu(screen))
        continue
    elif currentState == STATE.OPTION:
        currentState = STATE(options())
        continue

    # Check for mouseDown Event
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            currentState = STATE.QUIT
        if e.type == pygame.KEYDOWN:
            # Music Controls
            if e.key == pygame.K_p:
                pygame.mixer.music.pause()
                print('music paused')
            if e.key == pygame.K_r:
                pygame.mixer.music.unpause()
                print('music resumed')
            if e.key == pygame.K_SPACE and currentState == STATE.GAME:
                if selectedPiece is not None:
                    org_piece = allPieces[allPieces.index(selectedPiece)]
                    if org_piece.special()[0] == False:
                        # Exception
                        if org_piece.rank == 4:
                            org_piece.special([board, allPieces])
                            selectedPiece = None
                            turnCounter += 1
                            continue
                        # Failed [Likely to enter target mode]
                        currentState = STATE.TARGET
                    else:
                        # Success
                        selectedPiece = None
                        turnCounter += 1

        if pygame.event.event_name(e.type) == "MouseButtonDown":
            # Identify the row and column of our click
            # Get x and get y
            mouseX = e.pos[0]
            mouseY = e.pos[1]
            rowNum = int(mouseY / (100 * ASPECT_RATIO))
            colNum = int(mouseX / (100 * ASPECT_RATIO))
            # print("Row Clicked: " + str(rowNum + 1))
            # print("Column Clicked: " + str(colNum + 1))
            if rowNum not in range(0, 8, 1) or colNum not in range(0, 8, 1):
                piece = None
            else:
                piece = board.boardState[colNum][rowNum]
            """
            3 Cases:
                1. First selection (identified by -1 values in selectPos)
                2. Deselection (identified by the same position as selectPos)
                3. Final selection (identified by a non-negative selectPos and a negative dropPos)
            """
            if currentState == STATE.STRATEGY:
                if piece is not None:
                    if selectedPiece is not None and (selectedPiece.col - 1, selectedPiece.row - 1) == (colNum, rowNum): # Case 2
                        selectedPiece = None
                    else:
                        selectedPiece = piece
                else:
                    if continueRect.collidepoint(mouseX, mouseY):
                        currentState = STATE.GAME
                        selectedPiece = None
                    if selectedPiece is not None:
                        selectedPiece.atk = alteredAtk if alteredAtk != 0 else selectedPiece.atk
                        selectedPiece.hp = alteredHP if alteredHP != 0 else selectedPiece.hp

            elif currentState == STATE.TARGET:
                if piece is not None and piece.active:
                    org_piece = allPieces[allPieces.index(selectedPiece)]
                    if org_piece.rank in [3, 6]:
                        if not org_piece.special(piece)[0]:
                            # Failed [Likely to enter target mode]
                            currentState = STATE.TARGET
                        else:
                            # Success
                            currentState = STATE.GAME
                            selectedPiece = None
                            turnCounter += 1
                if org_piece.rank in [2, 7]:
                    if not org_piece.special([board, None, [colNum + 1, rowNum + 1]])[1]:
                        # Failed [Invalid move]
                        currentState = STATE.TARGET
                    else:
                        # Success
                        currentState = STATE.GAME
                        selectedPiece = None
                        turnCounter += 1

            elif currentState == STATE.GAME:
                if piece is not None and piece.active:
                    if selectedPiece is None:  # Case 1
                        if piece.white_piece is (turnCounter % 2 == 0):
                            if piece.row - 1 == rowNum and piece.col - 1 == colNum:
                                selectedPiece = piece
                    elif selectedPiece is not None and (selectedPiece.col - 1, selectedPiece.row - 1) == (colNum, rowNum): # Case 2
                        selectedPiece = None
                    else:
                        # If the move lands on another piece
                        if piece.row - 1 == rowNum and piece.col - 1 == colNum and selectedPiece.invincible is False:
                            if selectedPiece.doubleMove:
                                selectedPiece.special([board, [piece.col, piece.row]])
                                currentState = STATE.TARGET
                            # print("Moved Piece from " + str(INDEX_TO_GRID[selectedPiece.col - 1]) + str(selectedPiece.row) \
                            #       + " to " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
                            elif selectedPiece.move(colNum + 1, rowNum + 1, board, piece):
                                if selectedPiece.white_piece is True:
                                    blackSpecialGauge += piece.worth if piece.active is False else 0
                                else:
                                    whiteSpecialGauge += piece.worth if piece.active is False else 0
                                selectedPiece = None
                                turnCounter += 1
                                piece.special_duration -= 1

                elif piece is None and selectedPiece is not None and selectedPiece.invincible is False:  # Case 3
                    if selectedPiece.doubleMove:
                        if selectedPiece.special([board, [colNum + 1, rowNum + 1]])[1] is True:
                            currentState = STATE.TARGET
                    # If the move lands on an empty square
                    elif selectedPiece.move(colNum + 1, rowNum + 1, board):
                        turnCounter += 1
                        if not gameStarted:
                            globalClock.tick()
                            gameStarted = True
                        selectedPiece = None

    if turnHistory != turnCounter:
        for piece in allPieces:
            piece.special_duration -= 1
        turnHistory = turnCounter
    board.Update(allPieces)

    if selectedPiece is not None and selectedPiece.doubleMove is True:
        turnCounter += 2

    for i in range(len(allPieces)):
        # Check for King-Checks
        if allPieces[i].rank == 5 and allPieces[i].white_piece:
            if board.board_obs[allPieces[i].col - 1][allPieces[i].row - 1] % 1 != 0:
                print("White King is Under Check")
        elif allPieces[i].rank == 5 and not allPieces[i].white_piece:
            if board.board_obs[allPieces[i].col - 1][allPieces[i].row - 1] > 1:
                print("Black King is Under Check")

        # Check if the pawn reaches the promotion condition
        if allPieces[i].rank == 0 and allPieces[i].white_piece:
            if allPieces[i].row == 8:
                allPieces[i] = ChessPiece(allPieces[i].row, allPieces[i].col, 4, True)
        elif allPieces[i].rank == 0 and not allPieces[i].white_piece:
            if allPieces[i].row == 1:
                allPieces[i] = ChessPiece(allPieces[i].row, allPieces[i].col, 4, False)

    # # Draw Grid
    for i in range(8):  # Start i at 1, reach up to 8, increase i by 1 each loop
        for j in range(8):
            if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                pygame.draw.rect(screen, BROWN,
                                 pygame.Rect(j * 100 * ASPECT_RATIO, i * 100 * ASPECT_RATIO, 100 * ASPECT_RATIO, 100 * ASPECT_RATIO))
            else:
                pygame.draw.rect(screen, TAN, pygame.Rect(j * 100 * ASPECT_RATIO, i * 100 * ASPECT_RATIO, 100 * ASPECT_RATIO,
                                                          100 * ASPECT_RATIO))

    for piece in allPieces:
        piece.render(screen)

    if selectedPiece is not None:
        pygame.draw.rect(screen, CHARTREUSE, pygame.Rect((selectedPiece.col - 1) * 100 * ASPECT_RATIO, (selectedPiece.row - 1) * 100 * ASPECT_RATIO,
                                                         100 * ASPECT_RATIO, 100 * ASPECT_RATIO), 5)

    # Piece Info-chart
    pygame.draw.rect(screen, NEW_BROWN,
                     pygame.Rect(823 * ASPECT_RATIO, 0, math.ceil(302 * ASPECT_RATIO), 800 * ASPECT_RATIO))  # info chart bg
    pygame.draw.line(screen, WHITE, (799 * ASPECT_RATIO, 250 * ASPECT_RATIO), (screen.get_width(), 250 * ASPECT_RATIO), 2) # section divider
    pygame.draw.line(screen, WHITE, (799 * ASPECT_RATIO, 400 * ASPECT_RATIO), (screen.get_width(), 400 * ASPECT_RATIO), 2) # section divider
    pygame.draw.rect(screen, WHITE, pygame.Rect(823 * ASPECT_RATIO, 700 * ASPECT_RATIO, 151 * ASPECT_RATIO,
                                                102 * ASPECT_RATIO)) # white timer bg
    pygame.draw.rect(screen, BLACK, pygame.Rect(math.ceil(972 * ASPECT_RATIO), 700 * ASPECT_RATIO, 153 * ASPECT_RATIO,
                                                math.ceil(101 * ASPECT_RATIO)))  # black timer bg

    # Special gauge bar
    pygame.draw.rect(screen, GREY, pygame.Rect(799 * ASPECT_RATIO, 0, 24 * ASPECT_RATIO, 800 * ASPECT_RATIO))  # special gauge background
    pygame.draw.rect(screen, RED, pygame.Rect(799 * ASPECT_RATIO, (800 * ASPECT_RATIO) - blackSpecialGauge, 24 * ASPECT_RATIO,
                                                     800 * ASPECT_RATIO)) # black special gauge bar
    pygame.draw.rect(screen, CHARTREUSE, pygame.Rect(799 * ASPECT_RATIO, 0, 24 * ASPECT_RATIO, 0 + whiteSpecialGauge)) # white special gauge bar
    pygame.draw.rect(screen, BLACK, pygame.Rect(799 * ASPECT_RATIO, 0, 3 * ASPECT_RATIO, 800 * ASPECT_RATIO), 2)  # side divider
    pygame.draw.rect(screen, BLACK, pygame.Rect(820 * ASPECT_RATIO, 0, 3 * ASPECT_RATIO, 800 * ASPECT_RATIO), 2)  # side divider
    pygame.draw.line(screen, BLACK, (799 * ASPECT_RATIO, 400 * ASPECT_RATIO), (820 * ASPECT_RATIO, 400 * ASPECT_RATIO), 2) # black/white special divider

    # White special activation line indicator
    pygame.draw.line(screen, BLACK, (799 * ASPECT_RATIO, 80 * ASPECT_RATIO), (820 * ASPECT_RATIO, 80 * ASPECT_RATIO)) # pawn
    pygame.draw.line(screen, BLACK, (799 * ASPECT_RATIO, 120 * ASPECT_RATIO), (820 * ASPECT_RATIO, 120 * ASPECT_RATIO)) # bishop/rook
    pygame.draw.line(screen, BLACK, (799 * ASPECT_RATIO, 160 * ASPECT_RATIO), (820 * ASPECT_RATIO, 160 * ASPECT_RATIO)) # knight/king
    pygame.draw.line(screen, BLACK, (799 * ASPECT_RATIO, 200 * ASPECT_RATIO), (820 * ASPECT_RATIO, 200 * ASPECT_RATIO)) # queen

    # Black special activation line indicator
    pygame.draw.line(screen, BLACK, (799 * ASPECT_RATIO, 720 * ASPECT_RATIO), (820 * ASPECT_RATIO, 720 * ASPECT_RATIO)) # pawn
    pygame.draw.line(screen, BLACK, (799 * ASPECT_RATIO, 680 * ASPECT_RATIO), (820 * ASPECT_RATIO, 680 * ASPECT_RATIO)) # bishop/rook
    pygame.draw.line(screen, BLACK, (799 * ASPECT_RATIO, 640 * ASPECT_RATIO), (820 * ASPECT_RATIO, 640 * ASPECT_RATIO)) # knight/king
    pygame.draw.line(screen, BLACK, (799 * ASPECT_RATIO, 600 * ASPECT_RATIO), (820 * ASPECT_RATIO, 600 * ASPECT_RATIO)) # queen

    # White special piece indicator
    rescaled_pawnW_img = pygame.transform.scale(pygame.image.load("assets/images/PawnW.png"), (20 * ASPECT_RATIO, 20 * ASPECT_RATIO))
    rescaled_knightW_img = pygame.transform.scale(pygame.image.load("assets/images/KnightW.png"), (20 * ASPECT_RATIO, 20 * ASPECT_RATIO))
    rescaled_bishopW_img = pygame.transform.scale(pygame.image.load("assets/images/BishopW.png"), (17 * ASPECT_RATIO, 20 * ASPECT_RATIO))
    rescaled_rookW_img = pygame.transform.scale(pygame.image.load("assets/images/RookW.png"), (20 * ASPECT_RATIO, 20 * ASPECT_RATIO))
    rescaled_queenW_img = pygame.transform.scale(pygame.image.load("assets/images/QueenW.png"), (17 * ASPECT_RATIO, 20 * ASPECT_RATIO))
    rescaled_kingW_img = pygame.transform.scale(pygame.image.load("assets/images/KingW.png"), (14 * ASPECT_RATIO, 20 * ASPECT_RATIO))

    screen.blit(rescaled_pawnW_img, (810 * ASPECT_RATIO - rescaled_pawnW_img.get_width() / 2, 56 * ASPECT_RATIO))
    screen.blit(rescaled_knightW_img, (810 * ASPECT_RATIO - rescaled_knightW_img.get_width() / 2, 98 * ASPECT_RATIO))
    screen.blit(rescaled_bishopW_img, (810 * ASPECT_RATIO - rescaled_bishopW_img.get_width() / 2 + 1.11 * ASPECT_RATIO, 162 * ASPECT_RATIO))
    screen.blit(rescaled_rookW_img, (810 * ASPECT_RATIO - rescaled_rookW_img.get_width() / 2, 139 * ASPECT_RATIO))
    screen.blit(rescaled_queenW_img, (810 * ASPECT_RATIO - rescaled_queenW_img.get_width() / 2 + 1.11 * ASPECT_RATIO, 205 * ASPECT_RATIO))
    screen.blit(rescaled_kingW_img, (810 * ASPECT_RATIO - rescaled_kingW_img.get_width() / 2, 120 * ASPECT_RATIO))

    # Black special piece indicator
    rescaled_pawnB_img = pygame.transform.scale(pygame.image.load("assets/images/PawnB.png"), (20 * ASPECT_RATIO, 20 * ASPECT_RATIO))
    rescaled_knightB_img = pygame.transform.scale(pygame.image.load("assets/images/KnightB.png"), (20 * ASPECT_RATIO, 20 * ASPECT_RATIO))
    rescaled_bishopB_img = pygame.transform.scale(pygame.image.load("assets/images/BishopB.png"), (17 * ASPECT_RATIO, 20 * ASPECT_RATIO))
    rescaled_rookB_img = pygame.transform.scale(pygame.image.load("assets/images/RookB.png"), (20 * ASPECT_RATIO, 20 * ASPECT_RATIO))
    rescaled_queenB_img = pygame.transform.scale(pygame.image.load("assets/images/QueenB.png"), (17 * ASPECT_RATIO, 20 * ASPECT_RATIO))
    rescaled_kingB_img = pygame.transform.scale(pygame.image.load("assets/images/KingB.png"), (14 * ASPECT_RATIO, 20 * ASPECT_RATIO))

    screen.blit(rescaled_pawnB_img, (810 * ASPECT_RATIO - rescaled_pawnB_img.get_width() / 2, 725 * ASPECT_RATIO))
    screen.blit(rescaled_knightB_img, (810 * ASPECT_RATIO - rescaled_knightB_img.get_width() / 2, 682 * ASPECT_RATIO))
    screen.blit(rescaled_bishopB_img, (810 * ASPECT_RATIO - rescaled_bishopB_img.get_width() / 2 + 1.11 * ASPECT_RATIO, 620 * ASPECT_RATIO))
    screen.blit(rescaled_rookB_img, (810 * ASPECT_RATIO - rescaled_rookB_img.get_width() / 2, 643 * ASPECT_RATIO))
    screen.blit(rescaled_queenB_img, (810 * ASPECT_RATIO - rescaled_queenB_img.get_width() / 2 + 1.11 * ASPECT_RATIO, 576 * ASPECT_RATIO))
    screen.blit(rescaled_kingB_img, (810 * ASPECT_RATIO - rescaled_kingB_img.get_width() / 2, 661 * ASPECT_RATIO))

    mouse_pos = pygame.mouse.get_pos()
    mouse_col = math.floor(mouse_pos[0] / (100 * ASPECT_RATIO))
    mouse_row = math.floor(mouse_pos[1] / (100 * ASPECT_RATIO))
    try:
        located_piece = board.boardState[mouse_col][mouse_row]
    except:
        located_piece = None

    if selectedPiece is not None:
        located_piece = selectedPiece

    if currentState == STATE.STRATEGY:
        if located_piece is not None and located_piece.active:
            # Image rescaling
            rescaled_piece_img = pygame.transform.scale(located_piece.img, (145 * ASPECT_RATIO, 145 * ASPECT_RATIO))
            rescaled_HP_img = pygame.transform.scale(HP, (45 * ASPECT_RATIO, 45 * ASPECT_RATIO))
            rescaled_SWORD_img = pygame.transform.scale(SWORD, (45 * ASPECT_RATIO, 45 * ASPECT_RATIO))

            # Text type
            pygame.font.init()
            font_stats = pygame.font.SysFont('Calibri', int(50 * ASPECT_RATIO))
            font_desc = pygame.font.SysFont('Calibri', int(26 * ASPECT_RATIO))
            piece_name = font_stats.render(located_piece.name, False, (0, 0, 0))

            # Image display
            center_align = (screen.get_width() + 823 * ASPECT_RATIO) / 2
            screen.blit(rescaled_piece_img,
                        (center_align - rescaled_piece_img.get_width() / 2, 90 * ASPECT_RATIO))  # Piece type
            screen.blit(piece_name, ((screen.get_width() / 2 - piece_name.get_width() / 2) + (412 * ASPECT_RATIO),
                                     (screen.get_height() / 2 - piece_name.get_width() / 2) - (317 * ASPECT_RATIO))) # Piece name
            screen.blit(rescaled_HP_img, (center_align - 130 * ASPECT_RATIO, 340 * ASPECT_RATIO))
            barColor = (220, 20, 60)

            # HP stat bar
            alteredHP = 0
            for i in range(located_piece.hp):
                barRect = pygame.rect.Rect(center_align - (68 - i * 20) * ASPECT_RATIO, 350 * ASPECT_RATIO, 19 * ASPECT_RATIO,
                                           30 * ASPECT_RATIO)

                if i == 0:
                    pygame.draw.rect(screen, barColor, barRect, border_top_left_radius=5, border_bottom_left_radius=5)
                elif i == 9:
                    pygame.draw.rect(screen, barColor, barRect, border_top_right_radius=5, border_bottom_right_radius=5)
                else:
                    pygame.draw.rect(screen, barColor, barRect)

                if barRect.collidepoint(pygame.mouse.get_pos()):
                    barColor = (255, 127, 127)
                    alteredHP = i + 1

            barColor = (255, 255, 255)
            for i in range(9, located_piece.hp - 1, -1):
                barRect = pygame.rect.Rect(center_align - (68 - i * 20) * ASPECT_RATIO, 350 * ASPECT_RATIO, 19 * ASPECT_RATIO,
                                           30 * ASPECT_RATIO)

                if barRect.collidepoint(pygame.mouse.get_pos()):
                    barColor = (255, 127, 127)
                    alteredHP = i + 1

                if i == 0:
                    pygame.draw.rect(screen, barColor, barRect, border_top_left_radius=5, border_bottom_left_radius=5)
                elif i == 9:
                    pygame.draw.rect(screen, barColor, barRect, border_top_right_radius=5, border_bottom_right_radius=5)
                else:
                    pygame.draw.rect(screen, barColor, barRect)

            screen.blit(rescaled_SWORD_img, (center_align - 130 * ASPECT_RATIO, 270 * ASPECT_RATIO))

            # Atk stat bar
            alteredAtk = 0
            barColor = (255, 191, 0)
            for i in range(located_piece.atk):
                barRect = pygame.rect.Rect(center_align - (68 - i * 20) * ASPECT_RATIO, 280 * ASPECT_RATIO, 19 * ASPECT_RATIO,
                                           30 * ASPECT_RATIO)
                if barRect.collidepoint(pygame.mouse.get_pos()):
                    barColor = (251, 191, 119)
                    alteredAtk = i + 1

                if i == 0:
                    pygame.draw.rect(screen, barColor, barRect, border_top_left_radius=5, border_bottom_left_radius=5)
                elif i == 9:
                    pygame.draw.rect(screen, barColor, barRect, border_top_right_radius=5, border_bottom_right_radius=5)
                else:
                    pygame.draw.rect(screen, barColor, barRect)
            barColor = (255, 255, 255)
            for i in range(9, located_piece.atk - 1, -1):
                barRect = pygame.rect.Rect(center_align - (68 - i * 20) * ASPECT_RATIO, 280 * ASPECT_RATIO, 19 * ASPECT_RATIO,
                                           30 * ASPECT_RATIO)
                if barRect.collidepoint(pygame.mouse.get_pos()):
                    barColor = (251, 220, 180)
                    alteredAtk = i + 1

                if i == 0:
                    pygame.draw.rect(screen, barColor, barRect, border_top_left_radius=5, border_bottom_left_radius=5)
                elif i == 9:
                    pygame.draw.rect(screen, barColor, barRect, border_top_right_radius=5, border_bottom_right_radius=5)
                else:
                    pygame.draw.rect(screen, barColor, barRect)

            desc(located_piece.desc, (826 * ASPECT_RATIO + (7 * ASPECT_RATIO), 800 * ASPECT_RATIO - (260 * ASPECT_RATIO)))

        continueRect.centerx = center_align
        continueRect.centery = 480 * ASPECT_RATIO
        screen.blit(CONTINUE, continueRect)

    elif currentState == STATE.GAME:
        if located_piece is not None:
            # Image rescaling
            rescaled_piece_img = pygame.transform.scale(located_piece.img, (145 * ASPECT_RATIO, 145 * ASPECT_RATIO))
            rescaled_HP_img = pygame.transform.scale(HP, (92 * ASPECT_RATIO, 92 * ASPECT_RATIO))
            rescaled_SWORD_img = pygame.transform.scale(SWORD, (92 * ASPECT_RATIO, 92 * ASPECT_RATIO))

            # Text type
            pygame.font.init()
            font_stats = pygame.font.SysFont('Calibri', int(50 * ASPECT_RATIO))
            font_desc = pygame.font.SysFont('Calibri', int(26 * ASPECT_RATIO))
            piece_name = font_stats.render(located_piece.name, False, (0, 0, 0))
            piece_hp = font_stats.render(str(int(located_piece.hp)), False, (0, 0, 0))
            piece_atk = font_stats.render(str(int(located_piece.atk)), False, (0, 0, 0))

            # Image display
            center_align = (screen.get_width() + 800 * ASPECT_RATIO) / 2 + (12 * ASPECT_RATIO)
            screen.blit(rescaled_piece_img, (center_align - rescaled_piece_img.get_width() / 2, 90 * ASPECT_RATIO)) # Piece type
            screen.blit(piece_name, ((screen.get_width() / 2 - piece_name.get_width() / 2) + (412 * ASPECT_RATIO),
                                     (screen.get_height() / 2 - piece_name.get_width() / 2) - (317 * ASPECT_RATIO))) # Piece name
            screen.blit(piece_hp, ( center_align - piece_hp.get_width() / 2 - 25 * ASPECT_RATIO, 300 * ASPECT_RATIO)) # Piece hp stat
            screen.blit(rescaled_HP_img, (center_align - 150 * ASPECT_RATIO, 280 * ASPECT_RATIO))
            screen.blit(piece_atk, (center_align - piece_hp.get_width() / 2 + 115 * ASPECT_RATIO, 300 * ASPECT_RATIO)) # Piece atk stat
            screen.blit(rescaled_SWORD_img, (center_align - 1 * ASPECT_RATIO, 280 * ASPECT_RATIO))
            desc(located_piece.desc, (826 * ASPECT_RATIO + (7 * ASPECT_RATIO), 800 * ASPECT_RATIO - (260 * ASPECT_RATIO)))

    # Timer
    font_win = pygame.font.SysFont('Calibri', int(100 * ASPECT_RATIO))
    white_win = font_win.render("WHITE WON", False, (255, 255, 255))
    black_win = font_win.render("BLACK WON", False, (0, 0, 0))
    font_time = pygame.font.SysFont("sans", int(48 * ASPECT_RATIO))

    new_whiteTimer = font_time.render(str(time.strftime("%M:%S", time.gmtime(whiteTimer))), False, (0, 0, 0))
    screen.blit(new_whiteTimer, (screen.get_width() / 2 - new_whiteTimer.get_width() / 2 + (333 * ASPECT_RATIO), 724 * ASPECT_RATIO))
    new_blackTimer = font_time.render(str(time.strftime("%M:%S", time.gmtime(blackTimer))), False, (255, 255, 255))
    screen.blit(new_blackTimer, (screen.get_width() / 2 - new_blackTimer.get_width() / 2 + (487 * ASPECT_RATIO), 724 * ASPECT_RATIO))

    if gameStarted:
        globalClock.tick()
        if turnCounter % 2 == 0:
            whiteTimer -= float(globalClock.get_time()) / 1000.0
        if turnCounter % 2 == 1:
            blackTimer -= float(globalClock.get_time()) / 1000.0
        if whiteTimer < 0:  # Black wins due to time
            screen.blit(black_win, (400 * ASPECT_RATIO - black_win.get_width() / 2, screen.get_height() / 2 -
                                    black_win.get_height() / 2))
            pygame.display.flip()
            pygame.time.wait(5000)
            currentState = STATE.QUIT

        if blackTimer < 0:  # White wins due to time
            screen.blit(white_win, ((400 * ASPECT_RATIO - white_win.get_width() / 2, screen.get_height() / 2 -
                                     white_win.get_height() / 2)))
            pygame.display.flip()
            pygame.time.wait(5000)
            currentState = STATE.QUIT

    pygame.display.flip()