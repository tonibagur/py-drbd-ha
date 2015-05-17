from  ha_factory import HAFactory
import sys

def main():
    if len(sys.argv)>1 and sys.argv[1]=='master': 
        agent=HAFactory().buildMasterHaAgent()
        print "running master ha agent"
        agent.run()
    elif len(sys.argv)>1 and sys.argv[1]=='slave': 
        agent=HAFactory().buildSlaveHaAgent()
        print "running slave ha agent"
        agent.run()
    else:
        print "Use: python ha_runner.py master|slave"

if __name__=='__main__':
    main()
