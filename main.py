print "Hello World!"

import os
#os.system("ps -A")

import commands
status, output = commands.getstatusoutput("ps -A")