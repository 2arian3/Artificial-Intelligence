from collections import defaultdict

HEIGHT = 900
WIDTH = 900
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
X, Y = 0, 0
COLORS = {'g': (124, 209,  65), #green
          'r': (255,   0,   0), #red
          'b': (152, 244, 245), #blue
          'y': (248, 241,  87), #yellow
          'p': (255,  20, 147), #pink
          'o': (255, 165,   0), #orange
          ' ': (255, 255, 255)} #blank

def drawCells(screen, n, assignment, cells, cellSize):
    import pygame
    for i in range(n):
        for j in range(n):
            color = assignment[(i, j)].get('color', ' ')
            number = assignment[(i, j)].get('number', ' ')
            temp = pygame.Surface((cellSize-6, cellSize-6))
            temp.fill(COLORS[color])
            screen.blit(temp, (X+j*cellSize+3, Y+i*cellSize+3))
            cell = cells[number][color]
            cellRect = cell.get_rect()
            cellRect.center = (X+j*cellSize+cellSize//2, Y+i*cellSize+cellSize//2)
            screen.blit(cell, cellRect)

def visualize(n, colors, totalAssignments):
    import pygame
    pygame.init()

    global COLORS
    global CELLS
    global X
    global Y


    COLORS = {c: value for c, value in COLORS.items() if c in colors or c == ' '}
    font = pygame.font.SysFont('arial.ttf', 50)
    cellSize = (HEIGHT - 100) // n
    X, Y = (WIDTH - n * cellSize) // 2, (HEIGHT - n * cellSize) // 2
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(WHITE)
    

    index = 0
    running = True
    timerInterval = 500 # 0.5 seconds
    timerEvent = pygame.USEREVENT + 1
    pygame.time.set_timer(timerEvent , timerInterval)

    #Creating board lines
    for i in range(n+1):
        pygame.draw.line(screen, BLACK, (X, Y+i*cellSize), (X + n*cellSize, Y+i*cellSize), 3)
        pygame.draw.line(screen, BLACK, (X+i*cellSize, Y), (X+i*cellSize, Y+n*cellSize), 3)

    #Creating each cell based on the colors and numbers
    cells = defaultdict(lambda: defaultdict(lambda: defaultdict()))
    for i in range(1, n+1):
        for j in COLORS:
            cells[i][j] = font.render(str(i), True, BLACK, COLORS[j])
            cells[' '][j] = font.render(' ', True, BLACK, COLORS[j])

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == timerEvent:
                if index < len(totalAssignments):
                    drawCells(screen, n, totalAssignments[index], cells, cellSize)
                index += 1
        pygame.display.update()

    pygame.quit()