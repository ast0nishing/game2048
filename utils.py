def check_valid_move(func):
	def wrapper(*args, **kwargs):
		if str(args[1]) not in ['left', 'right', 'up', 'down']:
			print(str(args[1]))
			raise Exception('Direction is not valid')
		func(*args, **kwargs)
	return wrapper

def get_available_positions(board: list[list[int]]) -> list[tuple]:
	available_positions = []
	size = len(board[0])
	for row in range(size):
		for col in range(size):
			if board[row][col] == 0:
				available_positions.append((row, col))
	return available_positions

def get_largest_num(board: list[list[int]]) -> int:
		return max([max(row) for row in board])