import pygame
import sys
from game import *

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BACKGROUND_COLOR = (120, 120, 120)


class Block(pygame.sprite.Sprite):
	def __init__(self, value, location, size=100, random_appear=False):
		super().__init__()
		self.size = size
		self.image = load_image_from_value(value)
		self.random_appear = random_appear
		if random_appear:
			# self.location[0] += 
			self.image = pygame.transform.scale(self.image, (10, 10))
		self.rect = self.image.get_rect()
		self.rect.topleft = location
		# self.width, self.height = size, size
		self.speed = 25
		self.value= value

	def update(self, i, j, gui):
		bx, by = self.rect.topleft
		if gui.finish_all_animation:
			self.image = load_image_from_value(self.value)
		else:
			if gui.animating_move:
				if gui.move_tracker[i][j] != 0:
					if gui.direction == 'up':  # up
						self.rect.topleft = (bx, by-self.speed)
					elif gui.direction == 'down':  # down
						self.rect.topleft = (bx, by+self.speed)
					elif gui.direction == 'left':  # left
						self.rect.topleft = (bx-self.speed, by)
					else:  # right
						self.rect.topleft = (bx+self.speed, by)
					gui.move_tracker[i][j] -= 0.25
					self.image = load_image_from_value(self.value)
			elif self.random_appear:
				self.rect.topleft = (i*100, j*100)
				self.image = pygame.transform.scale(self.image, (self.rect.width+10, self.rect.width+10))
				self.rect = self.image.get_rect()
				self.rect.topleft = (i*100, j*100)
				if self.rect.width >= 100:
					self.random_appear = False



class GUI():
	def __init__(self, size=4, num_random_appear=2):
		self.animating_move = None
		self.finish_all_animation = None
		self.direction = None
		self.WIDTH = self.HEIGHT = 400
		self.SIZE = size
		self.BLOCK_SIZE = self.WIDTH // self.SIZE
		self.game = Game2048(size, num_random_appear)

		pygame.init()
		pygame.display.set_caption('2048')
		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		self.clock = pygame.time.Clock()
		self.all_sprites = pygame.sprite.Group()
		self.sprite_board = []
		for _ in range(self.SIZE):
			self.sprite_board.append([None] * self.SIZE)
		self.sprite_to_move = []
		self.move_tracker = None
		self.new_num_location = None

		self.generate_sprites_from_board()
		pygame.display.update()


	def generate_sprites_from_board(self):
		self.all_sprites = pygame.sprite.Group()
		for i in range(self.SIZE):
			for j in range(self.SIZE):
				location = (self.BLOCK_SIZE*j, self.BLOCK_SIZE*i)
				block = Block(self.game.board[i][j], location)
				self.all_sprites.add(block)
				self.sprite_board[i][j] = block


	def get_sprite_to_move(self, direction) -> list:
		lst = []
		if direction == 'up':
			for row in self.sprite_board:
				for element in row:
					if element is not None:
						lst.append(element)
		elif direction == 'down':
			for row in self.sprite_board[::-1]:
				for element in row:
					if element is not None:
						lst.append(element)
		elif direction == 'left':
			for col in range(self.SIZE):
				for row in range(self.SIZE):
					if self.sprite_board[row][col] is not None:
						lst.append(self.sprite_board[row][col])
		else:
			for col in range(self.SIZE-1, -1, -1):
				for row in range(self.SIZE):
					if self.sprite_board[row][col] is not None:
						lst.append(self.sprite_board[row][col])
		return lst
	def move(self):
		if not self.game.game_over:
			self.move_tracker, self.new_num_location= self.game.move(self.direction)
		else:
			print('You lose!!!')


def load_image_from_value(value):
	path = f'images/{value}.png'
	return pygame.image.load(path)



class main():
	gui = GUI(num_random_appear=2)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		if gui.finish_all_animation is False:
			if gui.animating_move:
				for i in range(gui.SIZE):
					for j in range(gui.SIZE):
						block = gui.sprite_board[i][j]
						block.update(i, j, gui)
				if max([max(row) for row in gui.move_tracker]) == 0:
					gui.animating_move = False
					for value, location in gui.new_num_location:
						block = Block(value, (location[1]*100, location[0]*100), random_appear=True)
						gui.all_sprites.add(block)
						gui.sprite_board[location[0]][location[1]] = block
			else:

				all_appeared = 0
				if gui.new_num_location is not None:
					for value, location in gui.new_num_location:
						if gui.sprite_board[location[0]][location[1]].random_appear == False:
							all_appeared += 1
						else :
							block = gui.sprite_board[location[0]][location[1]]
							block.update(location[1], location[0], gui)
				if all_appeared == len(gui.new_num_location):

					print('all appeard')
					gui.finish_all_animation = True
					gui.generate_sprites_from_board()
		else:
			key = pygame.key.get_pressed()
			if key[pygame.K_UP]:
				gui.direction = 'up'
			elif key[pygame.K_DOWN]:
				gui.direction = 'down'
			elif key[pygame.K_LEFT]:
				gui.direction = 'left'
			elif key[pygame.K_RIGHT]:
				gui.direction = 'right'

			if key[pygame.K_UP] or key[pygame.K_DOWN] or key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
				gui.move()
				

				gui.finish_all_animation = False
				gui.animating_move = True
				gui.game._display()


		gui.screen.fill(BACKGROUND_COLOR)
		gui.all_sprites.draw(gui.screen)
		pygame.display.update()
		gui.clock.tick(60)
if __name__ == '__main__':
	main()