class FileExceptions(Exception):
    
    """
        Custom file exceptions class inheriting from Exception class. This class handles all exception related to file
    """
    
    def __init__(self, message="Error while handling file"):
        self.message = message
        super().__init__(self.message)

class DirectoryExceptions(Exception):
    """
        Custom directory exceptions class inheriting from Exception class. This class handles all exception related to directory
    """
    
    
    def __init__(self, message="Error while handling directory path"):
        self.message = message
        super().__init__(self.message)