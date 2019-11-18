# mapAgents.py
# parsons/11-nov-2017
#
# Version 1.0
#
# A simple map-building to work with the PacMan AI projects from:
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

# The agent here is an extension of the above code written by Simon
# Parsons, based on the code in pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util
import sys

#
# A class that creates a grid that can be used as a map
#
# The map itself is implemented as a nested list, and the interface
# allows it to be accessed by specifying x, y locations.
#
class Grid:

    # Constructor
    #
    # Note that it creates variables:
    #
    # grid:   an array that has one position for each element in the grid.
    # width:  the width of the grid
    # height: the height of the grid
    #
    # Grid elements are not restricted, so you can place whatever you
    # like at each location. You just have to be careful how you
    # handle the elements when you use them.
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


    # Print the grid out.
    def display(self):
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print self.grid[i][j],
            # A new line after each line of the grid
            print
        # A line after the grid
        print

    # The display function prints the grid out upside down. This
    # prints the grid out so that it matches the view we see when we
    # look at Pacman.
    def prettyDisplay(self):
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print self.grid[self.height - (i + 1)][j],
            # A new line after each line of the grid
            print
        # A line after the grid
        print
    # Set and get the values of specific elements in the grid.
    # Here x and y are indices.
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


#
# An agent that creates a map.
#
# As currently implemented, the map places a % for each section of
# wall, a * where there is food, and a space character otherwise. That
# makes the display look nice. Other values will probably work better
# for decision making.
#
class SimpleMDPAgent(Agent):

    # The constructor. We don't use this to create the map because it
    # doesn't have access to state information.
    def __init__(self):
        print "Running init!"

    # This function is run when the agent is created, and it has access
    # to state information, so we use it to build a map for the agent.
    def registerInitialState(self, state):
         print "Running registerInitialState!"
         # Make a map of the right size
         self.makeMap(state)
         self.addWallsToMap(state)
         self.updateFoodInMap(state)
         self.map.display()
         self.calculateUtility(state)

    # This is what gets run when the game ends.

    # Make a map by creating a grid of the right size
    def makeMap(self,state):
        corners = api.corners(state)
        print corners
        height = self.getLayoutHeight(corners)
        width  = self.getLayoutWidth(corners)
        self.map = Grid(width, height)

    # Functions to get the height and the width of the grid.
    #
    # We add one to the value returned by corners to switch from the
    # index (returned by corners) to the size of the grid (that damn
    # "start counting at zero" thing again).
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

    # Functions to manipulate the map.
    #
    # Put every element in the list of wall elements into the map
    def addWallsToMap(self, state):
        walls = api.walls(state)
        for i in range(len(walls)):
            self.map.setValue(walls[i][0], walls[i][1], '%')

    # Create a map with a current picture of the food that exists.
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
        discount_factor = 0.6
        #probility = 0.8
        maximum_change = 1
        new_utility_values = []
        food_reward = 5
        ghost_reward = -100
        #Decide reward
        uti_need_change = True
        while uti_need_change == True:
            new_utility_values = []
            for i in range(self.map.getWidth()):
                for j in range(self.map.getHeight()):
                    #Calculation
                    current_utility = self.map.getUtility(i,j)
                    current_reward = -2   #Good!
                    #current_max = -999
                    # NOTIutility_changedCE: If food is eaten, the utitlity should be updated

                    if self.map.getValue(i,j) == '*':
                        current_reward = 1


                    #TODO: ADD Ghost State & Scared
                    #ghostStates_list = api.ghostStates(state)

                    ghost_list = api.ghosts(state)
                    #print(ghost_list)
                    if (i,j) in ghost_list:
                        #print("haha")

                        current_reward = ghost_reward


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
                            current_utilities_list.append(self.map.getUtility(dire[0],dire[1]))

                        #calculate the utilities
                        north_utility = 0.8 * current_utilities_list[2] + 0.1 * current_utilities_list[0] + 0.1 * current_utilities_list[1]
                        utilities_list.append(north_utility)

                        south_utility = 0.8 * current_utilities_list[3] + 0.1 * current_utilities_list[0] + 0.1 * current_utilities_list[1]
                        utilities_list.append(south_utility)

                        west_utility = 0.8 * current_utilities_list[1] + 0.1 * current_utilities_list[2] + 0.1 * current_utilities_list[3]
                        utilities_list.append(west_utility)

                        east_utility = 0.8 * current_utilities_list[0] + 0.1 * current_utilities_list[2] + 0.1 * current_utilities_list[3]
                        utilities_list.append(east_utility)

                        max_utility = max(utilities_list)

                        new_utility = current_reward + discount_factor * max_utility

                        self.map.setUtility(i,j,new_utility)

                        utility_changed = abs(current_utility - new_utility)
                        new_utility_values.append(utility_changed)

            if max(new_utility_values) < maximum_change:
                uti_need_change = False














    # For now I just move randomly, but I display the map to show my progress
    def getAction(self, state):
        self.updateFoodInMap(state)
        #self.map.prettyDisplay()
        self.calculateUtility(state)

        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.

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
