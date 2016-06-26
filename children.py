#!/usr/bin/python

# Python 2.6 :c 

# TODO
# - Print a regular ps -c listing recursively given a process or from the current process
# - Print a terse tree structure of processes
# - Print a terse tree structure with memory usage 
# - Enable some form of useful debugging

import argparse, sys, re
from pykdump.API import *


def main():

    pid = 0

    args = setup_argparse()
    if args.debug:

    pid = get_pid(args)

    print_children(pid)

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

def print_children(pid):
    hierarchy = build_hierarchy(pid)
    for entry in hierarchy:
        print entry


# Helper functions
def set_trace():
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
    return parser.parse_args()


main()
