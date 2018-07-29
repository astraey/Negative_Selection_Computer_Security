
import random
import string
from subprocess import Popen, PIPE
from gui import SystemGUI
from Tkinter import Tk, Label, Button
from re import split
from process import Proc

maxSelfBinaryStringSize = 138


root = Tk()
my_gui = SystemGUI(root)
#root.mainloop()
root.update_idletasks()
root.update()

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




def chunkMatchesSelf(chunk, size, S):

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



#This funcion returns a list with all the chunks detectors for the given self. This is where the magic happens

def chunkGenerator(S):

    if S:

        detectorChunksList = []

        sizeSelf = len(S)
        sizeStringsSelf = len(S[0])

        #print "Chunk Generator Initiated"

        #print "Self:", S


        #We use the length of self to get an idea of the initial random chunks that we want to generate, but this value can  be modified.
        for i in range(sizeSelf):
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
                stringOutput = "Number of ",str(maxSelfBinaryStringSize),"-Chunk Detectors Generated: ", str(len(detectorChunksList)),
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


#True if chunk is in S, including u symbols
def chunkMatchesSelf(chunk, S):
    #print "Lenght Chunk",len(chunk)
    #for string in S:
    #    print "Length S",len(string)
    for selfString in S:
        flag = True
        for i in range(len(chunk)):
            if not chunk[i] == selfString[i] and not chunk[i] == 'u':
                flag = False
        if flag == True:
            #print "ONE OF THE STRINGS IN SELF MATCHES THE CHUNK"
            return True
    return False


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


