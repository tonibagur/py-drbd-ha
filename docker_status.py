import os

class DockerStatus(object):
    def __init__(self,supervisor_file):
        self.supervisor_file=supervisor_file
    def get_status(self):
        lines=os.popen('supervisorctl -c {0} status'.format(self.supervisor_file)).readlines()
        print lines
        status='ok'
        if lines[0].find('refused connection')!=-1:
            status='ko'
        return status


if __name__=='__main__':
    print DockerStatus('/home/coneptum/railkivy_phonegap/supervisor/postgres_prepro.conf').get_status()    
