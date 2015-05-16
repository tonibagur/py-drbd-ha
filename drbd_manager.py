import os
import time

class DrbdManager(object):
    wait_time=2
    def __init__(self,resource_name,mount_point,drbd_device):
        self.resource_name=resource_name
        self.mount_point=mount_point
        self.drbd_device=drbd_device
    def promote_drbd(self):
        os.popen('drbdadm primary --force {0}'.format(self.resource_name)).read()
        time.sleep(self.wait_time)
        os.popen('mount {0} {1}'.format(self.drbd_device,self.mount_point)).read()
    
    def demote_drbd(self):
        os.popen('umount {0}'.format(self.mount_point)).read()
        time.sleep(self.wait_time)
        os.popen('drbdadm secondary {0}'.format(self.resource_name)).read()

if __name__=='__main__':
    pass
    #DrbdManager('vdocker03','/volumes2','/dev/drbd2').demote_drbd()
    #DrbdManager('vdocker03','/volumes2','/dev/drbd2').promote_drbd()
