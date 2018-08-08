from subprocess import Popen, PIPE
from gui import SystemGUI
from Tkinter import Tk, Label, Button
from re import split
from process import Proc
import random
import string
import os.path
import binascii
import pickle

maxSelfBinaryStringSize = 138

# Return a list of Proc objects representing the active processes in the system
def get_proc_list():

    proc_list = []
    sub_proc = Popen(['ps', 'aux'], shell=False, stdout=PIPE)
    sub_proc.stdout.readline()

    for line in sub_proc.stdout:
        proc_info = split(" *", line)

        # Only s is stored
        aux_process = Proc(proc_info)
        aux_process.cmd = aux_process.cmd.replace("\n","")
        aux_process.cmd = aux_process.cmd.replace(" ","")

        proc_list.append(aux_process)
    return proc_list

# Returns the binary conversion of the string passed as a parameter
def stringToBinary(string): 
    
    return ''.join(format(ord(x), 'b') for x in string)

# Returns a list of strings converted to binary
def listStringsToBinary(listStrings):

    newListStrings = []

    for string in listStrings:

        newListStrings.append(stringToBinary(string))

    return newListStrings

# Reduces the size of the binary string the numeric value stored in the variable maxSelfBinaryStringSize. Starts from the last digit of the string. 
def reduceStringList(listStrings):

    newListStrings = []

    for string in listStrings:
        newListStrings.append(string[len(string)-maxSelfBinaryStringSize:len(string)])

    return newListStrings



# Returns a list with all the chunks detectors for the given Self.
def chunkGenerator(S, my_gui, root):

    if S:

        detectorChunksList = []

        sizeSelf = len(S)
        sizeStringsSelf = len(S[0])


        # We use the length of self to get an idea of the initial random chunks that we want to generate. This value can  be modified.
        # We can't append them directly, we have to check wether it matches Self or not, and also change it to the minimal form patern.
        # We also need to delete repeated members of the list, as in the new form they will most likely be repeated.
        while not sizeSelf == len(detectorChunksList):

            randomBinaryString = generateRandomBinaryString(sizeStringsSelf)

            for i in reversed(range(len(randomBinaryString))):

                # If it doesn't match self, we change its last digit and check if it is in self. If none of them are, we substitute the digit for a 'u'
                # The goal is to transform the chunk into the minimal form.
                if not chunkMatchesSelf(randomBinaryString,S):
                    flippedRandomBinaryString = list(randomBinaryString)
                    if flippedRandomBinaryString[i] == '0':
                        flippedRandomBinaryString[i] = '1'
                    elif flippedRandomBinaryString[i] == '1':
                        flippedRandomBinaryString[i] = '0'
                    flippedRandomBinaryString = ''.join(flippedRandomBinaryString)

                    if not chunkMatchesSelf(flippedRandomBinaryString,S):

                        # We change the targeted digit for a 'u'
                        temp = list(randomBinaryString)
                        temp[i] = 'u'
                        randomBinaryString = ''.join(temp)

            else:

                # We add it to the detector chunk list
                detectorChunksList.append(randomBinaryString)
                stringOutput = "Number of ",str(maxSelfBinaryStringSize),"-Chunk Detectors Generated: ", str(len(detectorChunksList)),"/",str(sizeSelf)
                stringOutput = ''.join(stringOutput)

                # We update the GUI
                my_gui.changeMessage(stringOutput)
                root.update_idletasks()
                root.update()

        return detectorChunksList

# Returns a randomly generated binary string
def generateRandomBinaryString(length):

    return ''.join(random.choice("0" + "1") for _ in range(length))


# Saves the indexes of the processes that match in the list passed as a parameter: matchingProcessesListIndexes
# Takes into account 'u' symbols
def chunkMatchesSelfSaver(chunk, S, matchingProcessesListIndexes):

    j = 0

    for selfString in S:
        flag = True
        for i in range(len(chunk)):
            if not chunk[i] == selfString[i] and not chunk[i] == 'u':
                flag = False

        if flag == True:

            if not j in matchingProcessesListIndexes:
                matchingProcessesListIndexes.append(j)
        j += 1


# Returns True if chunk is in S, including u symbols
def chunkMatchesSelf(chunk, S):
    for selfString in S:
        returnValue = False
        flag = True
        for i in range(len(chunk)):
            if not chunk[i] == selfString[i] and not chunk[i] == 'u':
                flag = False
        if flag == True:
            return True
    return False


# We need to make all the strigs size maxSelfBinaryStringSize
def normaliseLengthStrings(stringList):

    returnList = []

    for string in stringList:
        aditionalDigits = maxSelfBinaryStringSize - len(string)
        tempString = ("0" * aditionalDigits) + string
        returnList.append(tempString)

    return returnList

# Return list of all the processes considered anomalies.
def anomalyDetection(processesList,chunkList):

    anomalyList = []
    anomaliesDetected = False

    for chunk in chunkList:
        chunkMatchesSelfSaver(chunk, processesList, anomalyList)

    return anomalyList


# Main Script, executes all the backend processes for training and runing the system.
def mainScript(my_gui, root):

    detectorChunksList = []

    # If file exists, reading chunk detector list from file chunk_list.txt and storing it in variable detectorChunksList
    if os.path.exists("chunk_list.txt"):
        with open("chunk_list.txt", "rb") as fp:   
            detectorChunksList = pickle.load(fp)

        my_gui.changeStatusMessage("STATUS: Loaded chunk_list.txt Detector Chunk List")
        root.update_idletasks()
        root.update()

    # If file does not exist, it generates a chunk detector list and stores in file chunk_list.txt and in variable detectorChunksList
    else:

        proc_list = get_proc_list()

        biggest_size = 0

        processListString = []

        for proc in proc_list:

            processListString.append(proc.cmd)

        processListString = listStringsToBinary(processListString)

        processListString = reduceStringList(processListString)

        processListString = normaliseLengthStrings(processListString)

        selfSet = processListString

        detectorChunksList = chunkGenerator(selfSet, my_gui,root)

        # Stores generated chunk detector list in file chunk_list.txt
        with open("chunk_list.txt", "wb") as fp:
            pickle.dump(detectorChunksList, fp)


    # At this point, we have a set of chunk detectors and we will proceed with the anomaly detection.

    processListString = []

    storedProcesses = []

    anomaliesList = []

    anomaliesStringsList = []

    my_gui.changeErrorMessage("Looking for anomalies", "orange")

    # We store the list of processes running in the system
    proc_list = get_proc_list()

    for proc in proc_list:
        processListString.append(proc.cmd)
        storedProcesses.append(proc.cmd)

    processListString = listStringsToBinary(processListString)

    processListString = reduceStringList(processListString)

    processListString = normaliseLengthStrings(processListString)

    anomaliesListIndexes = anomalyDetection(processListString, detectorChunksList)
    
    output = ""

    for index in anomaliesListIndexes:
        anomaliesStringsList.append(storedProcesses[index])
        output += storedProcesses[index] + "\n"

    message = "Anomalies found\n" + output

    my_gui.changeErrorMessage(message, "red")

    # Next steps

    # We need to set it so runs every 10 seconds for example, while the program is still open. 

    # We need to show on screen when the scan has run? Potentially. 

    # Maybe simplify the name of the shown processes(Just the last part of the proccess, the actual name of the script.  

    root.mainloop()