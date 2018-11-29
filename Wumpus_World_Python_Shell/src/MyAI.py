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

    def __init__(self):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.current = (1, 1)
        self.last_visited = None
        self.has_arrow = True
        self.wumpus_killed = False
        self.orientation = "right"
        self.visited = dict()
        self.safe = dict()
        self.pits = dict()
        self.wumpus = dict()
        self.moving = (False, None)
        self.xlim = 100000
        self.ylim = 100000
        self.got_gold = False
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction(self, stench, breeze, glitter, bump, scream):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.visited[self.current] = True
        if self.current in self.safe:
            del self.safe[self.current]
        if self.current in self.pits:
            del self.pits[self.current]
        if self.current in self.wumpus:
            del self.wumpus[self.current]

        if self.current == (1, 1) and self.got_gold:
            return Agent.Action.CLIMB
        elif self.got_gold:
            return_coord = self.return_to_start()
            return self.move_to(return_coord)

        if glitter:
            self.got_gold = True
            return Agent.Action.GRAB

        if scream:
            self.wumpus_killed = True

        if self.current == (1, 1) and breeze:
            return Agent.Action.CLIMB
        elif self.current == (1, 1) and stench and not self.wumpus_killed and not self.has_arrow:
            return Agent.Action.CLIMB
        elif self.current == (1, 1) and stench and not self.wumpus_killed:
            self.has_arrow = False
            return Agent.Action.SHOOT

        if bump:
            if self.orientation == "right":
                self.xlim = self.current[0]
                self.current = self.last_visited
                bad_keys = []
                for c in self.safe:
                    if c[0] >= self.xlim:
                        bad_keys.append(c)
                for k in bad_keys:
                    if k in self.safe:
                        del self.safe[k]
                    if k in self.visited:
                        del self.visited[k]
                    if k in self.pits:
                        del self.pits[k]
                    if k in self.wumpus:
                        del self.wumpus[k]
                return self.get_next_move()
            elif self.orientation == "up":
                self.ylim = self.current[1]
                self.current = self.last_visited
                bad_keys = []
                for c in self.safe:
                    if c[1] >= self.ylim:
                        bad_keys.append(c)
                for k in bad_keys:
                    if k in self.safe:
                        del self.safe[k]
                    if k in self.visited:
                        del self.visited[k]
                    if k in self.pits:
                        del self.pits[k]
                    if k in self.wumpus:
                        del self.wumpus[k]
                return self.get_next_move()

        if stench and breeze:
            # Index 0 of danger dictionary = pit, Index 1 is wumpus
            danger_coord = [(self.current[0]+1, self.current[1]), (self.current[0]-1, self.current[1]), (self.current[0], self.current[1]+1), (self.current[0], self.current[1]-1)]
            not_possible = []
            if len(self.wumpus) >= 1:
                for w in self.wumpus:
                    if w not in danger_coord:
                        not_possible.append(w)
                for n in not_possible:
                    del self.wumpus[n]

            if self.wumpus_killed:
                for c in danger_coord:
                    if self.is_valid(c) and c not in self.visited:
                        if c in self.wumpus and c not in self.pits:
                            del self.wumpus[c]
                            self.safe[c] = True
                        else:
                            self.pits[c] = True
                return self.get_next_move()

            elif len(self.wumpus) == 1 and self.has_arrow and not self.wumpus_killed:
                if self.check_orientation(list(self.wumpus.keys())[0]):
                    return Agent.Action.SHOOT
                else:
                    return self.move_to(list(self.wumpus.keys())[0])

            for c in danger_coord:
                if self.is_valid(c) and c not in self.visited:
                    self.pits[c] = True
                    self.wumpus[c] = True
            return self.get_next_move()

        if breeze:
            # Index 0 of danger dictionary = pit, Index 1 is wumpus
            danger_coord = [(self.current[0]+1, self.current[1]), (self.current[0]-1, self.current[1]), (self.current[0], self.current[1]+1), (self.current[0], self.current[1]-1)]
            for c in danger_coord:
                if self.is_valid(c) and c not in self.visited:
                    if c in self.wumpus and c not in self.pits:
                        del self.wumpus[c]
                        self.safe[c] = True
                    else:
                        self.pits[c] = True
            return self.get_next_move()

        if stench:
            # Index 0 of danger dictionary = pit, Index 1 is wumpus
            danger_coord = [(self.current[0]+1, self.current[1]), (self.current[0]-1, self.current[1]), (self.current[0], self.current[1]+1), (self.current[0], self.current[1]-1)]
            not_possible = []
            if len(self.wumpus) >= 1:
                for w in self.wumpus:
                    if w not in danger_coord:
                        not_possible.append(w)
                for n in not_possible:
                    del self.wumpus[n]

            if self.wumpus_killed:
                for c in danger_coord:
                    if self.is_valid(c) and c not in self.visited:
                        self.safe[c] = True
                        if c in self.pits:
                            del self.pits[c]
                        if c in self.wumpus:
                            del self.wumpus[c]
                if len(self.safe) > 0:
                    return self.get_next_move()
                else:
                    self.got_gold = True
                    return self.get_next_move()

            elif len(self.wumpus) == 1 and self.has_arrow and not self.wumpus_killed:
                if self.check_orientation(list(self.wumpus.keys())[0]):
                    self.has_arrow = False
                    return Agent.Action.SHOOT
                else:
                    return self.move_to(list(self.wumpus.keys())[0])

            else:
                for c in danger_coord:
                    if self.is_valid(c) and c not in self.visited:
                        if c in self.pits and c not in self.wumpus:
                            del self.pits[c]
                            self.safe[c] = True
                        else:
                            self.wumpus[c] = True

            return self.get_next_move()

        else:
            safe_coord = [(self.current[0] + 1, self.current[1]), (self.current[0] - 1, self.current[1]),
                            (self.current[0], self.current[1] + 1), (self.current[0], self.current[1] - 1)]
            for c in safe_coord:
                if self.is_valid(c) and c not in self.visited:
                    self.safe[c] = True
                    if c in self.pits:
                        del self.pits[c]
                    if c in self.wumpus:
                        del self.wumpus[c]
            if len(self.safe) > 0:
                return self.get_next_move()
            else:
                self.got_gold = True
                return self.get_next_move()
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def move_to(self, coord):
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
        return self.last_visited

    def check_orientation(self, coord):
        if self.current[0] + 1 == coord[0] and self.orientation == 'right':
            return True
        elif self.current[1] + 1 == coord[1] and self.orientation == 'up':
            return True
        elif self.current[0] - 1 == coord[0] and self.orientation == 'left':
            return True
        elif self.current[1] - 1 == coord[1] and self.orientation == 'down':
            return True
        else:
            return False

    def get_next_move(self):
        if self.moving[0]:
            coord = self.moving[1]
            if self.check_orientation(coord):
                self.moving = (False, None)
                return self.move_to(coord)
            elif self.current == self.moving[1]:
                self.moving = (False, None)
                return self.get_next_move()
            return self.move_to(coord)
        possible_coords = [(self.current[0] + 1, self.current[1]), (self.current[0] - 1, self.current[1]),
                            (self.current[0], self.current[1] + 1), (self.current[0], self.current[1] - 1)]
        for coord in possible_coords:
            if self.is_valid(coord) and coord != self.current and coord in self.safe:
                return self.move_to(coord)
        if len(self.safe) > 0:
            shuffled_list = possible_coords
            random.shuffle(shuffled_list)
            safe_coord = list(self.safe.keys())[0]
            optimal_coord = None
            for i in shuffled_list:
                if self.is_valid(i) and i in self.visited:
                    optimal_coord = i
            for c in shuffled_list:
                if c in self.visited and c != self.last_visited and self.is_valid(c):
                    if abs(safe_coord[0] - c[0]) < abs(safe_coord[0] - optimal_coord[0]):
                        optimal_coord = c
                    elif abs(safe_coord[1] - c[1]) < abs(safe_coord[1] - optimal_coord[1]):
                        optimal_coord = c
            self.moving = (True, optimal_coord)
            return self.move_to(optimal_coord)
        else:
            self.got_gold = True
            return self.move_to(self.return_to_start())
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================

