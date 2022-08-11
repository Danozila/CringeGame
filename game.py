def FieldCode(field):
    code = 0
    for row in field:
        for i in row:
            code = code * 100 + i
    return code
def FieldCopy(field):
    copy = []
    for row in field:
       copy.append(row.copy())
    return copy
def MakeTree(field, tree):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    win = 0
    count = 0
    bestWin = -1
    bestPos = None
    code = FieldCode(field)
    if code in tree:
        return tree[code][1]
    else:
        for i in range(len(field)):
            for j in range(len(field)):
                for value in range(2, field[i][j]):
                    if field[i][j] % value == 0 or CheckMove(field, i, j, value):
                        count += 1
                        new = FieldCopy(field)
                        new[i][j] = value
                        winTemp = MakeTree(new, tree)
                        win = (win * (count - 1) + winTemp) / count
                        if winTemp > bestWin:
                            bestPos = (j, i)
                            bestWin = winTemp
                            bestField = FieldCopy(new)
        if bestWin == -1:
            tree[code] = (None, 1, None)
        else:
            tree[code] = (bestField, 1 - win, bestPos)
        return 1 - win
def CheckMove(field, row, col, value):
    for i in range(len(field)):
        if i != col and IsMutuallyPrime(field[row][i], value) == False:
            return False
    for i in range(len(field)):
        if i != row and IsMutuallyPrime(field[i][col], value) == False:
            return False
    return True
def IsMutuallyPrime(a, b):
    if a == 0:
        if b == 1:
            return True
        else:
            return False
    else:
        return IsMutuallyPrime(b % a, a)
def GenerateField(size, minValue, maxValue):
    field = []
    for i in range(size):
        field.append([101] * size)
    for i in range(size):
        for j in range(size):
            value = randint(minValue, maxValue)
            while CheckMove(field, i, j, value) == False:
                value = randint(minValue, maxValue)
            field[i][j] = value
    return field
def GameEnd(field):
    for i in range(len(field)):
        for j in range(len(field)):
            for value in range(2, field[i][j]):
                if CheckMove(field, i, j, value):
                    return False
    return True
def MakeCells(field, cellSize):
    cells = []
    for i in range(len(field)):
        cells.append([])
        for j in range(len(field)):
            if (i + j) % 2 == 0:
                cellColour = (245,245,220)
            else:
                cellColour = (172,147,98)
            cell = pygame.Surface((cellSize, cellSize))
            cell.fill(cellColour)
            cells[i].append(cell)
    return cells
def DisplayField(field, cells, cellSize, x0, y0, numFont):
    for i in range(len(field)):
        for j in range(len(field)):
            screen.blit(cells[i][j], (x0 + j * cellSize, y0 + i * cellSize))
            num = numFont.render(str(field[i][j]), True, (0, 0, 0))
            screen.blit(num, (x0 + j * cellSize, y0 + i * cellSize))
import pygame
from random import randint
from time import time
from sys import exit
width = 550
height = 680
while True:
    field = GenerateField(3, 2, 11)
    if GameEnd(field) == False:
        break
