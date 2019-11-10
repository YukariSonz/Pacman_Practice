from pacman import Directions
from game import Agent
import api
import random
import game
import util


## Point: Searching Algorithm e.g. BFS, DFS, A*

# Naive: If have some food, go to eat, else find corner.
# After corner finding pick randomish (and prevent reverse moving) movement
# If distance_to_gost<2 , run !!!!!!!!!!!!!! 
"""
class CornerSeekingAgent(Agent):

	def __init__(self):
         self.cornerList = []
         self.stor = []

	def search(self,state,dest):


	#Manhattan Distance calculation
    def distance_cal(source,destination):
        x_dist = abs(destination[0] - source[0])
        y_dist = abs(destination[1] - source[1])
        return x_dist + y_dist

    def find_shortest_unbeen_corner(current_location):
		shortest_distance = 0
		for corner in self.cornerList:
			dist = distance(corner,current_location)


    def getAction(self, state):
		if len(cornerList) == 0:
			cornerList = api.corners(state)
		legal = api.legalActions(state)
		# print(legal)
		current_location = api.whereAmI(state)
		if current_location in cornerList:
			self.stor.append(current_location)
		shortest_corner = 0
		if Directions.STOP in legal:
			legal.remove(Directions.STOP)
"""
class CornerSeekingAgent(Agent):

        # Constructor
    #
    # Create variables to remember target positions
    def __init__(self):
         self.BL = False
         self.TL = False
         self.BR = False
         self.TR = False
         self.happy = True
         self.last = Directions.STOP

    """
    def final(self, state):
         self.BL = False
         self.TL = False
         self.BR = False
         self.TR = False
    """

    #Manhattan Distance calculation
    def distance_cal(self,source,destination):
        x_dist = abs(destination[0] - source[0])
        y_dist = abs(destination[1] - source[1])
        return x_dist + y_dist

    def find_nearest(self,source,list_node):
		current_best_node = (-1,-1)
		if len(list_node) == 0:
			return current_best_node
		else:
			current_min = float("inf") #infinite large
			for node in list_node:
				distance = self.distance_cal(source,node)
				if distance<= current_min:
					current_min = distance
					current_best_node = node
			return current_best_node
			
					


    def getAction(self, state):
        # Get extreme x and y values for the grid
        corners = api.corners(state)
        print corners
        # Setup variable to hold the values
        minX = 100
        minY = 100
        maxX = 0
        maxY = 0

        # Sweep through corner coordinates looking for max and min
        # values.
        for i in range(len(corners)):
            cornerX = corners[i][0]
            cornerY = corners[i][1]

            if cornerX < minX:
                minX = cornerX
            if cornerY < minY:
                minY = cornerY
            if cornerX > maxX:
                maxX = cornerX
            if cornerY > maxY:
                maxY = cornerY

        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        print legal
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Where is Pacman now?
        pacman = api.whereAmI(state)
        print pacman
        
		## TODO: Rewrite the action of pacman when it sees ghosts
        ghost_list = api.ghosts(state)
        print("ghost_list"+str(ghost_list))
        if len(ghost_list) != 0:
            nearest_ghost = self.find_nearest(pacman,ghost_list)
            if pacman[0] < nearest_ghost[0]:
			    if Directions.WEST in legal:
				    self.last = Directions.WEST
				    return api.makeMove(Directions.WEST, legal)
			    # Prevent pacman vibrating
			    elif self.last == Directions.WEST and (Directions.NORTH in legal or Directions.SOUTH in legal):
				    next_list = list(set(legal) - {Directions.WEST, Directions.EAST})
				    pick = random.choice(next_list)
				    self.last = pick
				    return api.makeMove(pick,legal)
            elif pacman[0] > nearest_ghost[0]:
			    if Directions.EAST in legal:
				    self.last = Directions.EAST
				    return api.makeMove(Directions.EAST, legal)
			    # Prevent pacman vibrating
			    elif self.last == Directions.WEST and (Directions.NORTH in legal or Directions.SOUTH in legal):
				    next_list = list(set(legal) - {Directions.WEST, Directions.EAST})
				    pick = random.choice(next_list)
				    self.last = pick
				    return api.makeMove(pick,legal)
            elif pacman[1] < nearest_ghost[1]:
			    if Directions.SOUTH in legal:
				    self.last = Directions.SOUTH
				    return api.makeMove(Directions.SOUTH, legal)
			    # Prevent pacman vibrating
			    elif self.last == Directions.NORTH and (Directions.EAST in legal or Directions.WEST in legal):
				    next_list = list(set(legal) - {Directions.SOUTH, Directions.NORTH})
				    pick = random.choice(next_list)
				    self.last = pick
				    return api.makeMove(pick,legal)
            else:
			    if Directions.NORTH in legal:
				    self.last = Directions.NORTH
				    return api.makeMove(Directions.NORTH, legal)
			    # Prevent pacman vibrating
			    elif self.last == Directions.SOUTH and (Directions.EAST in legal or Directions.WEST in legal):
				    next_list = list(set(legal) - {Directions.SOUTH, Directions.NORTH})
				    pick = random.choice(next_list)
				    self.last = pick
				    return api.makeMove(pick,legal)

		
		
		# TODO: REFACTOR the code to stop letting the pacman vibrating
		# TODO: Provide a mechanism to avoid the ghost
        food_list = api.food(state)
        nearest_food = self.find_nearest(pacman,food_list)
        print "nearest_food is"+str(nearest_food)
        if nearest_food != (-1,-1):
            if pacman[0] > nearest_food[0]:
			    if Directions.WEST in legal:
				    self.last = Directions.WEST
				    return api.makeMove(Directions.WEST, legal)
			    # Prevent pacman vibrating
			    elif self.last == Directions.WEST and (Directions.NORTH in legal or Directions.SOUTH in legal):
				    next_list = list(set(legal) - {Directions.WEST, Directions.EAST})
				    pick = random.choice(next_list)
				    self.last = pick
				    return api.makeMove(pick,legal)
            elif pacman[0] < nearest_food[0]:
			    if Directions.EAST in legal:
				    self.last = Directions.EAST
				    return api.makeMove(Directions.EAST, legal)
			    # Prevent pacman vibrating
			    elif self.last == Directions.WEST and (Directions.NORTH in legal or Directions.SOUTH in legal):
				    next_list = list(set(legal) - {Directions.WEST, Directions.EAST})
				    pick = random.choice(next_list)
				    self.last = pick
				    return api.makeMove(pick,legal)
            elif pacman[1] > nearest_food[1]:
			    if Directions.SOUTH in legal:
				    self.last = Directions.SOUTH
				    return api.makeMove(Directions.SOUTH, legal)
			    # Prevent pacman vibrating
			    elif self.last == Directions.NORTH and (Directions.EAST in legal or Directions.WEST in legal):
				    next_list = list(set(legal) - {Directions.SOUTH, Directions.NORTH})
				    pick = random.choice(next_list)
				    self.last = pick
				    return api.makeMove(pick,legal)
            else:
			    if Directions.NORTH in legal:
				    self.last = Directions.NORTH
				    return api.makeMove(Directions.NORTH, legal)
			    # Prevent pacman vibrating
			    elif self.last == Directions.SOUTH and (Directions.EAST in legal or Directions.WEST in legal):
				    next_list = list(set(legal) - {Directions.SOUTH, Directions.NORTH})
				    pick = random.choice(next_list)
				    self.last = pick
				    return api.makeMove(pick,legal)
			
			
				
		
		
				
				

        #
        # If we haven't got to the lower left corner, try to do that
        #

        # Check we aren't there:
        if pacman[0] == minX + 1:
            if pacman[1] == minY + 1:
                self.BL = True
		
        # If not, move towards it, first to the West, then to the South.
        if self.BL == False:
            if pacman[0] > minX + 1:
                if Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)


        #
        # Now we've got the lower left corner
        #

        # Move towards the top left corner
        
        # Check we aren't there:
        if pacman[0] == minX + 1:
           if pacman[1] == maxY - 1:
                self.TL = True

        # If not, move West then North.
        if self.TL == False:
            if pacman[0] > minX + 1:
                if Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

        # Now, the top right corner

        # Check we aren't there:
        if pacman[0] == maxX - 1:
           if pacman[1] == maxY - 1:
                self.TR = True

        # Move east where possible, then North
        if self.TR == False:
            if pacman[0] < maxX - 1:
                if Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

        # Fromto right it is a straight shot South to get to the bottom right.

        if pacman[0] == maxX - 1:
           if pacman[1] == minY + 1:
                self.BR = True
                return api.makeMove(random.choice(legal), legal)
           else:
               print "Nearly there"
               return api.makeMove(Directions.SOUTH, legal)
        

        return api.makeMove(random.choice(legal), legal)
