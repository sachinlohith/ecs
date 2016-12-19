'''
An elevator control system implemented in Python
Version 1.0, uses nearest elevator first algorithm
'''

import time
from src.elevator import Elevator, DIRECTION
from src.elevator_exception import ElevatorException

class ECS(object):
    '''
    An elevator control system
    Can be used to:
        * issue pickup requests
        * query the status of elevators
        * time step the simulation
        * update the current floors of elevators
            similar to moving a second forward in the real world
            assuming elevators move at the rate of 1 floor / second

    Attributes:
        elevators       Elevators numbering from 1 .. 16
        pickup_queue    Queue logging pickup requests as they are requested
        max_elevators   Maximum number of elevators present in the system
    '''
    def __init__(self, max_elevators=1):
        self.elevators = [None]
        self.pickup_queue = []
        self.max_elevators = max_elevators
        try:
            for _ in xrange(1, max_elevators+1):
                self.elevators.append(Elevator(_))
        except Exception:
            raise ElevatorException("Invalid elevator id specified")

    def status(self):
        '''
        Get the status of all the elevators

        Returns:
            [(int, int, int)] : [(elevator_id, floor_no, goal_floor_nos) ... ]
        '''
        _status = []
        for elevator in self.elevators[1:]:
            _status.append(elevator.get_state())

        return _status

    def update_elevators(self):
        '''
        Move the elevators one floor at a time
        '''
        for elevator in self.elevators[1:]:
            elevator.update_floor()
        return self._schedule()


    def pickup(self, floor_no, goal_floor_no):
        '''
        Issue a pickup request from a floor_no to a goal_floor_no

        Args:
            floor_no (int)      : current floor number of user
            goal_floor_no (int) : floor the user must get to
        '''
        self.pickup_queue.append((floor_no, goal_floor_no))
        if self._schedule():
            return True

    def _schedule(self):
        # pylint: disable=R0912
        '''
        Scheduling algorithm for the elevators

        Searches for the nearest elevators first
        '''
        _status = self.status()
        _scheduled_requests = []
        print "Pickup Queue: ",
        for request in self.pickup_queue:
            print request,
            floor_no, goal_floor_no = request
            # User wants to go down
            if goal_floor_no < floor_no:
                # Go over the states of elevators and pick the nearest one
                # that is going down
                _downward_elevators = [
                    (_elevator[0], _elevator[1])
                    for _elevator in _status
                    if self.elevators[_elevator[0]].get_direction() == DIRECTION.DOWN
                    or self.elevators[_elevator[0]].get_direction() == DIRECTION.HOLD
                ]
                _downward_elevators = [(_elevator[0], abs(floor_no - _elevator[1]))
                                       for _elevator in _downward_elevators]
                while _downward_elevators != [] :
                    _nearest_elevator = min(_downward_elevators, key=lambda x: x[1])
                    _downward_elevators.pop(_downward_elevators.index(_nearest_elevator))
                    _nearest_elevator = _nearest_elevator[0]
                    if self.elevators[_nearest_elevator].floor_no >= floor_no:
                        self.elevators[_nearest_elevator].set_goal_floor(floor_no)
                        # If an elevator residing at a lower floor must come up first
                        # to the requested pickup floor and then move up to the goal floor
                        # ==> add the request again so the request can be served after
                        # the elevator has reached the request floor
                        if self.elevators[_nearest_elevator].direction == DIRECTION.UP:
                            self.pickup_queue.append((floor_no, goal_floor_no))
                        else:
                            self.elevators[_nearest_elevator].set_goal_floor(goal_floor_no)
                        _scheduled_requests.append(request)
                        break
            elif goal_floor_no > floor_no:
                # User wants to go up
                _upward_elevators = [
                    (_elevator[0], _elevator[1])
                    for _elevator in _status
                    if self.elevators[_elevator[0]].get_direction() == DIRECTION.UP
                    or self.elevators[_elevator[0]].get_direction() == DIRECTION.HOLD
                ]
                _upward_elevators = [(_elevator[0], abs(floor_no - _elevator[1]))
                                     for _elevator in _upward_elevators
                                    ]
                while _upward_elevators != []:
                    _nearest_elevator = min(_upward_elevators, key=lambda x: x[1])
                    _upward_elevators.pop(_upward_elevators.index(_nearest_elevator))
                    _nearest_elevator = _nearest_elevator[0]
                    if self.elevators[_nearest_elevator].floor_no <= floor_no:
                        self.elevators[_nearest_elevator].set_goal_floor(floor_no)
                        # If an elevator residing at a higher floor must come down first
                        # to the requested pickup floor and then move up to the goal floor
                        # ==> add the request again so the request can be served after
                        # the elevator has reached the request floor
                        if self.elevators[_nearest_elevator].direction == DIRECTION.DOWN:
                            self.pickup_queue.append((floor_no, goal_floor_no))
                        else:
                            self.elevators[_nearest_elevator].set_goal_floor(goal_floor_no)
                        _scheduled_requests.append(request)
                        break
            else:
                # User is trying to get to the floor he's already in
                _scheduled_requests.append(request)
        # Remove scheduled requests from request queue
        print ""
        if _scheduled_requests != []:
            self._remove_scheduled_requests(_scheduled_requests)
            return True

    def _remove_scheduled_requests(self, _scheduled_requests):
        '''
        Remove all scheduled requests from the pickup queue

        Args:
            _scheduled_requests : all scheduled requests as (floor_no,
                                  goal_floor_no)
        '''
        self.pickup_queue = list(set(self.pickup_queue)^set(_scheduled_requests))


