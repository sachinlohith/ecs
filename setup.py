'''
Setup file to run the elevator control system implemented in src
'''

import sys
from src.ecs import step

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: $ python setup.py command_file"
    # pylint: disable=C0103
    file_name = sys.argv[1]
    step(file_name)
