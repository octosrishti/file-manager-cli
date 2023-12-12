COMMAND_WORDS = [
    'mkdir',
    'ls',
    'cd',
    'grep',
    'cat',
    'touch',
    'echo',
    'mv',
    'cp',
    'rm',
    'cwd',
]

COMMAND_VALIDATION = {
    'mkdir':{
        'length': [2]
    },
    'ls':{
        'length' : [1]
    },
    'cd':{
        'length' : [2]
    },
    'grep':{
        'length' : [3,4]
    },
    'cat':{
        'length' : [2]
    },
    'touch':{
        'length' : [2]
    },
    'echo':{
        'length' : [1,2]
    },
    'mv':{
        'length' : [3]
    },
    'cp':{
        'length' : [3]
    },
    'rm':{
        'length' : [2]
    },
    'cwd':{
        'length' : [1]
    }
}