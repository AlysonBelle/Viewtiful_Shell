





from subprocess import Popen, PIPE
import os
from os import listdir


def print_process(output):
    listing = ''
    for o in output:
        listing = listing + o + '\n'
    return listing

def command_error(output):
    print(output, " command not found")
    return None


def find_program(command, my_environ):
    try:
        pathway = os.environ['PATH']
    except KeyError:
        return 'PATH Environment variable not set'
    directories = pathway.split(':')
    for d in directories:
        for f in listdir(d):
            if command == f:
                return (d + '/' + f)
    return command + ' : command not found'


def process(command, my_environ):

    comms = command.split()
    if '/' in comms[0]:
        try:
            p = Popen(comms, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        except FileNotFoundError:
            return (command_error(comms[0]))
        output = p.stdout.read().decode('utf-8').split('\n')
        return (print_process(output))
    path = find_program(comms[0], my_environ)
    if '/' not in path:
        return path
    try:
        if len(comms) > 1:
            p = Popen([path, comms[1:][0]], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        else:
            p = Popen(path, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    except FileNotFoundError:
        return (command_error(comms[0]))
    output = p.stdout.read().decode('utf-8').split('\n')
    return (print_process(output))









