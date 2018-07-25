
import random
import string

maxSelfStringSize = 20


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
        newListStrings.append(string[len(string)-maxSelfStringSize:len(string)])

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



def newChunkMatchesSelf(chunk, S):
    print "New chunkMatches"

    #The chunk and the strings in S need to be the same size

    print chunk
    print S

    return True


#This funcion returns a list with all the chunks detectors for the given self. This is where the magic happens

def chunkGenerator(S):

    detectorChunksList = []

    sizeSelf = len(S)
    sizeStringsSelf = len(S[0])

    print "Chunk Generator Initiated"

    print "Self:", S


    for i in range(sizeSelf):
        #We can't append them directly, we have to check wether it matches Self or not, and also change it to the minimal form.
        #We also need to delete repeated members of the list, as in the new form they will most likely be repeated.

        randomBinaryString = generateRandomBinaryString(sizeStringsSelf)


        #Here we should check if this matches the list.

        #Do the whole replacing here.

        """For replacing a character in a String: 
        text = 'abcdefg'
        new = list(text)
        new[6] = 'W'
        ''.join(new)
        """


        for i in reversed(range(len(randomBinaryString))):

            if not randomBinaryString in S:
                print "Do something smart"


            #print randomBinaryString[i]

            #If not we change its last letter and check if it is in self.

            #Code to change the targeted digit for a 'u'
            temp = list(randomBinaryString)
            temp[i] = 'u'
            randomBinaryString = ''.join(temp)

        
        if randomBinaryString in detectorChunksList:
            print "Already in self!!*********************************"

        else:
            print "Added to detectors, not in detectorChunksList yet"
            detectorChunksList.append(randomBinaryString)   

    print "Result:", detectorChunksList

    return detectorChunksList

def generateRandomBinaryString(length):

    return ''.join(random.choice("0" + "1") for _ in range(length))


#True if chunk is in S, including u symbols
def chunkMatchesSelf(chunk, S):
    for selfString in S:
        flag = True
        for i in range(len(chunk)):
            if not chunk[i] == selfString[i] and not chunk[i] == 'u':
                flag = False
        if flag == True:
            print "ONE OF THE STRINGS MATCHES"
            return True
    return False


