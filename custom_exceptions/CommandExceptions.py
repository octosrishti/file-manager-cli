class CommandExceptions(Exception):
    """
        Custom command exceptions class inheriting from Exception class. This class handles all exception related to commands
    """
    
    def __init__(self, message="Error executing command"):
        self.message = message
        super().__init__(self.message)
