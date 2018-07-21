
def stringToBinary(string): 
    
    return ''.join(format(ord(x), 'b') for x in string)


def chunkMatchesSelf(chunk, size, S):

    print "***WE START COMPARISON***"

    #We also have to take into account the integer that comes with the chunk and the size of the chunk, that are not the same value

    #Keep in mind that the Integrer has to be >= 1

    #Size is the value of n for the n-chunk

    print "Chunk String: ", chunk[0]
    print "Chunk Integer: ", chunk[1]

    startIndex = chunk[1] -1
    endIndex = startIndex + size



    for selfString in S:
        selfTarget = selfString[startIndex:endIndex]

        if selfTarget == chunk[0]:
            print chunk[0]," IS PART OF SELF ", selfTarget
            return True

        else:
            print chunk[0]," is not part of the first checked self ", selfTarget
    
    return False

    
    test = "0123456789"

    #print test[startIndex:endIndex]

    #print startIndex, endIndex