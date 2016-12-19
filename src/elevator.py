'''
Module implementing a standard elevator class
'''

import heapq
import heapq_max
from src.elevator_exception import ElevatorException
from enum import Enum

DIRECTION = Enum('Direction', 'UP DOWN HOLD')
OCCUPIED = Enum('Occupied', 'YES NO')

class Elevator(object):
    '''
    A standard elevator

    Attributes:
        elevator_id    : id, ranges from 1 to 16 inclusive
        Direction      : direction of moving elevator
        Occupied       : state of occupancy
        floor_no       : current floor number
        goal_floor_nos : floor numbers it's heading towards
    '''

    def __init__(self, elevator_id):
        '''
        Create an elevator object
        '''

        self.elevator_id = elevator_id

        # Elevator is not occupied when created
        self.occupied = OCCUPIED.NO

        # Elevator is on HOLD
        self.direction = DIRECTION.HOLD

        # start with floor_no 1
        self.floor_no = 1
        self.goal_floor_nos = []

    def set_goal_floor(self, goal_floor_no):
        # pylint: disable=R0912
        '''
        Update the floor to which elevator must get in the list of goal floors

        Args:
            goal_floor_no (int): The floor the elevator must get to
        '''

        if self.direction == DIRECTION.HOLD:
            assert self.occupied == OCCUPIED.NO
            assert len(self.goal_floor_nos) == 0
            # Already reached destination floor
            if self.floor_no == goal_floor_no:
                pass
            else:
                if goal_floor_no not in self.goal_floor_nos:
                    self.goal_floor_nos += [goal_floor_no]
                    if goal_floor_no > self.floor_no:
                        # Elevator going up
                        self.direction = DIRECTION.UP
                        self.occupied = OCCUPIED.YES
                        heapq.heapify(self.goal_floor_nos)
                    else:
                        # Elevator going down
                        self.direction = DIRECTION.DOWN
                        self.occupied = OCCUPIED.YES
                        heapq_max.heapify_max(self.goal_floor_nos)
        elif self.direction == DIRECTION.UP and self.floor_no < goal_floor_no:
            # If the elevator is not headed to the goal floor already
            if goal_floor_no not in self.goal_floor_nos:
                # Min heap for retreiving earliest floor first while going UP
                heapq.heappush(self.goal_floor_nos, goal_floor_no)
        elif self.direction == DIRECTION.DOWN and self.floor_no > goal_floor_no:
            # If the elevator is not headed to the goal floor already
            if goal_floor_no not in self.goal_floor_nos:
                # Max heap for retrieving earliest floor first while going DOWN
                heapq_max.heappush_max(self.goal_floor_nos, goal_floor_no)
        elif self.floor_no == goal_floor_no:
            pass
        else:
            print str(self.get_state()) + str(self.direction)
            raise ElevatorException("Invalid Goal Floor number requested.")
    # pylint: disable=R0912

    def update_floor(self):
        '''
        Update the current floor of an elevator
        '''

        # Idle elevator, nothing to do
        if self.direction == DIRECTION.HOLD:
            pass
        elif self.direction == DIRECTION.UP:
            self.floor_no += 1
            if self.floor_no == self.goal_floor_nos[0]:
                # reached the first goal floor
                heapq.heappop(self.goal_floor_nos)
                if len(self.goal_floor_nos) == 0:
                    # the elevator has reached the final destination
                    self.direction = DIRECTION.HOLD
                    self.occupied = OCCUPIED.NO
        elif self.direction == DIRECTION.DOWN:
            self.floor_no -= 1
            if self.floor_no == self.goal_floor_nos[0]:
                # reached the first goal floor
                heapq_max.heappop_max(self.goal_floor_nos)
                if len(self.goal_floor_nos) == 0:
                    # the elevator has reached the final destination
                    self.direction = DIRECTION.HOLD
                    self.occupied = OCCUPIED.NO
        else:
            raise ElevatorException("Invalid direction of elevators detected")

    def get_state(self):
        '''
        Function to identify the state of an elevator

        Returns:
            (int, int, int) : elevator_id, floor_no, goal_floor_nos
        '''

        return (self.elevator_id, self.floor_no, self.goal_floor_nos)

    def get_direction(self):
        '''
        Function to identify the direction elevator is headed

        Returns:
            direction : DIRECTION.UP or DIRECTION.DOWN or DIRECTION.UP
        '''

        return self.direction
