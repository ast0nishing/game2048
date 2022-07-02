import pygame
import sys
from game import Game2048


class Block(pygame.sprite.Sprite):
	def __init__(self, value, location, size=100, random_appear=False):
		super().__init__()
		self.size = size
		self.image = load_image_from_value(value)
		self.random_appear = random_appear
		if random_appear:
			self.image = pygame.transform.scale(self.image, (10, 10))
		self.rect = self.image.get_rect()
		self.rect.topleft = location
		self.speed = 25
		self.value= value

	def update(self, i, j, gui):
		bx, by = self.rect.topleft
		if gui.animating_move:
			if gui.move_tracker[i][j] > 0:
				if gui.direction == 'up':  # up
					self.rect.topleft = (bx, by-self.speed)
				elif gui.direction == 'down':  # down
					self.rect.topleft = (bx, by+self.speed)
				elif gui.direction == 'left':  # left
					self.rect.topleft = (bx-self.speed, by)
				elif gui.direction == 'right':  # right
					self.rect.topleft = (bx+self.speed, by)
				gui.move_tracker[i][j] -= 0.25
		if self.random_appear:
			self.rect.topleft = (i*100, j*100)
			self.image = pygame.transform.scale(self.image, (self.rect.width+10, self.rect.width+10))
			self.rect = self.image.get_rect()
			self.rect.topleft = (i*100, j*100)
			if self.rect.width >= self.size:
				self.random_appear = False



class GUI():
	def __init__(self, size=4, num_random_appear=2, max_score=2048):
		self.NUM_RANDOM_APPEAR = num_random_appear
		self.MAX_SCORE = max_score
		
		self.WIDTH = self.HEIGHT = 400
		self.SIZE = size
		self.BLOCK_SIZE = self.WIDTH // self.SIZE
		self.game = Game2048(size, num_random_appear, max_score)

		pygame.init()
		pygame.display.set_caption('2048')
		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		self.clock = pygame.time.Clock()
		self.init_parameters()
		pygame.display.update()
		

	def init_parameters(self):
		self.animating_move = None
		self.finish_all_animation = None
		self.direction = None

		self.all_sprites = pygame.sprite.Group()
		self.sprite_board = []
		for _ in range(self.SIZE):
			self.sprite_board.append([None] * self.SIZE)
		self.sprite_to_move = []
		self.move_tracker = None
		self.merge_tracker = None
		self.new_num_location = None

		self.generate_sprites_from_board()

	def generate_sprites_from_board(self):
		self.all_sprites = pygame.sprite.Group()
		for i in range(self.SIZE):
			for j in range(self.SIZE):
				location = (self.BLOCK_SIZE*j, self.BLOCK_SIZE*i)
				block = Block(self.game.board[i][j], location)
				self.all_sprites.add(block)
				self.sprite_board[i][j] = block

	def move(self):
		if not self.game.game_over:
			self.move_tracker, self.merge_tracker, self.new_num_location= self.game.move(self.direction)
		else:
			print('You lose!!!')



def load_image_from_value(value):
	path = f'images/{value}.png'
	return pygame.image.load(path)



def main(size=4, num_random_appear=1, max_score=2048):
	BACKGROUND_COLOR = (120, 120, 120)
	display_last = True
	gui = GUI(size, num_random_appear, max_score)
	while True:
		key = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		if not gui.game.game_over:
			if gui.finish_all_animation is False:
				# move animation
				if gui.animating_move:
					for i in range(gui.SIZE):
						for j in range(gui.SIZE):
							block = gui.sprite_board[i][j]
							block.update(i, j, gui)
					if max([max(row) for row in gui.move_tracker]) == 0:
						gui.animating_move = False

						# merge animation
						for i in range(gui.SIZE):
							for j in range(gui.SIZE):
								if gui.merge_tracker[i][j] != 0:
									block = Block(gui.merge_tracker[i][j], (j*100, i*100))
									gui.all_sprites.add(block)
									gui.sprite_board[i][j] = block
									
						# add random values after a move
						if gui.new_num_location is not None and len(gui.new_num_location) != 0:
							for value, location in gui.new_num_location:
								block = Block(value, (location[1]*100, location[0]*100), random_appear=True)
								gui.all_sprites.add(block)
								gui.sprite_board[location[0]][location[1]] = block

				else:
					# add random values animation
					all_appeared = 0
					if gui.new_num_location is not None:
						for value, location in gui.new_num_location:
							if gui.sprite_board[location[0]][location[1]].random_appear == False:
								all_appeared += 1
							else :
								block = gui.sprite_board[location[0]][location[1]]
								block.update(location[1], location[0], gui)
						if all_appeared == len(gui.new_num_location):
							gui.finish_all_animation = True
							gui.generate_sprites_from_board()
			else:
				
				if key[pygame.K_UP]:
					gui.direction = 'up'
				elif key[pygame.K_DOWN]:
					gui.direction = 'down'
				elif key[pygame.K_LEFT]:
					gui.direction = 'left'
				elif key[pygame.K_RIGHT]:
					gui.direction = 'right'
				if key[pygame.K_UP] or key[pygame.K_DOWN] or key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
					if gui.game.can_move(gui.direction):
						gui.move()
						gui.finish_all_animation = False
						gui.animating_move = True
						gui.game._display()
					else:
						print('cant move')
		elif display_last:
			display_last = False

			gui.generate_sprites_from_board()
		
		if gui.game.game_over and gui.game.is_lose:
			BACKGROUND_COLOR = (255, 0, 0)
		elif gui.game.game_over and gui.game.is_win:
			BACKGROUND_COLOR = (0, 255, 0)
		if gui.game.game_over and key[pygame.K_SPACE]:
			gui.game = Game2048(gui.SIZE, gui.NUM_RANDOM_APPEAR, gui.MAX_SCORE)
			BACKGROUND_COLOR = (120, 120, 120)
			gui.init_parameters()
			display_last = True


		gui.screen.fill(BACKGROUND_COLOR)
		gui.all_sprites.draw(gui.screen)
		pygame.display.update()
		gui.clock.tick(60)
