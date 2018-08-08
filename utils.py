
import random
import string
from subprocess import Popen, PIPE
from gui import SystemGUI
from Tkinter import Tk, Label, Button
from re import split
from process import Proc
import os.path

import binascii

import pickle

maxSelfBinaryStringSize = 138

"""
root = Tk()
my_gui = SystemGUI(root)
#root.mainloop()
root.update_idletasks()
root.update()
"""




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

def stringToBinary(string): 
    
    return ''.join(format(ord(x), 'b') for x in string)

def listStringsToBinary(listStrings):

    newListStrings = []

    for string in listStrings:

        newListStrings.append(stringToBinary(string))

    return newListStrings

#Should be applied before the strings are converted to binary
def reduceStringList(listStrings):

    newListStrings = []

    for string in listStrings:
        newListStrings.append(string[len(string)-maxSelfBinaryStringSize:len(string)])

    return newListStrings



#This funcion returns a list with all the chunks detectors for the given self. This is where the magic happens
def chunkGenerator(S, my_gui, root):

    if S:

        detectorChunksList = []

        sizeSelf = len(S)
        sizeStringsSelf = len(S[0])

        #print "Chunk Generator Initiated"

        #print "Self:", S


        #We use the length of self to get an idea of the initial random chunks that we want to generate, but this value can  be modified.
        while not sizeSelf == len(detectorChunksList):
        #for i in range(sizeSelf):
            #We can't append them directly, we have to check wether it matches Self or not, and also change it to the minimal form patern.
            #We also need to delete repeated members of the list, as in the new form they will most likely be repeated.

            randomBinaryString = generateRandomBinaryString(sizeStringsSelf)

            #print "Randomly Generated String: ",randomBinaryString


            #Here we should check if this matches the list.

            #Do the whole replacing here.

            """For replacing a character in a String: 
            text = 'abcdefg'
            new = list(text)
            new[6] = 'W'
            ''.join(new)
            """


            for i in reversed(range(len(randomBinaryString))):

                #if not randomBinaryString in S:
                #    print "Do something smart"


                #print randomBinaryString[i]


                #If not we change its last letter and check if it is in self. If none of them are, we substitute the digit for a 'u'


                #if not randomBinaryString in S:
                if not chunkMatchesSelf(randomBinaryString,S):
                    flippedRandomBinaryString = list(randomBinaryString)
                    if flippedRandomBinaryString[i] == '0':
                        flippedRandomBinaryString[i] = '1'
                    elif flippedRandomBinaryString[i] == '1':
                        flippedRandomBinaryString[i] = '0'
                    flippedRandomBinaryString = ''.join(flippedRandomBinaryString)
                    #print "Original String", randomBinaryString
                    #print "Flipped new String: ", flippedRandomBinaryString

                    #if not flippedRandomBinaryString in S:
                    if not chunkMatchesSelf(flippedRandomBinaryString,S):
                        #print "Not",randomBinaryString, "nor", flippedRandomBinaryString,"are in S, so we proceed to change the digit for a u"
                        #Code to change the targeted digit for a 'u'
                        temp = list(randomBinaryString)
                        temp[i] = 'u'
                        randomBinaryString = ''.join(temp)
                    #else:
                        #print "Either",randomBinaryString, "or", flippedRandomBinaryString,"are in S, so we DO NOT change the digit for a u"






            
            #if randomBinaryString in detectorChunksList:
            #    print "Already in detectorChunkList!!*********************************"

            else:
                #print "Added to detectorChunkList"
                detectorChunksList.append(randomBinaryString)
                stringOutput = "Number of ",str(maxSelfBinaryStringSize),"-Chunk Detectors Generated: ", str(len(detectorChunksList)),"/",str(sizeSelf)
                stringOutput = ''.join(stringOutput)
                #print stringOutput

                my_gui.changeMessage(stringOutput)
                root.update_idletasks()
                root.update()
                

        #print "Result:", detectorChunksList
        #print "PROCESS FINISHED"

        return detectorChunksList

def generateRandomBinaryString(length):

    return ''.join(random.choice("0" + "1") for _ in range(length))

"""

def chunkMatchesSelf(chunk, size, S):

    print "is this even being called?"

    #S in this case needs to be a list of binary strings. The idea is that, for long commands, we cut the string and keep the part 
    #of interest starting from the end. The value needs to be a preset value.

    #print "***WE START COMPARISON***"

    #We also have to take into account the integer that comes with the chunk and the size of the chunk, that are not the same value

    #Keep in mind that the Integrer has to be >= 1

    #Size is the value of n for the n-chunk

    #print "Chunk String: ", chunk[0]
    #print "Chunk Integer: ", chunk[1]

    startIndex = chunk[1] -1
    endIndex = startIndex + size

    #test = "0123456789"

    #print(test[len(test)-40:len(test)])



    for selfString in S:
        selfTarget = selfString[startIndex:endIndex]

        if selfTarget == chunk[0]:
            #print chunk[0]," IS PART OF SELF ", selfTarget
            return True

        #else:
            #print chunk[0]," is not part of the first checked self ", selfTarget
    
    return False

    



    #print test[startIndex:endIndex]

    #print startIndex, endIndex

"""

#True if chunk is in S, including u symbols
def chunkMatchesSelfSaver(chunk, S, matchingProcessesListIndexes):
    #print "Lenght Chunk",len(chunk)
    #for string in S:
    #    print "Length S",len(string)

    i = 0

    for selfString in S:
        returnValue = False
        flag = True
        for i in range(len(chunk)):
            if not chunk[i] == selfString[i] and not chunk[i] == 'u':
                flag = False
        if flag == True:
            #print "ONE OF THE STRINGS IN SELF MATCHES THE CHUNK"
            #We add the process that has been detected by the Chunks Detectors to the list of anomalies
            if not i in matchingProcessesListIndexes:
                matchingProcessesListIndexes.append(i)
            return True
        
        i += 1
    return False


