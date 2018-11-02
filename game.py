import numpy as np
from numpy.random import randint
from scipy.signal import convolve2d

############################################################################
# This class contains the rules to define propely a Board containing bombs #
############################################################################

class Board:
	def __init__(self,width=10,height=10,n_bombs=10):
		self.width = width
		self.height = height
		if n_bombs<0:	
			n_bombs = 0
		elif n_bombs>width*height:
			n_bombs = width*height
		self.n_bombs = n_bombs
		self.shape = (width, height)

	# This method randomly place the bombs on the board
	def generate(self):
		self.bombs = np.zeros(shape = (self.width, self.height), dtype=np.int8)
		
		placed = 0
		while placed < self.n_bombs:
			x = randint(0, self.width)
			y = randint(0, self.height)

			if self.is_bomb(x,y):
				continue

			self.bombs[x,y] = 1
			placed += 1

		self.compute_counts()

	# This method employs 2d convolution to find the number of bombs nearby a dowel
	def compute_counts(self):
		ker = np.array([[1,1,1],[1,0,1],[1,1,1]])
		self.counts = convolve2d(self.bombs, ker, 'same')

	def is_bomb(self,x,y):
		return self.bombs[x,y] == 1

	def is_empty(self,x,y):
		return self.counts[x,y] == 0

	def inside(self,x,y):
		return (x >= 0) & (y >= 0) & (x < self.width) & (y < self.height)
	
	def load(self,file):
		pass

####################################################
# This class contains the rules to set up the game #
####################################################
class Game:
	def __init__(self):
		pass

	# This method start the games reading external input the features of the board
	def start(self):
		print('#'*20)
		print("## Mines of doom v0.1\n")

		while True:
			try:
				width = int(input("Width: "))
				height = int(input("Height: "))
				n_bombs = int(input("Bombs: "))
				self.board = Board(width,height,n_bombs)
				self.board.generate()
			except:
				print("I am not as dumb as you think... insert valid values for width, height and number of bombs")
				continue
			else:
				break
		
		self.alive = True
		self.revealed = np.zeros(shape = self.board.shape)
	
	def print_board(self):

		for x in range(self.board.width):
			for y in range(self.board.height):
				if self.revealed[x,y]:
					if self.board.bombs[x,y]:
						print('B', end = ' ')
					else:
						print(self.board.counts[x,y], end = ' ')
				else:
					print('X', end=' ')
			print()

	# This is the core method: it runs until you win or loose the game
	# It ask for your next move and then compute the new board
	def run(self):
		
		print('#'*20)
		self.print_board()

		while True:
			try:
				print("Your next move (format X Y): ",end='')
				x, y = [int(i) for i in input().split()]
				if not self.board.inside(x,y):
					print('It\'s out of the board mate')
					continue
				break
			except:
				print('Don\'t be dumb mate, just give me a valid move')
				continue
			else:
				break
		
		if self.board.is_bomb(x,y):
			self.revealed = np.ones(shape=self.board.shape)
			self.alive = False
			self.game_over()
		else:
			self.expand_from(x,y)

		if np.count_nonzero(self.revealed==0) == self.board.n_bombs:
			self.revealed = np.ones(shape=self.board.shape)
			self.alive = False
			self.victory()

		return self.alive
	
	def expand_from(self, x, y):
		
		if (self.revealed[x,y] == 1) | (self.board.is_bomb(x,y)):
			return
		
		self.revealed[x,y] = 1

		dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

		if self.board.is_empty(x,y):
			for (dx,dy) in dirs:
				if self.board.inside(x+dx,y+dy):
					self.expand_from(x+dx,y+dy)

	def game_over(self):
		print('#'*20)
		self.print_board()
		print('Enjoy getting blown :3')

	def victory(self):
		print('#'*20)
		self.print_board()
		print('Congrats!!! You won the game, you are not so dumb as I thought...')

if __name__ == "__main__":
	
	game = Game()
	game.start()

	while True:
		if not game.run():
			break