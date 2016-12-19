# Elevator control system

The design of the system is split among two classes - `Elevator` and `ECS (Elevator Control System)`. The `Elevator` class models each elevator and `ECS` class models the system as a whole. APIs are exposed by the `ECS` class and clients interact with the system through those APIs.

The crux of the design is in the `Scheduling Algorithm` in `ECS` class where new pickup requests are assigned to nearest elevators. The destination floors are assigned to min heap in case the elevator is going UP and are assigned to a max heap in case the elevators are going DOWN.

This system does not work in an FCFS schedule. It assigns the elevator that is closest to the requested pickup floor.

A pickup request consists of two integers - `floor` and `destination floor`. Direction is not required as the system deduces this automatically through the request.

## Interface

The interface is modified from the actual specification. The `update` method has been removed as clients should not be handed control over modification of the elevator statuses. The rest of the methods are the same.

```python
def status(self):
    # Returns a list of 3-tuple status for each elevator

def pickup(self, floor_no, goal_floor_no):
    # Issue a pickup request from a floor_no to a goal_floor_no

def step(ecs):
    # Simulate the functioning of ecs based on the command file
```
## Build requirements
- `enum34 version 1.1.6` => `$ pip install enum34`
- `heapq_max version 0.21` => `$ pip install heapq_max`

## Build instructions
* Add possible commands to the `commands` file
* Format :
    * start max_elevators
    * status
    * pickup floor_no goal_floor_no
* Example
```
start 10
status
pickup 1 10
step
step
pickup 2 10
step
step
step
step
step
step
pickup 10 5
step
pickup 8 5
step
step
step
step
pickup 7 10
step
step
step
step
step
status
pickup 6 10
step
step
step
step
step
step
step
step
pickup 1 10
status
```

* Run through `$ python setup.py commands`

## Drawbacks
- The elevator control system does not consider the capacity of the elevator when processing a new pickup request.
- Theoritically, there is a possibility of starvation in the system. To see this, consider a building with one elevator and infinite floors. The first person that gets in, goes up and the elevator keeps getting a pickup request for further up top. In such a case, a request from a lower floor will be waiting in the system's queue and will never be assigned to an elevator.
- Dynamic reconfiguration of elevators and the pickup queue. Suppose an elevator is not considered as nearest at some point for a certain pickup request at that point in time. Since it's moving, a few seconds later it's nearer than the one that was scheduled for the pickup of that request.
