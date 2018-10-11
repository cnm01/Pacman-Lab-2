# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
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

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class RandomishAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
         self.last = Directions.STOP

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.last = pick
            return api.makeMove(pick, legal)

# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)

        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)

        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)


# GoWestAgent
#
# Always goes west when it is possible, if not possible, randomly go north or south
class GoWestAgent(Agent):

        def getAction(self,state):
            legal = api.legalActions(state)
            if not Directions.WEST in legal:
                if Directions.EAST in legal:
                    legal.remove(Directions.EAST)
                return api.makeMove(random.choice(legal), legal)
            return api.makeMove(Directions.WEST, legal)




# CornerSeekingAgent
#
# Finds out the coordinates of the corners of the world
# Remembers the path it has taken, using constructor to initialise field variables
# Eats all food on map without ghosts

class CornerSeekingAgent(Agent):

        def __init__(self):
             self.visited = []
             self.last = Directions.STOP

        def getAction(self,state):

            legalMoves = state.getLegalPacmanActions()
            currentDirection = state.getPacmanState().configuration.direction

            #if all outermost walls already explored, go towards food if it can be seen...
            if len(legalMoves) > 3 and api.whereAmI(state) in self.visited:

                return self.foodWithin5(state, currentDirection, legalMoves)

            #always go left to visit outermost walls
            else:
                self.visited.append(api.whereAmI(state))

                if currentDirection == Directions.STOP:
                    currentDirection = Directions.NORTH
                if Directions.LEFT[currentDirection] in legalMoves:
                    self.last = Directions.LEFT[currentDirection]
                    return self.last
                if currentDirection in legalMoves:
                    self.last = currentDirection
                    return self.last
                if Directions.RIGHT[currentDirection] in legalMoves:
                    self.last = Directions.RIGHT[currentDirection]
                    return self.last
                if Directions.LEFT[Directions.LEFT[currentDirection]] in legalMoves:
                    self.last = Directions.LEFT[Directions.LEFT[currentDirection]]
                    return self.last
                return Directions.STOP



        def foodWithin2(self, state, currentDirection, legalMoves):
            cur = api.whereAmI(state)

            #north
            ##can see food within 2 units
            if (cur[0], cur[1]+1) in api.food(state) or (cur[0], cur[1]+2) in api.food(state):
                print "n"
                return Directions.NORTH
            #east
            ##can see food within 2 units
            if (cur[0]+1, cur[1]) in api.food(state) or (cur[0]+2, cur[1]) in api.food(state):
                print "e"
                return Directions.EAST
            #south
            ##can see food within 2 units
            if (cur[0], cur[1]-1) in api.food(state) or (cur[0], cur[1]-2) in api.food(state):
                print "s"
                return Directions.SOUTH
            #west
            ##can see food within 2 units
            if (cur[0]-1, cur[1]) in api.food(state) or (cur[0]+2, cur[1]) in api.food(state):
                print "w"
                return Directions.WEST


            legalMoves.remove(Directions.STOP)
            return random.choice(legalMoves)

        #if pacman can see food 5 units or closer to current
        # position, that isnt blocked by a wall, go towards it
        def foodWithin5(self, state, currentDirection, legalMoves):
            cur = api.whereAmI(state)

            for x in range(1, 6):
                #north
                ##can see food within 5 units north of current pos, not blocked by wall
                if (cur[0], cur[1]+x) in api.food(state):
                    noWall = True
                    for y in range(cur[1], cur[1]+x+1):
                        #if wall is detected between food and pacman
                        if (cur[0], y) in api.walls(state):
                            noWall = False
                    if noWall:
                        print "Food seen ", x, " north"
                        last = Directions.NORTH
                        return Directions.NORTH
                #east
                ##can see food within 5 units east of current pos, not blocked by wall
                if (cur[0]+x, cur[1]) in api.food(state):
                    noWall = True
                    for y in range(cur[0], cur[0]+x+1):
                        if (y, cur[1]) in api.walls(state):
                            noWall = False
                    if noWall:
                        print "Food seen ", x, " east"
                        last = Directions.EAST
                        return Directions.EAST
                #south
                ##can see food within 5 units south of current pos, not blocked by wall
                if (cur[0], cur[1]-x) in api.food(state):
                    noWall = True
                    for y in range(cur[1]-x, cur[1]+1):
                        if (cur[0], y) in api.walls(state):
                            noWall = False
                    if noWall:
                        print "Food seen ", x, " south"
                        last = Directions.SOUTH
                        return Directions.SOUTH
                #west
                ##can see food within 5 units west of current pos, not blocked by wall
                if (cur[0]-x, cur[1]) in api.food(state):
                    noWall = True
                    for y in range(cur[0]-x, cur[0]+1):
                        if (y, cur[1]) in api.walls(state):
                            noWall = False
                    if noWall:
                        print "Food seen ", x, " west"
                        last = Directions.WEST
                        return Directions.WEST


            #if at a intersection continue going straight
            # 1/2 probability of going stright, 1/2 probability of random choice
            if self.last in legalMoves:
                print "Probably going straight/ maybe random choice"
                legalMoves.remove(Directions.STOP)
                legalMoves.remove(self.last)
                choices = [self.last, random.choice(legalMoves)]
                self.last = random.choice(choices)
                return self.last

            #go random direction at intersection
            legalMoves.remove(Directions.STOP)
            print "Making random choice"
            self.last = random.choice(legalMoves)
            return self.last

































#
