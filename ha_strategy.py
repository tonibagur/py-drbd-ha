
class HAMasterStrategy(object):
    def __init__(self,drbd_parser,docker_status):
        self.drbd_parser=drbd_parser
        self.docker_status=docker_status
    def next_action(self):
        self.drbd_parser.parse()
        if self.drbd_parser.dr1=='Primary' and \
           self.drbd_parser.ds1=='UpToDate':
           return self.start_docker_if_down()
        elif self.drbd_parser.dr1=='Secondary':
           if self.docker_status.get_status()=='ok':
               return 'docker_down'
           elif self.drbd_parser.dr2 in('Secondary','Unknown') and self.drbd_parser.ds1=='UpToDate':
               return 'promote_drbd'
           elif self.drbd_parser.dr2=='Primary':
               return 'wait'
        return 'unknown_action'
    def start_docker_if_down(self):
        status=self.docker_status.get_status()
        print "start_docker_if_down,status:",status
        if status=='ok':
           return 'wait'
        elif status=='ko':
           return 'docker_up'

class HASlaveStrategy(object):
    def __init__(self,drbd_parser,docker_status):
        self.drbd_parser=drbd_parser
        self.docker_status=docker_status
    def next_action(self):
        self.drbd_parser.parse()
        if self.drbd_parser.dr1=='Primary' and \
           self.drbd_parser.ds1=='UpToDate':
           return self.start_docker_if_down_and_master_down()
        elif self.drbd_parser.dr1=='Secondary':
           if self.docker_status.get_status()=='ok':
               return 'docker_down'
           elif self.drbd_parser.dr2 == 'Unknown' and self.drbd_parser.ds1=='UpToDate':
               return 'promote_drbd'
           elif self.drbd_parser.dr2 in ('Primary','Secondary'):
               return 'wait'
        return 'unknown_action'
    def start_docker_if_down_and_master_down(self):
        if self.docker_status.get_status()=='ok':
           if self.drbd_parser.dr2=='Secondary':
               return 'docker_down'
           else:
               return 'wait'
        elif self.docker_status.get_status()=='ko':
           if self.drbd_parser.dr2=='Secondary':
               return 'demote_drbd'
           else:
               return 'docker_up'
