import random 
from utils import *
import copy

class Game2048:
	def __init__(self, size=4, num_random_appear=2, on_terminal=False):
		assert size >= num_random_appear, "num_random_appear can't be greater than size"
		self.on_terminal = on_terminal
		self.size = size
		self.num_random_appear = num_random_appear
		self.board = []
		for _ in range(size):
			self.board.append([0] * size)
		# self.board = [
		# 		[0, 0, 2, 0],
		# 		[0, 2, 2, 0],
		# 		[0, 2, 2, 0],
		# 		[0, 0, 2, 0]
		# ]
		self.new_appear_location = self._random_appear()
		if self.on_terminal:
			self._display()

		self.game_over = False

	def _display(self) -> None:
		largest_num = get_largest_num(self.board)
		space = len(str(largest_num))
		for row in self.board:
			row_element = '|'
			for element in row:
				if element == 0:
					row_element += ' '*space + '|'
				else:
					row_element += ' '*(space-len(str(element))) + str(element) + '|'
			print(row_element)
		print()


	def move(self, direction: str):
		if self.game_over is False:
			move_tracker, merge_tracker = self._move(direction)
			print(f'moved {direction}')
			num_and_pos = self._random_appear()
			if self.on_terminal:
				self._display()
			self.check_game_state()
			return move_tracker, merge_tracker, num_and_pos
	def can_move(self, direction):
		if direction in ['left', 'right']:
			for i in range(self.size):
				for j in range(self.size-1):
					if self.board[i][j] == self.board[i][j+1]:
						return True


	def _move(self, direction) -> list[list[int]]:
		move_tracker = [[0]*self.size for _ in range(self.size)]
		merge_tracker = [[0]*self.size for _ in range(self.size)]
		if direction in ['left', 'right']:
			for row_index, row in enumerate(self.board):
				merged_index = -1
				if direction=='right':
					row = list(reversed(row))
				for i, element in enumerate(row[1:], 1):
					if element == 0:
						continue
					element_move_tracker = 0
					for j in range(i-1, -1, -1):
						if row[j] == 0:
							element_move_tracker += 1
						elif row[j] == row[i]:
							if merged_index == j:
								break
							element_move_tracker += 1
							merged_index = j
							merge_tracker[row_index][j] = row[i]*2
							break
						if row[j] != 0:
							break
					if element_move_tracker != 0:
						row[i-element_move_tracker], row[i] = row[i-element_move_tracker]+row[i], 0
					if direction == 'left':
						move_tracker[row_index][i] = element_move_tracker
					else:
						move_tracker[row_index][self.size-1-i] = element_move_tracker
				if direction=='right':
					merge_tracker = [list(reversed(row_merge_tracker)) for row_merge_tracker in merge_tracker]
					# move_tracker = [list(reversed(row_move_tracker)) for row_move_tracker in move_tracker]
					self.board[row_index] = list(reversed(row))
			return move_tracker, merge_tracker
		elif direction in ['up', 'down']:
			for column_index in range(self.size):
				col = [row[column_index] for row in self.board]
				merged_index = -1
				if direction == 'down':
					col = list(reversed(col))
				for i, element in enumerate(col[1:], 1):
					if element == 0:
						continue
					element_move_tracker = 0
					for j in range(i-1, -1, -1):
						if col[j] == 0:
							element_move_tracker += 1
						elif col[j] == col[i]:
							if merged_index == j:
								break
							element_move_tracker += 1
							merged_index = j
							if direction == 'up':
								merge_tracker[j][column_index] = col[j]*2
							else:
								merge_tracker[self.size-1-j][column_index] = col[j]*2
							break
						if col[j] != 0:
							break
					if element_move_tracker != 0:
						col[i-element_move_tracker], col[i] = col[i-element_move_tracker]+col[i], 0
					if direction == 'down':
						move_tracker[self.size-1-i][column_index] = element_move_tracker
					else:
						move_tracker[i][column_index] = element_move_tracker
					
				if direction == 'down':
					col = list(reversed(col))
				for i in range(self.size):
					self.board[i][column_index] = col[i]
			return move_tracker, merge_tracker


	def _random_appear(self) -> list[int, tuple[int]]:
		# get all 0 positions
		available_positions = get_available_positions(self.board)
		if len(available_positions) == 0:
			return
		choices = [2, 4]
		weights = [9, 8]
		check_largest_num = [8, 16, 32, 64, 128, 256, 512]
		for i, num in enumerate(check_largest_num):
			if get_largest_num(self.board) > num:
				choices.append(num)
				weights.append(7-i)
				continue
			break
		num_and_pos = []
		pos = random.choices(available_positions, k=self.num_random_appear)
		for i in range(self.num_random_appear):
			num = random.choices(choices, weights, k=1)[0]
			self.board[pos[i][0]][pos[i][1]] = num
			num_and_pos.append([num, pos[i]])
		return num_and_pos

	def _is_win(self):
			return True if get_largest_num(self.board) == 2048 else False

	def _is_lose(self):
		if len(get_available_positions(self.board)) == 0:
			for i in range(self.size):
				for j in range(self.size-1):
					if self.board[i][j] == self.board[i][j+1] or self.board[j][i] == self.board[j+1][i]:
						return False
			return True
		return False

	def check_game_state(self):
		if self._is_lose():
			self.game_over = True
			print('you lose!!!')
		if self._is_win():
			self.game_over = True
			print('you won!!!!!!')


if __name__ == '__main__':
	game = Game2048(size=4, num_random_appear=2, on_terminal=True)
	game.move('right')
	# game.move('right')
	# game.move('right')