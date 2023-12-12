import os
import shutil
import re
from custom_exceptions.SystemExceptions import FileExceptions, DirectoryExceptions

class FileInputOutputUtility():
    
    """
        class to execute all the commands involving the file system. 
    """
    
    
    def __init__(self, file_name=None, file_absolute_dir=None, destination_file_name=None, destination_file_dir=None):
        self.file_name = file_name
        self.file_absolute_dir = file_absolute_dir
        self.destination_file_name = destination_file_name
        self.destination_file_dir = destination_file_dir
       
    @staticmethod 
    def __validate_file(file_name, file_absolute_dir, should_exist=False) -> str:
        if file_name is None:
            raise FileExceptions("File name is invalid")
        elif file_absolute_dir is None:
            raise DirectoryExceptions("Directory path is invalid")
        file_absolute_path = os.path.join(file_absolute_dir, file_name)
        
        if not should_exist and os.path.exists(file_absolute_path):
            raise FileExceptions("File already exists")
        if should_exist and not os.path.exists(file_absolute_path):
            raise FileExceptions("File does not exists")
        
        return file_absolute_path
    
    @staticmethod
    def __validate_dir_exists(dir_name):
        if not os.path.exists(dir_name):
            raise DirectoryExceptions("Directory does not exist")
        
    @staticmethod
    def __validate_dir_does_not_exist(dir_name):
        if os.path.exists(dir_name):
            raise DirectoryExceptions("Directory already exists")
    
    def write_to_file(self, file_content:str):
        write_mode = 'w'
        try:
            file_absolute_path = self.__validate_file(self.file_name, self.file_absolute_dir, should_exist=True)
        except FileExceptions as e:
            if e.message == "File already exists":
                write_mode = 'a'
        
        with open(file_absolute_path, write_mode) as file:
            file.writelines(file_content)
            
    def __read_file_as_buffer(self, file_absolute_path):
        with open(file_absolute_path, 'r') as file:
            while True:
                line = file.read(1024)
                
                if not line:
                    break
                print(line)
    
    def __read_file_as_line(self, file_absolute_path, pattern):
        with open(file_absolute_path, 'r') as file:
            while True:
                line = file.readline()
                
                if not line:
                    break
                if re.search(pattern, line, re.DOTALL):
                    print(line, end='')
            
        
    def read_from_file(self, pattern=None):
        
        try:
            file_absolute_path = self.__validate_file(self.file_name, self.file_absolute_dir, should_exist=True)
            with open(file_absolute_path, 'r') as file:
                
                if pattern:
                    self.__read_file_as_line(file_absolute_path, pattern)
                else:
                    self.__read_file_as_buffer(file_absolute_path)
        except FileExceptions as e:
            print("Error while reading file", e.message)
    
    def create_file(self):
        file_absolute_path = self.__validate_file(self.file_name, self.file_absolute_dir, should_exist=False)
        self.__validate_dir_exists(self.file_absolute_dir)
        
        with open(file_absolute_path, 'w'):
            pass
        
        print(f"{self.file_name} created succcessfully in location {self.file_absolute_dir}")            
    
    def copy_file(self):
        self.__validate_dir_exists(self.destination_file_dir)
        file_absolute_path = self.__validate_file(self.file_name, self.file_absolute_dir, should_exist=True)
        self.__validate_dir_exists(self.file_absolute_dir)
        if self.destination_file_name:
            destination_file_absolute_path =  self.__validate_file(self.destination_file_name, self.destination_file_dir, should_exist=False)
            shutil.copy(file_absolute_path, destination_file_absolute_path)
        else:
            shutil.copy(file_absolute_path, self.destination_file_dir)
        
        
        print(f"{self.file_name} copied to destination {self.destination_file_dir}")
        
    def move_file(self):
        file_absolute_path = self.__validate_file(self.file_name, self.file_absolute_dir, should_exist=True)
        self.__validate_dir_exists(self.file_absolute_dir)
        self.__validate_dir_exists(self.destination_file_dir)
        
        shutil.move(file_absolute_path, self.destination_file_dir)
        
        print(f"moved file with absolute path {file_absolute_path} to {self.destination_file_dir}")
        
    def remove_file(self):
        file_absolute_path = self.__validate_file(self.file_name, self.file_absolute_dir, should_exist=True)
        os.remove(file_absolute_path)
    
    def list_directory(self):
        
        self.__validate_dir_exists(self.file_absolute_dir)
        
        for dir_name in os.listdir(self.file_absolute_dir):
            print(dir_name)
        
    def create_directory(self):
        self.__validate_dir_does_not_exist(self.file_absolute_dir)
        os.makedirs(self.file_absolute_dir)
        
        print(f"created directory with absolute path {self.file_absolute_dir}")
    
    def copy_directory(self):
        self.__validate_dir_exists(self.file_absolute_dir)
        self.__validate_dir_does_not_exist(self.destination_file_dir)
        
        shutil.copytree(self.file_absolute_dir, self.destination_file_dir)
        
        print(f"copied directory with absolute path {self.file_absolute_dir} to {self.destination_file_dir}")
    
    def move_directory(self):
        self.__validate_dir_exists(self.file_absolute_dir)
        self.__validate_dir_exists(self.destination_file_dir)
        shutil.move(self.file_absolute_dir, self.destination_file_dir)
        
        print(f"moved directory with absolute path {self.file_absolute_dir} to {self.destination_file_dir}")
        
    def remove_directory(self):
        self.__validate_dir_exists(self.file_absolute_dir)
        
        shutil.rmtree(self.file_absolute_dir)
        
        print(f"removed directory {self.file_absolute_dir}")
    