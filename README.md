# Elevator control system

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

   > start 10
   
   > status
   
   > pickup 1 10
   
   > pickup 1 9
   
   > status
   
   > status
   
   > pickup 10 3
   
   > pickup 7 9
   
   > status

* Run through `$ python setup.py commands`

## Drawbacks
- The elevator control system does not consider the capacity of the elevator when processing a new pickup request.
- Theoritically, there is a possibility of starvation in the system. To see this, consider a building with one elevator and infinite floors. The first person that gets in, goes up and the elevator keeps getting a pickup request for further up top. In such a case, a request from a lower floor will be waiting in the system's queue and will never be assigned to an elevator.
