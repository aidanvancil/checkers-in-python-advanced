import pygame

# @properties
#####################################################################################

ROWS = 8
COLS = 8
SIZE = HEIGHT, WIDTH = 1000, 1000       # optimally 1:1 aspect ratio
BOX_SIZE = SIZE[0]//ROWS

# RGB
#####################################################################################

BLACK = (0,0,0)
OUTLINE = (255, 128, 0)
red = [220,20, 60]
GRAY = (128, 128, 128)
WHITE = (255,255,255)
TITLE_SCREEN_BG = (245, 69, 66)
BEIGE = (207, 185, 151)

# EXTERNAL ASSETS
#####################################################################################
def color(r, g, b) -> None:
	if red[0] < 255 and red[0] > 0:
		red[0] += r
	if red[1] < 255 and red[1] > 0:
		red[1] += g
	if red[2] < 255 and red[2] > 0:
		red[2] += b
	return None

volatility = [True, False]

def probability_volatility() -> str:
	count = 0
	for i in volatility:
		if i == True:
			count += 1
	return(str(round((count / (len(volatility) / 100)))) + '%')

def change_volatility(val) -> None:
	if val == -1 and (len(volatility) > 1):
		volatility.pop()
	elif (len(volatility) < 20) and val != -1:
		volatility.append(False)
	return None

CROWN = pygame.transform.scale(pygame.image.load(r'assets/crown.png'), (65, 45))
IS_SELECTED = pygame.transform.scale(pygame.image.load(r'assets/selected.png'), (45, 45))
pygame.mixer.init()
MOVE_WAV = pygame.mixer.Sound(r'assets/move_piece.wav')
MOVE_WAV.set_volume(0.3)
KING_WAV = pygame.mixer.Sound(r'assets/king_piece.wav')
KING_WAV.set_volume(0.3)
BACKGROUND_WAV = pygame.mixer.music.load(r'assets/background.mp3')
TITLE_CHECKERS = pygame.transform.scale(pygame.image.load(r'assets/title_checkers.png'), (250, 250))
pygame.mixer.music.set_volume(0.02)
pygame.mixer.music.play(-1)