cellSize = min(width, height) // len(field)
x0 = (width - len(field) * cellSize) / 2
y0 = (height - len(field) * cellSize) / 2
running = True
pos = None
old = None
num = ''
player = 1
computer = 0
gameEnd = False
scene = "Game mode choice"
timer = -1

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
textFont = pygame.font.Font(None, 32)
playerChoiceText = textFont.render('Выберите игрока(1-первый, 2-второй)', True, (0, 0, 0))
gmChoiceText1 = textFont.render('Выберите режим игры', True, (0, 0, 0))
gmChoiceText2 = textFont.render('(1-два игрока, 2 - игрок против компьютера)', True, (0, 0, 0))
loadingText = textFont.render('Загрузка...', True, (0, 0, 0))
numFont = pygame.font.Font(None, cellSize)
winText2 = textFont.render('Нажмите любую клавишу, чтобы начать заново', True, (0, 0, 0))
cells = MakeCells(field, cellSize)
while running:
    if scene == "Game mode choice":
        screen.fill((255, 255, 255))
        screen.blit(gmChoiceText1, (0, 0))
        screen.blit(gmChoiceText2, (0, 30))
        DisplayField(field, cells, cellSize, x0, y0, numFont)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == '1' or pygame.key.name(event.key) == '[1]':
                    scene = "Game"
                    gameMode = "PvP"
                elif pygame.key.name(event.key) == '2' or pygame.key.name(event.key) == '[2]':
                    scene = "Loading"
                    gameMode = "PvE"
    elif scene == "Loading":
        screen.fill((255, 255, 255))
        screen.blit(loadingText, (0, 0))
        DisplayField(field, cells, cellSize, x0, y0, numFont)
        pygame.display.flip()
        tree = {}
        MakeTree(field, tree)
        scene = "Player choice"
    elif scene == "Player choice":
        screen.fill((255, 255, 255))
        screen.blit(playerChoiceText, (0, 0))
        DisplayField(field, cells, cellSize, x0, y0, numFont)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == '1' or pygame.key.name(event.key) == '[1]':
                    computer = 2
                    scene = 'Game'
                elif pygame.key.name(event.key) == '2' or pygame.key.name(event.key) == '[2]':
                    computer = 1
                    timer = time()
                    scene = 'Game'
    elif scene == "Game":
        screen.fill((255, 255, 255))
        cells = MakeCells(field, cellSize)
        if pos != None:
            if gameMode == "PvE" and player == computer:
                cells[pos[1]][pos[0]].fill((255, 70, 66))
            else:
                cells[pos[1]][pos[0]].fill((255, 255, 0))
        DisplayField(field, cells, cellSize, x0, y0, numFont)
        if gameMode == "PvE" and player == computer:
            playerText = textFont.render("Игрок: " + str(player) + "(Компьютер)", True, (0, 0, 0))
        else:
            playerText = textFont.render("Игрок: " + str(player), True, (0, 0, 0))
        screen.blit(playerText, (0, 0))
        pygame.display.flip()
        if gameMode == "PvE" and player == computer and not gameEnd:
            if pos == None:
                pos = tree[FieldCode(field)][2]
            if time() - timer > 1:
                field = tree[FieldCode(field)][0]
                player = player % 2 + 1
                gameEnd = GameEnd(field)
                pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif gameMode == "PvP" or player != computer:
                if event.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pos()[0] > x0 and pygame.mouse.get_pos()[0] < width - x0 and pygame.mouse.get_pos()[1] > y0 and pygame.mouse.get_pos()[1] < height - y0:
                    if num != '':
                        field[pos[1]][pos[0]] = old
                        num = ''
                    pos = (int((pygame.mouse.get_pos()[0] - x0) / cellSize), int((pygame.mouse.get_pos()[1] - y0) / cellSize))
                elif event.type == pygame.KEYDOWN and pos != None:
                    if pygame.key.name(event.key) == 'return' or pygame.key.name(event.key) == 'enter':
                        num = ''
                        if old != None:
                            if field[pos[1]][pos[0]] > 1 and CheckMove(field, pos[1], pos[0], field[pos[1]][pos[0]]) and field[pos[1]][pos[0]] < old:
                                player = player % 2 + 1
                                timer = time()
                                gameEnd = GameEnd(field)
                                pos = None
                            else:
                                field[pos[1]][pos[0]] = old
                    elif pygame.key.name(event.key).isdigit():
                        if num == '':
                            old = field[pos[1]][pos[0]]
                        num += pygame.key.name(event.key)
                        field[pos[1]][pos[0]] = int(num)
                    elif len(pygame.key.name(event.key)) == 3 and pygame.key.name(event.key)[1].isdigit():
                        if num == '':
                            old = field[pos[1]][pos[0]]
                        num += pygame.key.name(event.key)[1]
                        field[pos[1]][pos[0]] = int(num)
        if gameEnd:
            scene = "Win"
            if player != computer and gameMode == "PvE":
                winText1 = textFont.render("Игрок " + str(player % 2 + 1) + "(Компьютер)" + " выиграл", True, (0, 0, 0))
            else:
                winText1 = textFont.render("Игрок " + str(player % 2 + 1) + " выиграл", True, (0, 0, 0))
    elif scene == "Win":
        screen.fill((255, 255, 255))
        screen.blit(winText1, (0, 0))
        screen.blit(winText2, (0, 36))
        cells = MakeCells(field, cellSize)
        DisplayField(field, cells, cellSize, x0, y0, numFont)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                while True:
                    field = GenerateField(3, 2, 11)
                    if GameEnd(field) == False:
                        break
                scene = "Game mode choice"
                player = 1
                gameEnd = False
pygame.quit()
