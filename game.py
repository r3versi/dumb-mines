import numpy as np
from numpy.random import randint
from scipy.signal import convolve2d

class Board:
	'''Contains the rules to define propely a board containing bombs.'''
	def __init__(self,width=10,height=10,n_bombs=10):
		self.width = width
		self.height = height
		if n_bombs<0:	
			n_bombs = 0
		elif n_bombs>width*height:
			n_bombs = width*height
		self.n_bombs = n_bombs
		self.shape = (width, height)

	def generate(self):
		'''Randomly places the bombs on the board.'''
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

	def compute_counts(self):
		'''Employs 2d convolution to find the number of bombs adjacent to a box.'''
		ker = np.array([[1,1,1],[1,0,1],[1,1,1]])
		self.counts = convolve2d(self.bombs, ker, 'same')

	def is_bomb(self,x,y):
		'''Reveals if the box hide a bomb.'''
		return self.bombs[x,y] == 1

	def is_empty(self,x,y):
		'''Reveals if the box is empty.'''
		return self.counts[x,y] == 0

	def inside(self,x,y):
		'''Returns True or Flase depending on whether the coordinates (x,y) fall inside of outside the board.'''
		return (x >= 0) & (y >= 0) & (x < self.width) & (y < self.height)
	
	def load(self,file):
		pass

class Game:
	'''Contains the rules to set up the game.'''
	def __init__(self):
		pass

	def start(self):
		'''Start the game reading from the standard input the features of the board.'''
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
		'''Print the board on the standard output.'''
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

	def run(self):
		'''It asks for your next move and then compute the new board until you win or loose the game.'''		
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
		'''If the box does not hide a bomb, reaveal it and calculate how many adjacent boxes contains bombs. If no mines are adjacent, all adjacent squares are recursively revealed.'''
		if (self.revealed[x,y] == 1) | (self.board.is_bomb(x,y)):
			return
		
		self.revealed[x,y] = 1

		dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

		if self.board.is_empty(x,y):
			for (dx,dy) in dirs:
				if self.board.inside(x+dx,y+dy):
					self.expand_from(x+dx,y+dy)

	def game_over(self):
		'''Set the game over screen.'''
		print('#'*20)
		self.print_board()
		print('Enjoy getting blown :3')

	def victory(self):
		'''Set the victory screen.'''
		print('#'*20)
		self.print_board()
		print('Congrats!!! You won the game, you are not so dumb as I thought...')

if __name__ == "__main__":
	
	game = Game()
	game.start()

	while True:
		if not game.run():
			break