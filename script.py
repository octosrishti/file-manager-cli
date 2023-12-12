import time
import sys
import json
from custom_exceptions.SystemExceptions import FileExceptions, DirectoryExceptions
from custom_exceptions.CommandExceptions import CommandExceptions
from utility.Command import CommandClass

def parse_args(args):
    parsed_argument = eval(args.replace("'", "\""))
    return (parsed_argument.get("state"), parsed_argument.get("path"))
    

if __name__ == "__main__":
    state, file_path = parse_args(sys.argv[1])
    command_utility = CommandClass(load_state=state, load_file=file_path)
    
    while True:
        print("> ", end=' ')
        command = input()
        command_list = command.split(' ')
        
        if command == "exit":
            command_utility.save_command_file()
            exit(0)
        
        try:
            command_utility.execute_command(command)
            if command_utility.load_state:
                command_utility.append_command(command=command_list[0], args=' '.join(command_list[1:]), state=True)
        except FileExceptions as e:
            if command_utility.load_state:
                command_utility.append_command(command=command_list[0], args=' '.join(command_list[1:]), state=False)
            print(e.message)
        except DirectoryExceptions as e:
            if command_utility.load_state:
                command_utility.append_command(command=command_list[0], args=' '.join(command_list[1:]), state=False)
            print(e.message)
        except CommandExceptions as e:
            if command_utility.load_state:
                command_utility.append_command(command=command_list[0], args=' '.join(command_list[1:]), state=False)
            print(e.message)
        except Exception as e:
            if command_utility.load_state:
                command_utility.append_command(command=command_list[0], args=' '.join(command_list[1:]), state=False)
            print(str(e))
        
        
        