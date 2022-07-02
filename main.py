from gui import *
import argparse



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='These are some arguments that help you config the game',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-s', '--size', help='Set the size of the board', default=4, type=int)
	parser.add_argument('-r', '--random', help='Number of random element appear after each movement', default=1, type=int)
	parser.add_argument('-m', '--max', help='Max score', default=2048, type=int)
	args = parser.parse_args()
	config = vars(args)
	if 2**((config['size']**2)-1) < config['max']:
		config['max'] = 2**(config['size']**2-1)
		print(f'max_score are set to {config["max"]} because the the size is quite small compared to max score')
		# raise Exception('The size is quite small compared to max score')
	if config['size'] < config['random']:
		raise Exception('The size must be greater than random')
	main(config['size'], config['random'], config['max'])