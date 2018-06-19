import commands
status, output = commands.getstatusoutput("ps -A")

#print output

#print output[0]


test = output.split('\n')

print test

print "*****************************************"

print test[0]
print test[1]
print test[2]
#print test[3]
#print test [4]