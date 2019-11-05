from pacman import Directions
from game import Agent
import api
import random
import game
import util



class GoWestAgent(Agent):
	"""
	def __init__(self):
         self.last = Directions.STOP
	"""
	def getAction(self, state):
		legal = api.legalActions(state)
		# print(legal)
		if Directions.STOP in legal:
			legal.remove(Directions.STOP)
		if Directions.WEST in legal:
			self.last = Directions.WEST
			return api.makeMove(Directions.WEST,legal)
		else:
			
			if self.last in legal:
				return api.makeMove(self.last, legal)
			else:	
				pick = random.choice(legal)
				self.last = pick
				return api.makeMove(pick, legal)
			
			"""
			if self.last == Directions.WEST:
				legal.remove(Directions.EAST)
				if self.last in legal:
					return api.makeMove(self.last,legal)
				else:
					pick = random.choice(legal)
					print(pick)
					self.last = pick
					return api.makeMove(pick, legal)
			"""
				
				
			
