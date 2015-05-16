
class DrbdStatus(object):
    def __init__(self,drbd_file='/proc/drbd'):
        self.drbd_file=drbd_file
    def getDrbdLines(self):
        f=open(self.drbd_file)
        l=f.readlines() 
        f.close()
        return l


if __name__=='__main__':
    print DrbdStatus().getDrbdLines()    
