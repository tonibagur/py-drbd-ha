
class HAMasterStrategy(object):
    def __init__(self,drbd_parser,docker_status):
        self.drbd_parser=drbd_parser
        self.docker_status=docker_status
    def next_action(self):
        self.drbd_parser.parse()
        if self.drbd_parser.cs=='Connected' and \
           self.drbd_parser.dr1=='Primary' and \
           self.drbd_parser.dr2=='Secondary' and \
           self.drbd_parser.ds1=='UpToDate' and \
           self.drbd_parser.ds2=='UpToDate':
           if self.docker_status.get_status()=='ko':
               return 'docker_up'
           elif self.docker_status.get_status()=='ok':
               return 'wait'
        elif self.drbd_parser.cs=='WFConnection' and \
           self.drbd_parser.dr1=='Primary' and \
           self.drbd_parser.dr2=='Unknown' and \
           self.drbd_parser.ds1=='UpToDate' and \
           self.drbd_parser.ds2=='DUnknown':
           if self.docker_status.get_status()=='ok':
               return 'wait'
           elif self.docker_status.get_status()=='ko':
               return 'docker_up'
        return 'unknown_action'