def print_elevators(ecs):
    '''
    Pretty printer for elevator states

    Args:
        ecs : Elevator control system to be printed
    '''
    # Only prints elevators that are not on hold
    status = ecs.status()
    print '-'*100
    print '|'
    for elevator in status:
        if ecs.elevators[elevator[0]].get_direction() != DIRECTION.HOLD:
            print "{0} : {1} {2} {3}".format(elevator[0], elevator[1],
                                             ecs.elevators[elevator[0]]
                                             .get_direction(),
                                             str(elevator[2]))
            print '|'
    print '-'*100
    # pylint: disable=R0912

def step(file_name):
    '''
    Time stepping the simulation commands described in a text file

    Format for commands in the text file :
        * start max_elevators
        * status
        * pickup floor_no goal_floor_no
        * step

    The command file should begin with the start command specified the
    maximum number of elevators that should be created

    The commands should not contain any other characters other than the ones
    specified above before or after the command

    max_elevators, floor_no, goal_floor_no are all integers

    The step command moves the elevator system one second into the future

    The simulation ends once end of file is reached

    Example:
        start 10
        status
        pickup 1 10
        step
        step
        step
        step
        step
        step
        step
        pickup 1 9
        step
        status
        pickup 10 3
        step
        step
        step
        step
        pickup 7 9
        step
        step
        step
        step
        step
        status

    Args:
        file_name : file name containing the list of commands to be executed
    '''
    import re
    # Possible commands
    start_command = re.compile(r'^start\s\d+$')
    status_command = re.compile(r'^status$')
    pickup_command = re.compile(r'^pickup\s\d+\s\d+$')
    step_command = re.compile(r'^step$')
    try:
        with open(file_name, 'r') as filep:
            commands = filep.readlines()
        command = commands[0]
        command = command.strip()

        # Ensure command file starts with `start` command
        if not start_command.match(command):
            raise IOError("Invalid command file")
        else:
            max_elevators = int(command.split()[1])

        # Ensure number of elevators are within the system limit
        assert max_elevators <= 16 and max_elevators >= 1
        # create the elevator control system
        ecs = ECS(max_elevators)
        print_elevators(ecs)
        for command in commands[1:]:
            print command
            command = command.strip()
            if status_command.match(command):
                print_elevators(ecs)
            elif pickup_command.match(command):
                floor_no, goal_floor_no = map(int, command.split()[1:])
                assert floor_no >= 1 and goal_floor_no >= 1
                # Add the request to the pickup queue and process
                ecs.pickup(floor_no, goal_floor_no)
                print_elevators(ecs)
            elif step_command.match(command):
                ecs.update_elevators()
                print_elevators(ecs)
                time.sleep(1)
            else:
                raise IOError("Invalid command file")
        while ecs.update_elevators():
            print_elevators(ecs)
            time.sleep(1)

    except ElevatorException as error:
        print error
    except IOError as error:
        print error
    except ValueError as error:
        print error
    except AssertionError as error:
        print error
