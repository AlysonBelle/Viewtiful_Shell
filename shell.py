



from run_subprocess import process
from subprocess import Popen, PIPE
import os



class Commands():

    def __init__(self):
        pass

    def switch_paths(self, my_environ):
        old_pwd = my_environ['PWD']
        my_environ['PWD'] = os.getcwd()
        my_environ['OLDPWD'] = old_pwd
        return my_environ


    def is_file_or_directory_error(self, filename):
        error_msg = 'cd : Not a Directory' if os.path.isfile(filename) else 'cd : Directory not found'
        return error_msg

    def change_directory(self, command, my_environ):
        error_msg = ''

        if len(command) == 1:
            os.chdir('/')
        else:
            if command[1] == '~':
                os.chdir(my_environ['HOME'])
                error_msg = my_environ['HOME']
            elif command[1] == '-':
                os.chdir(my_environ['OLDPWD'])
                error_msg = my_environ['OLDPWD']
            else:
                try:
                    os.chdir(command[1])
                except (FileNotFoundError, NotADirectoryError):
                    error_msg = self.is_file_or_directory_error(command[1])
        return (self.switch_paths(my_environ)), error_msg


    def echo(self, command, my_environ):
        i = 1

        while i < len(command):
            if command[i][0] == '$':
                try:
                    print(my_environ[command[i][1:]], end=' ')
                    return (my_environ[command[i][1:]] + '\n')
                except KeyError:
                    print('Error : variable not found', end='')
                    return ("Error : variable not found\n")
            else:
                print(command[i], end=' ')
                return ('')
            i += 1
        print('\n', end='')        


    def print_env(self, command, my_environ):
        env = ''
        for key, val in my_environ.items():
            val = key +'='+val;
            env = env + val + '\n'
        return (env)


    def set_env(self, command, my_environ):
        error_msg = ''
        if len(command) != 3:
            error_msg = "Usage : setenv [VARIABLE] [VALUE]"
            print('Usage : setenv [VARIABLE] [VALUE]')
        else:
            my_environ[command[1]] = command[2]
        return my_environ, error_msg


    def unset_env(self, command, my_environ):
        error_msg = ''
        if len(command) != 2:
            error_msg = "Usage: unsetenv [VARIABLE]"
            print('Usage: unsetenv [VARIABLE]')
        else:
            try:
                del my_environ[command[1]]
            except KeyError:
                error_msg = "Error : variable not found"
                print('Error : variable not found')
        return my_environ, error_msg






def parse(command, ShellCommands, my_environ):
    comm_args = command.split()
    output = ''
    
    if comm_args[0] == 'cd':
        my_environ, output = ShellCommands.change_directory(comm_args, my_environ)
    elif comm_args[0] == 'echo':
        output = ShellCommands.echo(comm_args, my_environ)
    elif comm_args[0] == 'env':
        output = ShellCommands.print_env(comm_args, my_environ)
    elif comm_args[0] == 'setenv':
        my_environ, output = ShellCommands.set_env(comm_args, my_environ)
    elif comm_args[0] == 'unsetenv':
        my_environ, output  = ShellCommands.unset_env(comm_args, my_environ)
    else:
        output = process(command, my_environ)
    print('output is ', output)
    return output, my_environ


def viewtiful(my_environ, ShellCommand):
    while True:
       command = input("$>")
       command = command.rstrip().lstrip()
       if len(command) == 0:
           continue
       else:
           parse(command, ShellCommand, my_environ)



def init_shell():
    my_environ = os.environ.copy()
    my_environ['SHELL'] = os.getcwd() + '/viewtiful.py'
    my_environ['SHLVL'] = str(int(my_environ['SHLVL']) + 1)
    ShellCommand = Commands()
    return my_environ, ShellCommand
    #viewtiful(my_environ, ShellCommand)

