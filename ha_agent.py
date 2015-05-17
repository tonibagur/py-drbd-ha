import time

class Agent(object):
    last_action=''
    def __init__(self,strategy,**kwargs):
        self.strategy=strategy
        for k in kwargs:
            setattr(self,k,kwargs[k])
    def run(self):
        self.last_action=self.strategy.next_action()
        while (self.last_action!='unknown_action'):
            print "last_action",self.last_action
            method=getattr(self,'action_'+self.last_action)
            method()
            self.last_action=self.strategy.next_action()
            if self.last_action!='unknown_action' and self.last_action!='action_wait':    
                self.action_wait()

class HAAgent(Agent):
     wait_time=5
     def action_docker_up(self):
         self.docker_runner.docker_up()
     def action_docker_down(self):
         self.docker_runner.docker_down()
     def action_promote_drbd(self):
         self.drbd_manager.promote_drbd()
     def action_demote_drbd(self):
         self.drbd_manager.demote_drbd()
     def action_wait(self):
         time.sleep(self.wait_time)
	