#True if chunk is in S, including u symbols
def chunkMatchesSelf(chunk, S):
    #print "Lenght Chunk",len(chunk)
    #for string in S:
    #    print "Length S",len(string)
    for selfString in S:
        returnValue = False
        flag = True
        for i in range(len(chunk)):
            if not chunk[i] == selfString[i] and not chunk[i] == 'u':
                flag = False
        if flag == True:
            #print "ONE OF THE STRINGS IN SELF MATCHES THE CHUNK"
            return True
    return False


"""
#Another option for this: 

def chunkMatchesSelf(chunk, S, matchingProcessesList):
    #print "Lenght Chunk",len(chunk)
    #for string in S:
    #    print "Length S",len(string)
    for selfString in S:
        returnValue = False
        flag = True
        for i in range(len(chunk)):
            if not chunk[i] == selfString[i] and not chunk[i] == 'u':
                flag = False
        if flag == True:
            #print "ONE OF THE STRINGS IN SELF MATCHES THE CHUNK"
            #We add the process that has been detected by the Chunks Detectors to the list of anomalies
            matchingProcessesList.append(selfString)
            #return True
            returnValue = True
    #return False

    return returnValue

"""

#We need to make all the strigs size maxSelfBinaryStringSize. We can just add either 0 at the beginning or at the end of the string. We should test both. 
def normaliseLengthStrings(stringList):

    returnList = []

    for string in stringList:
        #print "Size of String:", len(string)
        aditionalDigits = maxSelfBinaryStringSize - len(string)
        #print "Extra letters needed:", aditionalDigits

        tempString = ("0" * aditionalDigits) + string

        #print "Length new string:", len(tempString)

        returnList.append(tempString)

        #print "NEW STRING", tempString

        #print "*********************************************"


    return returnList

#Return list of all the processes considered anomalies.
def anomalyDetection(processesList,chunkList):

    anomalyList = []

    anomaliesDetected = False


    for chunk in chunkList:
        chunkMatchesSelfSaver(chunk, processesList, anomalyList)
        #if chunkMatchesSelfSaver(chunk, processesList, anomalyList):
            #print "Anomaly No",str(len(anomalyList)),"Detected"

    #print anomalyList

    #print "List of all the processes that actually match"

    #print chunkMatchesSelf("0u1u",["0011","1011"])

    return anomalyList


def mainScript(my_gui, root):


    detectorChunksList = []

    if os.path.exists("chunk_list.txt"):
        with open("chunk_list.txt", "rb") as fp:   # Reading list from chunk_list.txt and storing it in variable b
            detectorChunksList = pickle.load(fp)

        my_gui.changeStatusMessage("STATUS: Loaded chunk_list.txt Detector Chunk List")
        root.update_idletasks()
        root.update()

    else:


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
        processListString = listStringsToBinary(processListString)

        #print "*******************************"

        processListString = reduceStringList(processListString)

        #print processListString

        processListString = normaliseLengthStrings(processListString)

        #print len(processListString)

        #returnValue = utils.chunkMatchesSelf(['011', 1], 3, ['00001','01111','01000'])
        #print returnValue

        #returnValue = utils.newChunkMatchesSelf('01100',['00001','01111','01000'])
        #print returnValue

        #selfSet = ['00001','01111','01000']

        selfSet = processListString

        detectorChunksList = chunkGenerator(selfSet, my_gui,root)

        with open("chunk_list.txt", "wb") as fp:   #Storing list in chunk_list.txt
            pickle.dump(detectorChunksList, fp)


    my_gui.changeErrorMessage("Looking for anomalies", "orange")

    #At this point, we have stored the ChunkList in detectorChunksList

    proc_list = get_proc_list()

    processListString = []

    storedProcesses = []

    anomaliesList = []

    for proc in proc_list:
        """
        print proc.pid," ", proc.cmd
        print "Size of String: ", len(proc.cmd)
        if len(proc.cmd) > biggest_size:
            biggest_size = len(proc.cmd)
        """
        #print utils.stringToBinary(proc.cmd)
        processListString.append(proc.cmd)
        storedProcesses.append(proc.cmd)

    #print processListString

    processListString = listStringsToBinary(processListString)

    processListString = reduceStringList(processListString)

    processListString = normaliseLengthStrings(processListString)

    anomaliesListIndexes = anomalyDetection(processListString, detectorChunksList)

    anomaliesStringsList = []

    output = ""

    for index in anomaliesListIndexes:
        anomaliesStringsList.append(storedProcesses[index])
        output += storedProcesses[index] + "\n"

    message = "Anomalies found: " + output

    my_gui.changeErrorMessage(message, "red")

    print len(anomaliesStringsList)

    #print anomaliesStringsList

    #Once these are generated, we want to: 

    #Compare the new processes with the chunks

    #Those who match might be a thread.

    #Don't forget the file thing, that makes a lot of sense

    
    #my_gui.changeErrorMessage("      No Anomalies Detected", "green")


    #We need to set it so runs every 10 seconds for example, while the program is still open. 

    #We have to make it print some feedback on the GUI.

    #We should also print out information on the GUI, like the number of annomalies and the name of the process, maybe cleaned? (Just the last part of the proccess)    

    root.mainloop()