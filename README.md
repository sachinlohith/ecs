# Elevator control system

## Build requirements
- `enum34 version 1.1.6` => `$ pip install enum34`
- `heapq_max version 0.21` => `$ pip install heapq_max`

## Build instructions
- Add possible commands to the `commands` file
- Format :
    * start max_elevators
    * status
    * pickup floor_no goal_floor_no
- Example:
   `start 10
    status
    pickup 1 10
    pickup 1 9
    status
    status
    pickup 10 3
    pickup 7 9
    status`
- Run using `$ python setup.py commands`
