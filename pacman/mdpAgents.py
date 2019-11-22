# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

class Grid:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        subgrid = []
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                row.append(0)
            subgrid.append(row)

        self.grid = subgrid

        subgrid_utility = []
        for i in range(self.height):
            row_utility=[]
            for j in range(self.width):
                row_utility.append(0.5) # Init Utility
            subgrid_utility.append(row_utility)
        self.utilities = subgrid_utility



    def setValue(self, x, y, value):
        self.grid[y][x] = value

    def getValue(self, x, y):
        return self.grid[y][x]

    # Return width and height to support functions that manipulate the
    # values stored in the grid.
    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getUtility(self,x,y):
        return self.utilities[y][x]

    def setUtility(self, x, y, utility):
        self.utilities[y][x] = utility

class MDPAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        print "Starting up MDPAgent!"
        name = "Pacman"

    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    def registerInitialState(self, state):
        print "Running registerInitialState for MDPAgent!"
        print "I'm at:"
        print api.whereAmI(state)
        self.makeMap(state)
        self.addWallsToMap(state)
        self.updateFoodInMap(state)
        self.calculateUtility(state)

    def makeMap(self,state):
        corners = api.corners(state)
        print corners
        height = self.getLayoutHeight(corners)
        width  = self.getLayoutWidth(corners)
        self.map = Grid(width, height)

    def getLayoutHeight(self, corners):
        height = -1
        for i in range(len(corners)):
            if corners[i][1] > height:
                height = corners[i][1]
        return height + 1

    def getLayoutWidth(self, corners):
        width = -1
        for i in range(len(corners)):
            if corners[i][0] > width:
                width = corners[i][0]
        return width + 1

    def addWallsToMap(self, state):
        walls = api.walls(state)
        for i in range(len(walls)):
            self.map.setValue(walls[i][0], walls[i][1], '%')

    def updateFoodInMap(self, state):
        # First, make all grid elements that aren't walls blank.
        for i in range(self.map.getWidth()):
            for j in range(self.map.getHeight()):
                if self.map.getValue(i, j) != '%':
                    self.map.setValue(i, j, ' ')
        food = api.food(state)
        for i in range(len(food)):
            self.map.setValue(food[i][0], food[i][1], '*')


    def calculateUtility(self,state):
        #TODO: Find a good discount_factor and maximum_change value
        discount_factor = 0.7
        #probility = 0.8
        maximum_change = 0.1
        new_utility_values = []
        food_reward = 5
        ghost_reward = -100
        #Decide reward
        uti_need_change = True
        while uti_need_change == True:
            new_utility_values = []
            for i in range(self.map.getWidth()):
                for j in range(self.map.getHeight()):
                    #Utility calculation by using value iteration with bellman equation
                    current_utility = self.map.getUtility(i,j)
                    current_reward = -2   #Good!
                    # NOTICE: If food is eaten, the utitlity should be updated

                    if self.map.getValue(i,j) == '*':
                        current_reward = 1


                    #TODO: ADD Ghost State & Scared
                    ghostStates_list = api.ghostStatesWithTimes(state)

                    ghost_list = api.ghosts(state)
                    #print(ghost_list)

                    #Notice: if the ghost is scared, its speed will reduce 
                    #Notice: The time is reduced from 36 to 0
                    if (i,j) in ghost_list:
                        for ghost, time in ghostStates_list:
                            if ghost == (i,j):
                                if time > 6:
                                    current_reward = 0
                                else:
                                    current_reward = ghost_reward
                                break
                        #current_reward = ghost_reward


                    #There is no need to update the utility if it's a wall
                    if self.map.getValue(i,j) != '%':
                        east = (i+1,j)
                        west = (i-1,j)
                        north = (i,j+1)
                        south = (i,j-1)


                        dires = [east,west,north,south]

                        init_index = 0
                        for dire in dires:
                            if self.map.getValue(dire[0], dire[1]) == '%':      
                                dires[init_index] = (i,j)  # The case that hit the wall
                            init_index += 1

                        utilities_list = []

                        current_utilities_list = []

                        for dire in dires:
                            current_utilities_list.append(self.map.getUtility(dire[0],dire[1])) #It stores the effect by applying the action from current state (order: east west north south)

                        #calculate the utilities
                        north_utility = 0.8 * current_utilities_list[2] + 0.1 * current_utilities_list[0] + 0.1 * current_utilities_list[1]
                        utilities_list.append(north_utility)

                        south_utility = 0.8 * current_utilities_list[3] + 0.1 * current_utilities_list[0] + 0.1 * current_utilities_list[1]
                        utilities_list.append(south_utility)

                        west_utility = 0.8 * current_utilities_list[1] + 0.1 * current_utilities_list[2] + 0.1 * current_utilities_list[3]
                        utilities_list.append(west_utility)

                        east_utility = 0.8 * current_utilities_list[0] + 0.1 * current_utilities_list[2] + 0.1 * current_utilities_list[3]
                        utilities_list.append(east_utility)

                        max_utility = max(utilities_list)   #Find the max value of them : It's NP!

                        new_utility = current_reward + discount_factor * max_utility    # Bellman function

                        self.map.setUtility(i,j,new_utility)    #Set the new utility to this location

                        utility_changed = abs(current_utility - new_utility)
                        new_utility_values.append(utility_changed)

            #Faster convergence speed, but precision might be lost
            if max(new_utility_values) < maximum_change:
                uti_need_change = False



    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like the game just ended!"

    def getAction(self, state):
        self.updateFoodInMap(state)
        self.calculateUtility(state)

        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        available_options_utilities = []

        location = api.whereAmI(state)
        location_x = location[0]
        location_y = location[1]

        for option in legal:

            if option == Directions.EAST:
                north_ok = Directions.NORTH in legal
                south_ok  = Directions.SOUTH in legal
                if north_ok and south_ok:
                    east_utility = 0.8 * self.map.getUtility(location_x + 1, location_y) + 0.1 * self.map.getUtility(location_x, location_y+1) + 0.1 * self.map.getUtility(location_x, location_y-1)
                elif north_ok and (not south_ok):
                    east_utility = 0.8 * self.map.getUtility(location_x + 1, location_y) + 0.1 * self.map.getUtility(location_x, location_y+1) + 0.1 * self.map.getUtility(location_x, location_y)
                elif south_ok and (not north_ok):
                    east_utility = 0.8 * self.map.getUtility(location_x + 1, location_y) + 0.1 * self.map.getUtility(location_x, location_y) + 0.1 * self.map.getUtility(location_x, location_y-1)
                else:
                    east_utility = 0.8 * self.map.getUtility(location_x + 1, location_y) + 0.2 * self.map.getUtility(location_x, location_y)
                available_options_utilities.append((east_utility,Directions.EAST))

            elif option == Directions.WEST:
                north_ok = Directions.NORTH in legal
                south_ok  = Directions.SOUTH in legal
                if north_ok and south_ok:
                    west_utility = 0.8 * self.map.getUtility(location_x - 1, location_y) + 0.1 * self.map.getUtility(location_x, location_y+1) + 0.1 * self.map.getUtility(location_x, location_y-1)
                elif north_ok and (not south_ok):
                    west_utility = 0.8 * self.map.getUtility(location_x - 1, location_y) + 0.1 * self.map.getUtility(location_x, location_y+1) + 0.1 * self.map.getUtility(location_x, location_y)
                elif south_ok and (not north_ok):
                    west_utility = 0.8 * self.map.getUtility(location_x - 1, location_y) + 0.1 * self.map.getUtility(location_x, location_y) + 0.1 * self.map.getUtility(location_x, location_y-1)
                else:
                    west_utility = 0.8 * self.map.getUtility(location_x - 1, location_y) + 0.2 * self.map.getUtility(location_x, location_y)
                available_options_utilities.append((west_utility,Directions.WEST))

            elif option == Directions.NORTH:
                east_ok = Directions.EAST in legal
                west_ok  = Directions.WEST in legal
                if east_ok and west_ok:
                    north_utility = 0.8 * self.map.getUtility(location_x, location_y + 1) + 0.1 * self.map.getUtility(location_x + 1, location_y) + 0.1 * self.map.getUtility(location_x - 1, location_y)
                elif east_ok and (not west_ok):
                    north_utility = 0.8 * self.map.getUtility(location_x, location_y + 1) + 0.1 * self.map.getUtility(location_x + 1, location_y) + 0.1 * self.map.getUtility(location_x, location_y)
                elif west_ok and (not east_ok):
                    north_utility = 0.8 * self.map.getUtility(location_x, location_y + 1) + 0.1 * self.map.getUtility(location_x, location_y) + 0.1 * self.map.getUtility(location_x - 1, location_y)
                else:
                    north_utility = 0.8 * self.map.getUtility(location_x, location_y + 1) + 0.2 * self.map.getUtility(location_x, location_y)
                available_options_utilities.append((north_utility,Directions.NORTH))

            elif option == Directions.SOUTH:
                east_ok = Directions.EAST in legal
                west_ok  = Directions.WEST in legal
                if east_ok and west_ok:
                    south_utility = 0.8 * self.map.getUtility(location_x, location_y - 1) + 0.1 * self.map.getUtility(location_x + 1, location_y) + 0.1 * self.map.getUtility(location_x - 1, location_y)
                elif east_ok and (not west_ok):
                    south_utility = 0.8 * self.map.getUtility(location_x, location_y - 1) + 0.1 * self.map.getUtility(location_x + 1, location_y) + 0.1 * self.map.getUtility(location_x, location_y)
                elif west_ok and (not east_ok):
                    south_utility = 0.8 * self.map.getUtility(location_x, location_y - 1) + 0.1 * self.map.getUtility(location_x, location_y) + 0.1 * self.map.getUtility(location_x - 1, location_y)
                else:
                    south_utility = 0.8 * self.map.getUtility(location_x, location_y - 1) + 0.2 * self.map.getUtility(location_x, location_y)
                available_options_utilities.append((south_utility,Directions.SOUTH))


        decision = max(available_options_utilities, key=lambda op: op[0])
        return api.makeMove(decision[1], legal)
