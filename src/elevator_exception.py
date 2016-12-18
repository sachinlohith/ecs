'''
Invalid Elevator Exception
Happens when a elevator going down is tried to update to a floor below or vice versa
'''

class ElevatorException(Exception):
    '''
    Exception to handle invalid elevator conditions

    Attributes:
        message (str)  :    The error message
        errors  (dict) :    Further error messages along with variable that caused it
    '''
    def __init__(self, message, errors=None):
        super(ElevatorException, self).__init__(message)
        self.errors = errors
