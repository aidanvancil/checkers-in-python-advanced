import pygame

from .board import Board
from .constants import BEIGE, red, GRAY, BLACK, color, change_volatility, volatility, probability_volatility
from .game import *

# INTIALIZING & UPDATES
#####################################################################################
class Sidebar():
	def __init__(self, WINDOW, game, vol):
		self.window = WINDOW
		OUTLINE = (0, 255, 0)

		# FONT RENDERING
		fontObj = pygame.font.Font(None, 32)
		fontRGB = pygame.font.Font(None, 20)
		fontWinner = pygame.font.Font(None, 90)

		# SURRENDERING
		self.surrender = fontObj.render('Surrender', True, OUTLINE, None)

		# PIECE/KING DESC.
		self.piece_count_red = fontObj.render('Your Pieces: ', True, OUTLINE, None)
		self.piece_count_red_count = fontObj.render(str(game.board.red_pieces), True, OUTLINE, None)
		self.piece_count_gray = fontObj.render('Gray Pieces: ', True, OUTLINE, None)
		self.piece_count_gray_count = fontObj.render(str(game.board.gray_pieces), True, OUTLINE, None)
		self.king_count_red = fontObj.render('Your Kings: ', True, OUTLINE, None)
		self.king_count_red_count = fontObj.render(str(game.board.red_kings), True, OUTLINE, None)
		self.king_count_gray = fontObj.render('Gray Kings: ', True, OUTLINE, None)
		self.king_count_gray_count = fontObj.render(str(game.board.gray_kings), True, OUTLINE, None)

		# VOLUME
		self.volume = fontObj.render('Volume: ', True, OUTLINE, None)
		self.volume_plus = fontObj.render('+', True, OUTLINE, None)
		self.volume_minus = fontObj.render('-', True, OUTLINE, None)
		self.volume_variable = vol

		# RBG COLORING
		self.color_myself = fontObj.render('Your Color: ', True, OUTLINE, None)
		self.color_myself_rep = fontRGB.render(('({R}, {G}, {B})'.format(R=str(red[0]), G=str(red[1]), B=str(red[2]))), True, OUTLINE, None)
		self.color_enemy = fontObj.render('Enemy Color: ', True, OUTLINE, None)
		self.color_enemy_rep = fontRGB.render(('({R}, {G}, {B})'.format(R=str(GRAY[0]), G=str(GRAY[1]), B=str(GRAY[2]))), True, OUTLINE, None)

		# RANDOMNESS / VOLATILITY
		self.enemy_rng = fontObj.render('Enemy Volatility: ', True, OUTLINE, None)
		self.volatility_count = fontRGB.render(('{var}'.format(var=str(len(volatility)))), True, OUTLINE, None)
		self.volatility_prob = fontRGB.render((probability_volatility()), True, OUTLINE, None)

		# HOME
		self.hometext = fontObj.render('Home', True, OUTLINE, None)

	def draw_sidebar(self, event) -> None:
		self.event = event
		pygame.draw.rect(self.window, BEIGE, pygame.Rect(683, 300, 310, 855))
		pygame.draw.rect(self.window, BLACK, pygame.Rect(700, 340, 270, 830))
		switch = self.draw_surrender()
		self.draw_piece_count()
		self.draw_king_count()
		vol = self.draw_volume_slider()
		self.draw_color_changer()
		self.draw_volatility()
		home = self.draw_home()
		return vol, switch, home

	def draw_surrender(self) -> bool:
		if self.window.blit(self.surrender, (700, 350)).collidepoint(pygame.mouse.get_pos()) and self.event.type == pygame.MOUSEBUTTONDOWN:
			return True
		return False

	def draw_piece_count(self) -> None:
		self.window.blit(self.piece_count_red, (700, 450))
		self.window.blit(self.piece_count_red_count, (870, 450))
		self.window.blit(self.piece_count_gray, (700, 500))
		self.window.blit(self.piece_count_gray_count, (870, 500))
		return None

	def draw_king_count(self) -> None:
		self.window.blit(self.king_count_red, (700, 600))
		self.window.blit(self.king_count_red_count, (870, 600))
		self.window.blit(self.king_count_gray, (700, 650))
		self.window.blit(self.king_count_gray_count, (870, 650))
		return None

	def draw_volume_slider(self) -> None:
		self.window.blit(self.volume, (700, 730))
		if self.window.blit(self.volume_plus, (850, 730)).collidepoint(pygame.mouse.get_pos()) and self.event.type == pygame.MOUSEBUTTONDOWN:
			pygame.time.wait(100)
			self.volume_variable += 0.005
			pygame.mixer.music.set_volume(self.volume_variable)
		if self.window.blit(self.volume_minus, (900, 730)).collidepoint(pygame.mouse.get_pos()) and self.event.type == pygame.MOUSEBUTTONDOWN:
			pygame.time.wait(100)
			self.volume_variable -= 0.005
			pygame.mixer.music.set_volume(self.volume_variable)
		return self.volume_variable

	def draw_color_changer(self) -> tuple:
		self.window.blit(self.color_myself, (700, 800))
		self.window.blit(self.color_myself_rep, (870, 800))
		self.window.blit(self.color_enemy, (700, 850))
		self.window.blit(self.color_enemy_rep, (870, 850))

		if self.window.blit(self.volume_plus, (877, 810)).collidepoint(pygame.mouse.get_pos()) and self.event.type == pygame.MOUSEBUTTONDOWN:
			pygame.time.wait(100)
			color(1, 0, 0)
		if self.window.blit(self.volume_plus, (902, 810)).collidepoint(pygame.mouse.get_pos()) and self.event.type == pygame.MOUSEBUTTONDOWN:
			pygame.time.wait(100)
			color(0, 1, 0)
		if self.window.blit(self.volume_plus, (927, 810)).collidepoint(pygame.mouse.get_pos()) and self.event.type == pygame.MOUSEBUTTONDOWN:
			pygame.time.wait(100)
			color(0, 0, 1)
		if self.window.blit(self.volume_minus, (880, 830)).collidepoint(pygame.mouse.get_pos()) and self.event.type == pygame.MOUSEBUTTONDOWN:
			pygame.time.wait(100)
			color(-1, 0, 0)
		if self.window.blit(self.volume_minus, (905, 830)).collidepoint(pygame.mouse.get_pos()) and self.event.type == pygame.MOUSEBUTTONDOWN:
			pygame.time.wait(100)
			color(0, -1, 0)
		if self.window.blit(self.volume_minus, (930, 830)).collidepoint(pygame.mouse.get_pos()) and self.event.type == pygame.MOUSEBUTTONDOWN:
			pygame.time.wait(100)
			color(0, 0, -1)
		return red

	def draw_home(self) -> bool:
		if self.window.blit(self.hometext, (720, 975)).collidepoint(pygame.mouse.get_pos()) and self.event.type == pygame.MOUSEBUTTONDOWN:
			pygame.time.wait(100)
			return True
		return False

	def draw_volatility(self) -> None:
		self.window.blit(self.enemy_rng, (700, 900))
		self.window.blit(self.volatility_count, (920, 930))
		self.window.blit(self.volatility_prob, (915, 950))
		if self.window.blit(self.volume_plus, (900, 900)).collidepoint(pygame.mouse.get_pos()) and self.event.type == pygame.MOUSEBUTTONDOWN:
			pygame.time.wait(100)
			change_volatility(1)
		if self.window.blit(self.volume_minus, (935, 900)).collidepoint(pygame.mouse.get_pos()) and self.event.type == pygame.MOUSEBUTTONDOWN:
			pygame.time.wait(100)
			change_volatility(-1)
		return None