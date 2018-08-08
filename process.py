
# Data structure for a processes
# The class properties are process attributes
class Proc(object):
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
 
    # Returns a string containing minimal info about the process : user, pid, and command
    def to_str(self):
        return '%s %s %s' % (self.user, self.pid, self.cmd)