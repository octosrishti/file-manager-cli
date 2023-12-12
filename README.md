# In Memory File System CLI

## Software Information

This software is build using python(3.10) version and is a in-memory file system cli, that has the following features:
- **_Note - 1_**: all path name supports absolute paths ('~', '/') as well as relative paths ('../', './').
- **_Note - 2_**: all path name and command do not support inverted commas and must be written directly.
1. Excute the following commands:

    ```
        1. mkdir <dir_name> : this command creates a directory with given path name.

        2. ls : this command lists all the files/directory present in current working directory.

        3. cd <dir_name> : this command changes directory to dir_name.

        4. grep <pattern> <file_name>: this command searches and prints pattern in the given file.

        5. cat <file_name>: this command prints the content of the file given.

        6. touch <file_name>: this command creates an empty file with the given file name.

        7. echo <text> / echo <text> > <file_name>: this command either prints the text in terminal or writes/appends the text in the given file.

        8. mv <file_name>/<dir_name> <dest_name> : this command moves a file or directory to given destination directory.

        9. cp <file_name>/<dir_name> <dest_file_name>/<dest_dir_name>: this command copies a file or directory to given file path or directory location.

        10. rm <file_name>/<dir_name> : this command removes the existing file or directory.

        11. cwd : this command is an extra feature provides current working directory,
    ```

2. Given the initial argument {'state':true, file_name:file_name} this saves the command to valid file.

- **_Note_**: grep command has been implemeted such that it can print entire line where the pattern is present, can be changed to just print pattern too.

## Features and Functionalities

1. All commands are in-memory, use with care when using file operations 😉.
2. All commands are optimal, example read and write files have been implemented such that large files can be handled with buffer read and write.
3. The save state functionality has been implemented that saves all the commands and reloads them as passed in argument
4. Save state is optimal as it save only the recent program to file not the entire commands

## Setup

- ### Local setup

1. Install Python3 from microsoft store for windows or follow steps from : https://www.python.org/downloads/

2. Clone the repository

```
    git clone <repository_clone_link>
```

3. Execute the command 

```
    pipenv shell
    python script.py {'state': True, 'path': <'file_name'>}
```

- ### Docker setup

1. Clone the repository and change directory to repository

```
    git clone <repository_clone_link>
    cd <repo_name>
```

2. Create an Image for the container using the Dockerfile

```
    docker build -t file-system-cli .
```

3. Run the container

```
    docker run -d file-system-cli
```

4. Get inside the container

```
    docker ps | grep <container_name> (copy the container id)
    docke exec -it <container_id> bash
```

5. Start the script

```
    python script.py {'state': False, 'path': <'file_name'>}
```