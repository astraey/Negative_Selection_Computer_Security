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



# Returns a list with all the contiguouss detectors for the given Self.
def contiguousGenerator(S, my_gui, root):

    if S:

        detectorcontiguousList = []

        sizeSelf = len(S)
        sizeStringsSelf = len(S[0])


        # We use the length of self to get an idea of the initial random contiguouss that we want to generate. This value can  be modified.
        # We can't append them directly, we have to check wether it matches Self or not, and also change it to the minimal form patern.
        # We also need to delete repeated members of the list, as in the new form they will most likely be repeated.
        while not sizeSelf == len(detectorcontiguousList):

            randomBinaryString = generateRandomBinaryString(sizeStringsSelf)

            for i in reversed(range(len(randomBinaryString))):

                # If it doesn't match self, we change its last digit and check if it is in self. If none of them are, we substitute the digit for a 'u'
                # The goal is to transform the contiguous into the minimal form.
                if not contiguousMatchesSelf(randomBinaryString,S):
                    flippedRandomBinaryString = list(randomBinaryString)
                    if flippedRandomBinaryString[i] == '0':
                        flippedRandomBinaryString[i] = '1'
                    elif flippedRandomBinaryString[i] == '1':
                        flippedRandomBinaryString[i] = '0'
                    flippedRandomBinaryString = ''.join(flippedRandomBinaryString)

                    if not contiguousMatchesSelf(flippedRandomBinaryString,S):

                        # We change the targeted digit for a 'u'
                        temp = list(randomBinaryString)
                        temp[i] = 'u'
                        randomBinaryString = ''.join(temp)

            else:

                # We add it to the detector contiguous list
                detectorcontiguousList.append(randomBinaryString)
                stringOutput = "Number of ",str(maxSelfBinaryStringSize),"-contiguous Detectors Generated: ", str(len(detectorcontiguousList)),"/",str(sizeSelf)
                stringOutput = ''.join(stringOutput)

                # We update the GUI
                my_gui.changeMessage(stringOutput)
                root.update_idletasks()
                root.update()

        return detectorcontiguousList

# Returns a randomly generated binary string
def generateRandomBinaryString(length):

    return ''.join(random.choice("0" + "1") for _ in range(length))


# Saves the indexes of the processes that match in the list passed as a parameter: matchingProcessesListIndexes
# Takes into account 'u' symbols
def contiguousMatchesSelfSaver(contiguous, S, matchingProcessesListIndexes):

    j = 0

    for selfString in S:
        flag = True
        for i in range(len(contiguous)):
            if not contiguous[i] == selfString[i] and not contiguous[i] == 'u':
                flag = False

        if flag == True:

            if not j in matchingProcessesListIndexes:
                matchingProcessesListIndexes.append(j)
        j += 1


# Returns True if contiguous is in S, including u symbols
def contiguousMatchesSelf(contiguous, S):
    for selfString in S:
        returnValue = False
        flag = True
        for i in range(len(contiguous)):
            if not contiguous[i] == selfString[i] and not contiguous[i] == 'u':
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
def anomalyDetection(processesList,contiguousList):

    anomalyList = []
    anomaliesDetected = False

    for contiguous in contiguousList:
        contiguousMatchesSelfSaver(contiguous, processesList, anomalyList)

    return anomalyList


# Main Script, executes all the backend processes for training and runing the system.
def mainScript(my_gui, root):

    detectorcontiguousList = []

    # If file exists, reading contiguous detector list from file contiguous_list.txt and storing it in variable detectorcontiguousList
    if os.path.exists("contiguous_list.txt"):
        with open("contiguous_list.txt", "rb") as fp:   
            detectorcontiguousList = pickle.load(fp)

        my_gui.changeStatusMessage("STATUS: Loaded contiguous_list.txt Detector contiguous List")
        root.update_idletasks()
        root.update()

    # If file does not exist, it generates a contiguous detector list and stores in file contiguous_list.txt and in variable detectorcontiguousList
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

        detectorcontiguousList = contiguousGenerator(selfSet, my_gui,root)

        # Stores generated contiguous detector list in file contiguous_list.txt
        with open("contiguous_list.txt", "wb") as fp:
            pickle.dump(detectorcontiguousList, fp)


    # At this point, we have a set of contiguous detectors and we will proceed with the anomaly detection.

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

    anomaliesListIndexes = anomalyDetection(processListString, detectorcontiguousList)
    
    output = ""

    for index in anomaliesListIndexes:
        anomaliesStringsList.append(storedProcesses[index])
        output += storedProcesses[index] + "\n"

    message = "Anomalies found\n" + output

    my_gui.changeErrorMessage(message, "red")

    #Keep the graphical user interface open
    root.mainloop()