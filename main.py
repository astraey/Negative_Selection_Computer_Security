#!/usr/bin/env python
 
from subprocess import Popen, PIPE
from re import split
from sys import stdout
import utils as utils
from Tkinter import Tk, Label, Button
from gui import SystemGUI

from process import Proc



proc_list = utils.get_proc_list()

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

processListString = []

for proc in proc_list:
    """
    print proc.pid," ", proc.cmd
    print "Size of String: ", len(proc.cmd)
    if len(proc.cmd) > biggest_size:
        biggest_size = len(proc.cmd)
    """
    #print utils.stringToBinary(proc.cmd)
    processListString.append(proc.cmd)


#print "Number of processess running: ", len(proc_list)
#print "Length of biggest Command String: ", biggest_size

#print utils.stringToBinary("Hello World! How have you been")

#print processListString



#print processListString
#print len(processListString)


#print "*******************************"
processListString = utils.listStringsToBinary(processListString)

#print "*******************************"

processListString = utils.reduceStringList(processListString)

#print processListString

processListString = utils.normaliseLengthStrings(processListString)

#print len(processListString)

#returnValue = utils.chunkMatchesSelf(['011', 1], 3, ['00001','01111','01000'])
#print returnValue

#returnValue = utils.newChunkMatchesSelf('01100',['00001','01111','01000'])
#print returnValue

#selfSet = ['00001','01111','01000']

selfSet = processListString

detectorChunksList = []

detectorChunksList = utils.chunkGenerator(selfSet)

#utils.chunkMatchesSelf("0u1u",["0011","1011"])
