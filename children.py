#!/usr/bin/python

# Python 2.6 :c 

# TODO
# - Print a regular ps -c listing recursively given a process or from the current process
# - Print a terse tree structure of processes
# - Print a terse tree structure with memory usage 
# - Enable some form of useful debugging
# - Docstrings (how do for pykdump?)
import argparse, sys, re
from pykdump.API import *


def main():

    pid = 0

    args = setup_argparse()
    #if args.debug:

    pid = get_pid(args)
    # Can't operate on swapper
    if pid == 0:
        print '\nCurrently set or provided PID is 0. Please indicate a non-swapper PID.\n'
        return

    hierarchy = build_hierarchy(pid)
    
    print_children(hierarchy, args.tree)
    if args.count:
        print '\n' + hierarchy[0][1]
        print 'Total children (threads and processes): ' + str(len(hierarchy) - 1)
        

def build_hierarchy(pid):
    hierarchy = []
    return __rec_build_hierarchy(hierarchy, 0, pid)

def __rec_build_hierarchy(hierarchy, level, pid):
    processes = exec_crash_command('ps -c ' + str(pid)).strip().split('\n')
    hierarchy.append((level, processes.pop(0)))

    # swapper is a child unto itself and init somehow. 
    # Step over it when seen to avoid recursion looping
    while 'swapper' in processes[0]: processes.pop(0)

    if 'no children' in processes[0]:
        return hierarchy
    for proc in processes:
        next_pid = [int(s) for s in proc.split() if s.isdigit()][0]
        __rec_build_hierarchy(hierarchy, level+1, next_pid)
    return hierarchy

def print_children(hierarchy, tree):
    pre_str = ''
    proc_str = ''
    for i in range(len(hierarchy)):
        proc = hierarchy[i]

        # Just do a basic ps -c like printing if no tree printing
        if not tree:
           pre_str = '  ' * proc[0]
           proc_str = proc[1]
           print pre_str + proc_str
           continue

        #if i == 0:
        #    print proc 
        #if i == len(hierarchy) - 1:
        #    pre_string 
        #print pre_string + proc
        pre_string = ''
        proc_str = ''


# Helper functions
#def set_trace():
    # figure this out

def get_pid(args):
    # If we were passed the pid manually
    if args.pid:
        set_trace()
        pid = args.pid

    # If we were not passed the pid
    else:
        kernel_set = exec_crash_command('set').split("\n")
        if any("PID" in s for s in kernel_set):
            pid_str = [s for s in kernel_set if "PID" in s][0] 
            pid = [int(s) for s in pid_str.split() if s.isdigit()][0]

    return pid



def setup_argparse():
    parser = argparse.ArgumentParser(description='Crash ps data but with recursive features.')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug execution.')
    parser.add_argument('-p', '--pid', type=int, help='Optional, prints all children and child threads of PID. When omitted, uses the set PID.')
    parser.add_argument('-c', '--count', action='store_true', help='Count child processes/threads')
    parser.add_argument('-t', '--tree', action='store_true', help='Print output in pstree-like format. This option is ignored when "-q|--quiet" is used as well.')
    parser.add_argument('-q', '--quiet', action='store_true', help='Run without printing the children hierarchy. Other options will still print however (for example, -c will still print the count of children).')
    return parser.parse_args()


main()
