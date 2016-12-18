'''
An elevator control system implemented in Python
Version 1.0, uses nearest elevator first algorithm
'''

from enum import Enum

class Elevator(Object):
    '''
    A standard elevator

    Attributes:
        elevator_id     id, ranges from 1 to 16 inclusive
        Direction       direction of moving elevator
        Occupied        state of occupancy
        floor_no        current floor number
        goal_floor_no   floor number it's heading towards
    '''
    elevator_id, floor_no, goal_floor_no
    Direction = Enum('Direction', 'UP DOWN NONE')
    Occupied = Enum('Occupied', 'YES NO')

    def __init__(self, elevator_id):
        '''
        Create an elevator object
        '''
        # Check if the elevator_id complies with limits
        assert isinstance(elevator_id, int)
        assert elevator_id <= 16 and elevator_id >= 1
        self.elevator_id = elevator_id

        # Elevator is not occupied when created
        self.Occupied = Occupied.NO

        # start with floor_no and goal_floor_no as 1
        self.floor_no = 1
        self.goal_floor_no = 1


'''
Elevator control system has the following variables :
    Elevators - numbering upto 16
    Pickup queue - request for pickup is recorded in this queue
and methods :
    status() -> [(ID, floor_number, (goal_floor_number/s)] -> returns the current status of each elevator
    update(ID, floor_number, (goal_floor_number/s)) -> updates the status of an elevator specified by the ID
    pickup(floor_number, direction) -> allows the user to add himself to the pickup queue
    step() -> time stepping the simulation
'''
class Elevator_Control_System(Object):
    elevators = None
    pickup_queue = []

