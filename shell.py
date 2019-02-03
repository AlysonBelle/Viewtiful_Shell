



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


    def change_directory(self, command, my_environ):
        if len(command) == 1:
            os.chdir('/')
        else:
            if command[1] == '~':
                os.chdir(os.my_environ['HOME'])
            else:
                os.chdir(command[1])
        return (switch_paths(my_environ))


    def echo(self, command, my_environ):
        i = 1

        while i < len(command):
            if command[i][0] == '$':
                try:
                    print(my_environ[command[i][1:]], end=' ')
                except KeyError:
                    print('Error : variable not found', end='')
           else:
                print(command[i], end=' ')
            i += 1
        print('\n', end='')        


    def print_env(self, command, my_environ):
        for key, val in my_environ.items():
            print(key,'=',val);


    def set_env(self, command, my_environ):
        if len(command) != 3:
            print('Usage : setenv [VARIABLE] [VALUE]')
        else:
            my_environ[command[1]] = command[2]
        return my_environ


    def unset_env(self, command, my_environ):
        if len(command) != 2:
            print('Usage: unsetenv [VARIABLE]')
        else:
            try:
                del my_environ[command[1]]
            except KeyError:
                print('Error : variable not found')
        return my_environ






def parse(command, ShellCommands, my_environ):
    comm_args = command.split()
    
    if comm_args[0] == 'cd':
        my_environ = ShellCommands.change_directory(comm_args, my_environ)
    elif comm_args[0] == 'echo':
        ShellCommands.echo(comm_args, my_environ)
    elif comm_args[0] == 'env':
        ShellCommands.print_env(comm_args, my_environ)
    elif comm_args[0] == 'setenv':
        my_environ = ShellCommands.set_env(comm_args, my_environ)
    elif comm_args[0] == 'unsetenv':
        my_environ = ShellCommands.unset_env(comm_args, my_environ)
    else:
        process(command, my_environ)


def viewtiful(my_environ):
    ShellCommand = Commands()

    while True:
       command = input("$>")
       command = command.rstrip().lstrip()
       if len(command) == 0:
           continue
       else:
           parse(command, ShellCommand, my_environ)



def main():
    my_environ = os.environ.copy()
    my_environ['SHELL'] = os.getcwd() + '/viewtiful.py'
    my_environ['SHLVL'] = str(int(my_environ['SHLVL']) + 1)
    viewtiful(my_environ)

main()
