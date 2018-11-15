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
import queue
import random

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.current = (1, 1)
        self.last_visited = None
        self.orientation = "right"
        self.visited = dict()
        self.safe = dict()
        self.danger = dict()
        self.queue = queue.Queue()
        self.xlim = 100000
        self.ylim = 100000
        self.got_gold = False
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        print("Safe coords:", self.safe)
        print("Danger coords:", self.danger)
        print("Visited coords:", self.visited)
        print("Current:", self.current)
        print("Last visited:",self.last_visited)
        print("Xlim:", self.xlim)
        print("Ylim:", self.ylim)

        self.visited[self.current] = True
        if self.current in self.safe:
            del self.safe[self.current]
        if self.current in self.danger:
            del self.danger[self.current]


        self.queue = queue.Queue()
        for i in self.safe.keys():
            self.queue.put(i)
        for i in self.visited.keys():
            self.queue.put(i)


        if self.current == (1,1) and self.got_gold:
            return Agent.Action.CLIMB
        elif self.got_gold:
            return_coord = self.return_to_start()
            return self.moveTo(return_coord)

        if glitter:
            self.got_gold = True
            return Agent.Action.GRAB

        if self.current == (1,1) and (stench or breeze):
            return Agent.Action.CLIMB


        if bump:
            if self.orientation == "right":
                self.xlim = self.current[0]
                self.current = self.last_visited
                self.orientation = "up"
                bad_keys = []
                for c in self.safe:
                    if c[0] > self.xlim:
                        bad_keys.append(c)
                for k in bad_keys:
                    del self.safe[k]
                    del self.visited[k]
                return Agent.Action.TURN_LEFT
            elif self.orientation == "up":
                self.ylim = self.current[1]
                self.current = self.last_visited
                self.orientation = "left"
                bad_keys = []
                for c in self.safe:
                    if c[1] > self.ylim:
                        bad_keys.append(c)
                for k in bad_keys:
                    del self.safe[k]
                    del self.visited[k]
                return Agent.Action.TURN_LEFT

        if stench and breeze:
            #Index 0 of danger dictionary = pit, Index 1 is wumpus
            danger_coord = [(self.current[0]+1, self.current[1]), (self.current[0]-1, self.current[1]), (self.current[0], self.current[1]+1), (self.current[0], self.current[1]-1)]
            for c in danger_coord:
                if self.is_valid(c) and c not in self.visited:
                    self.danger[c] = (True, True)
            while not self.queue.empty():
                coord = self.queue.get()
                if self.is_valid(coord) and coord != self.current:
                    return self.moveTo(coord)
            return self.moveTo(self.last_visited)


        if breeze:
            #Index 0 of danger dictionary = pit, Index 1 is wumpus
            danger_coord = [(self.current[0]+1, self.current[1]), (self.current[0]-1, self.current[1]), (self.current[0], self.current[1]+1), (self.current[0], self.current[1]-1)]
            for c in danger_coord:
                if self.is_valid(c) and c not in self.visited:
                    if c in self.danger and self.danger[c][0] == False:
                        del self.danger[c]
                        self.safe[c] = True
                    else:
                        self.danger[c] = (True, False)
            while not self.queue.empty():
                coord = self.queue.get()
                if self.is_valid(coord) and coord != self.current:
                    return self.moveTo(coord)
            return self.moveTo(self.last_visited)

        if stench:
            #Index 0 of danger dictionary = pit, Index 1 is wumpus
            danger_coord = [(self.current[0]+1, self.current[1]), (self.current[0]-1, self.current[1]), (self.current[0], self.current[1]+1), (self.current[0], self.current[1]-1)]
            for c in danger_coord:
                if self.is_valid(c) and c not in self.visited:
                    if c in self.danger and self.danger[c][1] == False:
                        del self.danger[c]
                        self.safe[c] = True
                    else:
                        self.danger[c] = (False, True)
            while not self.queue.empty():
                coord = self.queue.get()
                if self.is_valid(coord) and coord != self.current:
                    return self.moveTo(coord)
            return self.moveTo(self.last_visited)

        else:
            safe_coord = [(self.current[0] + 1, self.current[1]), (self.current[0] - 1, self.current[1]),
                            (self.current[0], self.current[1] + 1), (self.current[0], self.current[1] - 1)]
            for c in safe_coord:
                if self.is_valid(c) and c not in self.visited:
                    self.safe[c] = True
                    self.queue.put(c)
                    if c in self.danger:
                        del self.danger[c]
            if len(self.safe) > 0:
                while not self.queue.empty():
                    coord = self.queue.get()
                    if self.is_valid(coord) and coord != self.last_visited:
                        return self.moveTo(coord)
                return self.moveTo(self.return_to_start())
            else:
                self.got_gold = True
                return Agent.Action.CLIMB
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

    def is_in_bounds(self, coord):
        if coord[0] >= self.xlim or coord[1] >= self.ylim:
            return False
        elif coord[0] <= 0 or coord[1] <= 0:
            return False
        return True

    def is_valid(self, coord):
        if self.is_in_bounds(coord):
            if (coord[0] == self.current[0] + 1 or coord[0] == self.current[0] - 1) and coord[1] == self.current[1]:
                return True
            elif (coord[1] == self.current[1] + 1 or coord[1] == self.current[1] - 1) and coord[0] == self.current[0]:
                return True
            else:
                return False
        else:
            return False

    def return_to_start(self):
        for coord in self.visited:
            if self.current[0] - 1 == coord[0] and self.current[1] == coord[1]:
                del self.visited[self.current]
                return coord
            elif self.current[0] == coord[0] and self.current[1] - 1 == coord[1]:
                del self.visited[self.current]
                return coord



    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================

