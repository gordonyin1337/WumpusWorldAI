# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.current = (1, 1)
        self.last_visited = None
        self.orientation = "right"
        self.visited = dict()
        self.visited[self.current] = 1
        self.safe = dict()
        self.danger = dict()
        self.xlim = 100000
        self.ylim = 100000
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        print("Current: ", self.current)
        print("Just Visited: ", self.last_visited)
        print(self.visited)
        self.visited[self.last_visited] = 1
        if self.current == (1, 1):
            coord = (self.current[0] + 1, self.current[1])
            return self.moveTo(coord)
        if bump:
            if self.orientation == "right":
                self.xlim = self.current[0]
            elif self.orientation == "up":
                self.ylim = self.current[1]
        if breeze:
            pass
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def moveTo(self, coord):
        if coord[0] == 1 + self.current[0]:
            return self.move_right(coord)
        elif coord[1] == 1 + self.current[1]:
            return self.move_up(coord)
        elif coord[0] == self.current[0] - 1:
            return self.move_left(coord)
        elif coord[1] == self.current[1] - 1:
            return self.move_down(coord)

    def move_right(self, coord):
        if self.orientation == "right":
            self.last_visited = self.current
            self.current = coord
            return Agent.Action.FORWARD
        elif self.orientation == "up":
            self.orientation = "right"
            return Agent.Action.TURN_RIGHT
        elif self.orientation == "down":
            self.orientation = "right"
            return Agent.Action.TURN_LEFT
        elif self.orientation == "left":
            self.orientation = "down"
            return Agent.Action.TURN_LEFT

    def move_up(self, coord):
        if self.orientation == "up":
            self.last_visited = self.current
            self.current = coord
            return Agent.Action.FORWARD
        elif self.orientation == "left":
            self.orientation = "up"
            return Agent.Action.TURN_RIGHT
        elif self.orientation == "right":
            self.orientation = "up"
            return Agent.Action.TURN_LEFT
        elif self.orientation == "down":
            self.orientation = "right"
            return Agent.Action.TURN_LEFT

    def move_left(self, coord):
        if self.orientation == "left":
            self.last_visited = self.current
            self.current = coord
            return Agent.Action.FORWARD
        elif self.orientation == "up":
            self.orientation = "left"
            return Agent.Action.TURN_LEFT
        elif self.orientation == "down":
            self.orientation = "left"
            return Agent.Action.TURN_RIGHT
        elif self.orientation == "right":
            self.orientation = "up"
            return Agent.Action.TURN_LEFT

    def move_down(self, coord):
        if self.orientation == "down":
            self.last_visited = self.current
            self.current = coord
            return Agent.Action.FORWARD
        elif self.orientation == "right":
            self.orientation = "down"
            return Agent.Action.TURN_RIGHT
        elif self.orientation == "left":
            self.orientation = "down"
            return Agent.Action.TURN_LEFT
        elif self.orientation == "up":
            self.orientation = "left"
            return Agent.Action.TURN_LEFT
    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================

