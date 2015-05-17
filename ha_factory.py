import parser_drbd
import docker_status
import ha_strategy
import ha_agent
import docker_runner
import drbd_manager

class HAFactory(object):
    def __init__(self):
        self.config={
            'num':2,
            'supervisor_file_master':'/home/coneptum/railkivy_phonegap/supervisor/postgres_prepro_master.conf',
            'supervisor_file_slave':'/home/coneptum/railkivy_phonegap/supervisor/postgres_prepro_slave.conf',
            'resource_name':'vdocker03',
            'mount_point':'/volumes2',
            'drbd_device':'/dev/drbd2',
            
        }
    def buildHaAgent(self,Strategy,supervisor_file):
        self.parser=parser_drbd.DrbdParser(self.config['num'])
        self.docker_status=docker_status.DockerStatus(supervisor_file)
        self.strategy=Strategy(self.parser,self.docker_status)
        self.docker_runner=docker_runner.DockerRunner(supervisor_file)
        self.drbd_manager=drbd_manager.DrbdManager(self.config['resource_name'],self.config['mount_point'],self.config['drbd_device'])
        self.agent=ha_agent.HAAgent(self.strategy,docker_runner=self.docker_runner,drbd_manager=self.drbd_manager)
        return self.agent
    def buildMasterHaAgent(self):
        return self.buildHaAgent(ha_strategy.HAMasterStrategy,self.config['supervisor_file_master'])
    def buildSlaveHaAgent(self):
        return self.buildHaAgent(ha_strategy.HASlaveStrategy,self.config['supervisor_file_slave'])

        
