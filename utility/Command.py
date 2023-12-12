import os
import json
from constants.CommandConstant import COMMAND_WORDS, COMMAND_VALIDATION
from custom_exceptions.SystemExceptions import FileExceptions, DirectoryExceptions
from custom_exceptions.CommandExceptions import CommandExceptions
from utility.FileIO import FileInputOutputUtility

class CommandClass():
    
    """
        class to execute all the commands using FileInputOutputUtility class, this also handle all file path handling. 
    """
    
    def __init__(self, load_state=False, load_file=None):
        self.current_dir = os.getcwd()
        self.load_state = load_state
        self.load_file = self.__get_absolute_load_file(load_file)
        self.commands = []
        self.recent_commands = []
        self.current_commad_position = 0
        
        if self.load_state:
            self.__load_file_commands()
        
    def __get_absolute_load_file(self, load_file_path):
        absolute_path, file_name = self.__get_absolute_path_and_filename(load_file_path)
        return os.path.join(absolute_path, file_name)
    
    def __load_file_commands(self):
        if not os.path.exists(self.load_file):
            print("command file does not exists, creating a new file...")
            
            with open(self.load_file, 'w') as f:
                pass
        print("----> loading commands")
        
        with open(self.load_file, 'r') as file:
            commands = file.read()
            if commands:
                try:
                    commands_list = json.loads(commands)
                    self.commands = commands_list
                    self.current_commad_position = len(commands_list)
                except Exception as e:
                    raise FileExceptions("Failed to load commands")
                
    def append_command(self, command, state, args):
        self.commands.append({"state": state, "args": args, "command": command})
        self.recent_commands.append({"state": state, "args": args, "command": command})
    
    def save_command_file(self):
        try:
            print("-----> saving recent commands to file")
            with open(self.load_file, 'a') as f:
                command_string = json.dumps(self.recent_commands)
                f.write(command_string)
        except Exception as e:
            raise FileExceptions("Failed to save recent commands to list")
        
    @staticmethod
    def __validate_dir_exists(dir_name):
        if not os.path.exists(dir_name):
            raise DirectoryExceptions("Directory does not exist")
    
    def __get_current_dir(self):
        return self.current_dir
    
    def __change_current_dir(self, dir):
        self.__validate_dir_exists(dir)
        self.current_dir = dir
    
    def __parse_command(self, command):
        return command.split(' ')
    
    @staticmethod
    def __validate_command(command_list:list):
        if len(command_list) == 0:
            pass
        
        command = command_list[0]
        
        if command not in COMMAND_WORDS:
            raise CommandExceptions("Command not found")
        elif not len(command_list) in COMMAND_VALIDATION.get(command).get("length"):
            raise CommandExceptions("Invalid Parameters")
        
        return True

    def __get_absolute_path(self, dir:str=None):
        
        if not dir:
            return self.current_dir
        
        if dir.startswith("../") or dir.startswith('..'):
            current_parent_dir = os.path.dirname(self.current_dir)
            return os.path.join(current_parent_dir, '/'.join(dir.split('/')[1:]))
        elif dir.startswith("./"):
            return os.path.join(self.current_dir, '/'.join(dir.split('/')[1:]))
        elif dir.startswith("~") or dir.startswith('/'):
            return os.path.join(os.path.expanduser('~'), '/'.join(dir.split('/')[1:]))
        else:
            return os.path.join(self.current_dir, dir)
    
    def __get_absolute_path_and_filename(self, dir:str=None):
        
        if not dir:
            return self.current_dir
        
        if dir.startswith("../") or dir.startswith('..'):
            current_parent_dir = os.path.dirname(self.current_dir)
            return (os.path.join(current_parent_dir, '/'.join(dir.split('/')[1:-1])), dir.split('/')[-1])
        elif dir.startswith("./"):
            return (os.path.join(self.current_dir, '/'.join(dir.split('/')[1:-1])), dir.split('/')[-1])
        elif dir.startswith("~") or dir.startswith('/'):
            return (os.path.join(os.path.expanduser('~'), '/'.join(dir.split('/')[2:-1])), dir.split('/')[-1])
        else:
            return (os.path.join(self.current_dir, '/'.join(dir.split('/')[:-1])), dir.split('/')[-1])
    
    def __is_file(self, dir:str):
        return True if dir.split('/')[-1].count('.') > 0 else False
            
    def execute_command(self, command):
        command_list = self.__parse_command(command)
        
        self.__validate_command(command_list)
        
        command = command_list[0]
        
        if command == 'mkdir':
            absolute_file_path = self.__get_absolute_path(command_list[1])
            file_utility = FileInputOutputUtility(file_absolute_dir=absolute_file_path)
            file_utility.create_directory()
        
        elif command == 'cwd':
            print(self.__get_current_dir())
            
        elif command == 'ls':
            absolute_file_path = self.__get_absolute_path()
            file_utility = FileInputOutputUtility(file_absolute_dir=absolute_file_path)
            file_utility.list_directory()
            
        elif command == 'cd':
            absolute_file_path = self.__get_absolute_path(command_list[1])
            self.__change_current_dir(absolute_file_path)
            
        elif command == 'grep':
            absolute_file_path, file_name = self.__get_absolute_path_and_filename(command_list[2])
            file_utility = FileInputOutputUtility(file_name=file_name,file_absolute_dir=absolute_file_path)
            file_utility.read_from_file(pattern=command_list[1])
            
        elif command == 'cat':
            
            absolute_file_path, file_name = self.__get_absolute_path_and_filename(command_list[1])
            file_utility = FileInputOutputUtility(file_name=file_name,file_absolute_dir=absolute_file_path)
            file_utility.read_from_file()
            
        elif command == 'touch':
            
            absolute_file_path, file_name = self.__get_absolute_path_and_filename(command_list[1])
            file_utility = FileInputOutputUtility(file_name=file_name,file_absolute_dir=absolute_file_path)
            file_utility.create_file()
            
        elif command == 'echo':
            if len(command_list) > 1:
                absolute_file_path, file_name = self.__get_absolute_path_and_filename(command_list[3])
                file_utility = FileInputOutputUtility(file_name=file_name,file_absolute_dir=absolute_file_path)
                file_utility.write_to_file(command_list[1])
            else:
                print(command_list[1])
            
        elif command == 'mv':
            absolute_dest_path = self.__get_absolute_path(command_list[2])
            dest_file_name = None
            if self.__is_file(command_list[1]):
                absolute_file_path, file_name = self.__get_absolute_path_and_filename(command_list[1])
                file_utility = FileInputOutputUtility(file_name=file_name,file_absolute_dir=absolute_file_path, destination_file_dir=absolute_dest_path)
                file_utility.move_file()
            else:
                absolute_file_path = self.__get_absolute_path(command_list[1])
                file_utility = FileInputOutputUtility(file_absolute_dir=absolute_file_path, destination_file_dir=absolute_dest_path)
                file_utility.move_directory()
                
        elif command == 'cp':
            dest_file_name = None
            if self.__is_file(command_list[1]):
                absolute_file_path, file_name = self.__get_absolute_path_and_filename(command_list[1])
            else:
                absolute_file_path= self.__get_absolute_path(command_list[1])
            if self.__is_file(command_list[2]):
                absolute_dest_path, dest_file_name = self.__get_absolute_path_and_filename(command_list[2])
            else:
                absolute_dest_path = self.__get_absolute_path(command_list[2])
                
            if self.__is_file(command_list[1]):
                file_utility = FileInputOutputUtility(file_name=file_name,file_absolute_dir=absolute_file_path, destination_file_name=dest_file_name, destination_file_dir=absolute_dest_path)
                file_utility.copy_file()
            else:
                file_utility = FileInputOutputUtility(file_absolute_dir=absolute_file_path)
                file_utility.copy_directory()
                
        elif command == 'rm':
            if self.__is_file(command_list[1]):
                absolute_file_path, file_name = self.__get_absolute_path_and_filename(command_list[1])
                file_utility = FileInputOutputUtility(file_name=file_name,file_absolute_dir=absolute_file_path)
                file_utility.remove_file()
            else:
                absolute_file_path = self.__get_absolute_path(command_list[1])
                file_utility = FileInputOutputUtility(file_absolute_dir=absolute_file_path)
                file_utility.remove_directory()
           
    