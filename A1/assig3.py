import sys, pygame, time
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def visualize(board, wait = False, title="workings"):
    x = len(board)
    y = len(board[0])


    size = width, height = y*21+1, x*21+1
    screen = pygame.display.set_mode(size)
    background = 111, 111, 111
    running = True
    font = pygame.font.SysFont("arial", 16)
    pygame.display.set_caption(title)

    def draw():
        screen.fill(background)
        for ox, line in enumerate(board):
            for oy, char in enumerate(line):
                if char == ".":
                    pygame.draw.rect(screen, WHITE, (oy*21+1, ox*21+1, 20, 20))
                elif char == "#":
                    pygame.draw.rect(screen, BLACK, (oy*21+1, ox*21+1, 20, 20))
                elif char == "A":
                    pygame.draw.rect(screen, RED, (oy*21+1, ox*21+1, 20, 20))
                    screen.blit(font.render("A", True, (0, 0, 0)), (oy*21+5, ox*21+1, 20, 20))
                elif char == "B":
                    pygame.draw.rect(screen, GREEN, (oy*21+1, ox*21+1, 20, 20))
                    screen.blit(font.render("B", True, (0, 0, 0)), (oy*21+5, ox*21+1, 20, 20))
                elif char == "Y":
                    pygame.draw.rect(screen, WHITE, (oy*21+1, ox*21+1, 20, 20))
                    pygame.draw.rect(screen, BLUE, (oy*21+5, ox*21+5, 10, 10))
                    
        pygame.display.update()
    draw()
    if not wait:
        pygame.time.wait(50)
        return

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                draw()
                return
                
