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

        def getAction(self,state):
            # print api.whereAmI(state)
            # print state.getLegalPacmanActions()

            #always go left if possible to visit outer wall
            if api.whereAmI(state) not in self.visited:
                self.visited.append(api.whereAmI(state))
                #print self.visited
                legal = state.getLegalPacmanActions()
                current = state.getPacmanState().configuration.direction
                if current == Directions.STOP:
                    current = Directions.NORTH
                left = Directions.LEFT[current]
                if left in legal:
                    return left
                if current in legal:
                    return current
                if Directions.RIGHT[current] in legal:
                    return Directions.RIGHT[current]
                if Directions.LEFT[left] in legal:
                    return Directions.LEFT[left]
                return Directions.STOP

            else:
                #if square already visited, only go to one that hasnt been visited on next move
                if api.whereAmI(state) not in self.visited:
                    self.visited.append(api.whereAmI(state))

                #print self.visited
                legalMoves = state.getLegalPacmanActions()
                currentDirection = state.getPacmanState().configuration.direction
                if currentDirection == Directions.STOP:
                    currentDirection = Directions.NORTH

                #go left if possible
                if Directions.LEFT[currentDirection] in legalMoves and self.nextCoord(legalMoves, api.whereAmI(state), currentDirection) not in self.visited:
                    return Directions.LEFT[currentDirection]
                #go straight if cant go left
                if currentDirection in legalMoves and self.nextCoord(legalMoves, api.whereAmI(state), currentDirection) not in self.visited:
                    return currentDirection
                #go right if cant go straight
                if Directions.RIGHT[currentDirection] in legalMoves and self.nextCoord(legalMoves, api.whereAmI(state), currentDirection) not in self.visited:
                    return Directions.RIGHT[currentDirection]
                #go back if cant go right
                if Directions.LEFT[Directions.LEFT[currentDirection]] in legalMoves and self.nextCoord(legalMoves, api.whereAmI(state), currentDirection) not in self.visited:
                    return Directions.LEFT[left]

                #if no choice but to visit previously visited square, go left as usual
                if currentDirection == Directions.STOP:
                    currentDirection = Directions.NORTH
                left = Directions.LEFT[currentDirection]
                if left in legalMoves:
                    return left
                if currentDirection in legalMoves:
                    return currentDirection
                if Directions.RIGHT[currentDirection] in legalMoves:
                    return Directions.RIGHT[currentDirection]
                if Directions.LEFT[left] in legalMoves:
                    return Directions.LEFT[left]
                return Directions.STOP


        #find coord of next move
        def nextCoord(self, legalMoves, currentCoord, currentDirection):

            #go left if possible
            if Directions.LEFT[currentDirection] in legalMoves:
                #if currentDirection is north; x-1
                if currentDirection == Directions.NORTH:
                    nextCoord = (currentCoord[0]-1, currentCoord[1])
                elif currentDirection == Directions.EAST:
                    #if currentD is east; y+1
                    nextCoord = (currentCoord[0], currentCoord[1]+1)
                elif currentDirection == Directions.SOUTH:
                    #if currentD is south; x+1
                    nextCoord = (currentCoord[0]+1, currentCoord[1])
                elif currentDirection == Directions.WEST:
                    #if currentD is west; y-1
                    nextCoord = (currentCoord[0], currentCoord[1]-1)

                return nextCoord

            #go straight if cant go left
            if currentDirection in legalMoves:
                #if currentDirection is north; y+1
                if currentDirection == Directions.NORTH:
                    nextCoord = (currentCoord[0], currentCoord[1]+1)
                elif currentDirection == Directions.EAST:
                #if currentD is east; x+1
                    nextCoord = (currentCoord[0]+1, currentCoord[1])
                elif currentDirection == Directions.SOUTH:
                    #if currentD is south; y-1
                    nextCoord = (currentCoord[0], currentCoord[1]-1)
                elif currentDirection == Directions.WEST:
                    #if currentD is west; x-1
                    nextCoord = (currentCoord[0]-1, currentCoord[1])

                return nextCoord

            #go right if cant go straight
            if Directions.RIGHT[currentDirection] in legalMoves:
                #if currentDirection is north; x+1
                if currentDirection == Directions.NORTH:
                    nextCoord = (currentCoord[0]+1, currentCoord[1])
                elif currentDirection == Directions.EAST:
                    #if currentD is east; y-1
                    nextCoord = (currentCoord[0], currentCoord[1]-1)
                elif currentDirection == Directions.SOUTH:
                    #if currentD is south; x-1
                    nextCoord = (currentCoord[0]-1, currentCoord[1])
                elif currentDirection == Directions.WEST:
                    #if currentD is west; y+1
                    nextCoord = (currentCoord[0], currentCoord[1]+1)

                return nextCoord

            #go back if cant go right
            if Directions.LEFT[left] in legalMoves:
                #if currentDirection is north; y-1
                if currentDirection == Directions.NORTH:
                    nextCoord = (currentCoord[0], currentCoord[1]-1)
                elif currentDirection == Directions.EAST:
                    #if currentD is east; x-1
                    nextCoord = (currentCoord[0]-1, currentCoord[1])
                elif currentDirection == Directions.SOUTH:
                    #if currentD is south; y+1
                    nextCoord = (currentCoord[0], currentCoord[1]+1)
                elif currentDirection == Directions.WEST:
                    #if currentD is west; x+1
                    nextCoord = (currentCoord[0]+1, currentCoord[1])

                return nextCoord




























#
