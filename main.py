from checkers.constants import SIZE, GRAY, TITLE_SCREEN_BG, BLACK, red, OUTLINE, TITLE_CHECKERS
from checkers.game import Game
from checkers.sidebar import Sidebar
import logging
import sys

# NEEDED IMPORT(S)
#####################################################################################

try:
    import pygame
except ImportError as e:
    print("\n\t can't run, check requirements.txt for needed installs\n" )
    sys.exit()
    pass  


pygame.init()

# Improvements + QOL from @aidanvancil


# DISPLAY
#####################################################################################
FPS = 60
WINDOW = pygame.display.set_mode((SIZE), pygame.RESIZABLE)
pygame.display.set_caption('Checkers')
fontObj = pygame.font.Font(None, 32)
mainObj = pygame.font.Font(None, 140)
# TEXTS
menu = fontObj.render('Menu', True, (0, 255, 0), None)
title_text = mainObj.render('Checkers', True, GRAY, None)
title_text2 = mainObj.render('Checkers', True, BLACK, None)


def build_text() -> None:
    GAMEMODES = ['[1] REGULAR', '[2] ONLY KINGS', '[3] RANDOMLY SELECTED KING', '[4] TWO MOVES EVERY TURN', 'EXIT']
    GM1 = fontObj.render(GAMEMODES[0], True, BLACK, None)
    GM2 = fontObj.render(GAMEMODES[1], True, BLACK, None)
    GM3 = fontObj.render(GAMEMODES[2], True, BLACK, None)
    GM4 = fontObj.render(GAMEMODES[3], True, BLACK, None)
    GM5 = fontObj.render(GAMEMODES[4], True, BLACK, None)
    GMs = [GM1, GM2, GM3, GM4, GM5]
    return GMs

def draw_text(WINDOW, GMs) -> None:
    WINDOW.blit(GMs[0], (350, 350))
    WINDOW.blit(GMs[1], (350, 450))
    WINDOW.blit(GMs[2], (350, 550))
    WINDOW.blit(GMs[3], (350, 650))
    WINDOW.blit(GMs[4], (350, 750))

def main() -> None:
    game = Game(WINDOW)
    clock = pygame.time.Clock()
    GMs = build_text()
    running, title_screen = True, True
    count, selection = 0, None
    sidebar_bool = False
    vol = 0.02
    while running:
        clock.tick(FPS)

        if game.win_condition() != None:
            running = False
    
        for event in pygame.event.get():    
            if (title_screen) and (count == 0):
                    WINDOW.fill(TITLE_SCREEN_BG)
                    WINDOW.blit(title_text2, (235, 15))
                    WINDOW.blit(title_text, (240, 20))
                    WINDOW.blit(TITLE_CHECKERS, (340, 130))
                    count += 1
                    draw_text(WINDOW, GMs)
            elif title_screen:
                    if (pygame.draw.rect(WINDOW, BLACK, pygame.Rect(270, 350, 65, 65)).collidepoint(pygame.mouse.get_pos()) or pygame.draw.rect(WINDOW, GRAY, pygame.Rect(275, 355, 40, 55)).collidepoint(pygame.mouse.get_pos())) and event.type == pygame.MOUSEBUTTONDOWN:              
                        title_screen = False
                        selection = 1
                    elif (pygame.draw.rect(WINDOW, BLACK, pygame.Rect(270, 450, 65, 65)).collidepoint(pygame.mouse.get_pos()) or pygame.draw.rect(WINDOW, GRAY, pygame.Rect(275, 450, 40, 55)).collidepoint(pygame.mouse.get_pos())) and event.type == pygame.MOUSEBUTTONDOWN:             
                        title_screen = False
                        selection = 2
                    elif (pygame.draw.rect(WINDOW, BLACK, pygame.Rect(270, 550, 65, 65)).collidepoint(pygame.mouse.get_pos()) or pygame.draw.rect(WINDOW, GRAY, pygame.Rect(275, 550, 40, 55)).collidepoint(pygame.mouse.get_pos())) and event.type == pygame.MOUSEBUTTONDOWN:            
                        title_screen = False
                        selection = 3
                    elif (pygame.draw.rect(WINDOW, BLACK, pygame.Rect(270, 650, 65, 65)).collidepoint(pygame.mouse.get_pos()) or pygame.draw.rect(WINDOW, GRAY, pygame.Rect(275, 650, 40, 55)).collidepoint(pygame.mouse.get_pos())) and event.type == pygame.MOUSEBUTTONDOWN:
                        title_screen = False
                        selection = 4
                    elif (pygame.draw.rect(WINDOW, BLACK, pygame.Rect(270, 750, 65, 65)).collidepoint(pygame.mouse.get_pos()) or pygame.draw.rect(WINDOW, GRAY, pygame.Rect(275, 750, 40, 55)).collidepoint(pygame.mouse.get_pos())) and event.type == pygame.MOUSEBUTTONDOWN:
                        running = False
                    pygame.display.update()

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = game.get_rows_cols(x, y)
                game.selected(row, col)
        if not title_screen:
            while count == 1:
                count -= 1
                game.gamemode(selection)
            game.update()
            if (pygame.draw.rect(WINDOW, GRAY, pygame.Rect(883, 970, 110, 105)).collidepoint(pygame.mouse.get_pos()) or pygame.draw.rect(WINDOW, BLACK, pygame.Rect(884, 971, 108, 106)).collidepoint(pygame.mouse.get_pos())) and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.time.wait(100)
                if sidebar_bool == False:
                    sidebar_bool = True
                else:
                    sidebar_bool = False
            if sidebar_bool:
                sidebar = Sidebar(WINDOW, game, vol) 
                vol, surrender, home = sidebar.draw_sidebar(event)
                if surrender:
                    running = False
                if home:
                    game.reset(WINDOW)
                    title_screen = True
                    count = 0
                    selection = None
            WINDOW.blit(menu, (883, 975))
            pygame.display.update()
            

    if running:
        logging.error('runtime skipped over game.win_condition()')
        
    pygame.quit()

if __name__ == '__main__':
    main()
