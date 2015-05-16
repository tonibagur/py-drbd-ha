import os

class DockerRunner(object):
    def __init__(self,supervisor_file):
        self.supervisor_file=supervisor_file
    def docker_down(self):
        os.popen('supervisorctl -c {0} shutdown'.format(self.supervisor_file)).read()
    def docker_up(self):
        os.popen('supervisord -c {0}'.format(self.supervisor_file)).read()


if __name__=='__main__':
   pass
   #DockerRunner('/home/coneptum/railkivy_phonegap/supervisor/postgres_prepro.conf').docker_down() 
   #DockerRunner('/home/coneptum/railkivy_phonegap/supervisor/postgres_prepro.conf').docker_up() 
