#!/usr/bin/env python
 
from subprocess import Popen, PIPE
from re import split
from sys import stdout
import utils as utils
 
class Proc(object):
    ''' Data structure for a processes . The class properties are
    process attributes '''
    def __init__(self, proc_info):
        self.user = proc_info[0]
        self.pid = proc_info[1]
        self.cpu = proc_info[2]
        self.mem = proc_info[3]
        self.vsz = proc_info[4]
        self.rss = proc_info[5]
        self.tty = proc_info[6]
        self.stat = proc_info[7]
        self.start = proc_info[8]
        self.time = proc_info[9]
        self.cmd = proc_info[10]
 
    def to_str(self):
        ''' Returns a string containing minimalistic info
        about the process : user, pid, and command '''
        return '%s %s %s' % (self.user, self.pid, self.cmd)


def get_proc_list():
    ''' Return a list [] of Proc objects representing the active
    process list list '''
    proc_list = []
    sub_proc = Popen(['ps', 'aux'], shell=False, stdout=PIPE)
    #Discard the first line (ps aux header)
    sub_proc.stdout.readline()
    for line in sub_proc.stdout:
        #The separator for splitting is 'variable number of spaces'
        proc_info = split(" *", line)

        #We only store the s
        aux_process = Proc(proc_info)
        aux_process.cmd = aux_process.cmd.replace("\n","")
        aux_process.cmd = aux_process.cmd.replace(" ","")

        proc_list.append(aux_process)
    return proc_list


if __name__ == "__main__":

    proc_list = get_proc_list()

    #Show the minimal proc list (user, pid, cmd)

    """
    stdout.write('Process list:n')
    for proc in proc_list:
        stdout.write('t' + proc.to_str() + 'n')
 
    #Build &amp; print a list of processes that are owned by root
    #(proc.user == 'root')
    root_proc_list = [ x for x in proc_list if x.user == 'root' ]
    stdout.write('Owned by root:n')
    for proc in root_proc_list:
        stdout.write('t' + proc.to_str() + 'n')

    """

    biggest_size = 0

    for proc in proc_list:
        print proc.pid," ", proc.cmd
        print "Size of String: ", len(proc.cmd)
        if len(proc.cmd) > biggest_size:
            biggest_size = len(proc.cmd)

    print "Number of processess running: ", len(proc_list)
    print "Length of biggest Command String: ", biggest_size

    print utils.stringToBinary("Hello World! How have you been")

