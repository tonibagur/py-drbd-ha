#!/usr/bin/env python 
# -*- coding: utf-8
import unittest
import parser_drbd
from stub import Stub

class TestDrbdParser(unittest.TestCase):
    def test_parse1(self):
        class ConnectorStub(Stub):
            def getDrbdLines(self):
                return ['version: 8.4.3 (api:1/proto:86-101)\n', 'srcversion: F97798065516C94BE0F27DC \n', '\n', ' 1: cs:Connected ro:Primary/Secondary ds:UpToDate/UpToDate C r-----\n', '    ns:5206108 nr:0 dw:5206108 dr:48757241 al:645 bm:0 lo:0 pe:0 ua:0 ap:0 ep:1 wo:d oos:0\n']
        p=parser_drbd.DrbdParser(1,ConnectorStub())
        p.parse()
        self.assertEqual(p.cs,'Connected')
        self.assertEqual(p.dr1,'Primary')
        self.assertEqual(p.dr2,'Secondary')
        self.assertEqual(p.ds1,'UpToDate')
        self.assertEqual(p.ds2,'UpToDate')
    def test_parse2(self):
        class ConnectorStub(Stub):
            def getDrbdLines(self):
                return ['version: 8.4.3 (api:1/proto:86-101)\n', 'srcversion: F97798065516C94BE0F27DC \n', '\n', ' 1: cs:Connected ro:Secondary/Secondary ds:UpToDate/UpToDate C r-----\n', '    ns:5206108 nr:0 dw:5206108 dr:48757241 al:645 bm:0 lo:0 pe:0 ua:0 ap:0 ep:1 wo:d oos:0\n']
        p=parser_drbd.DrbdParser(1,ConnectorStub())
        p.parse()
        self.assertEqual(p.cs,'Connected')
        self.assertEqual(p.dr1,'Secondary')
        self.assertEqual(p.dr2,'Secondary')
        self.assertEqual(p.ds1,'UpToDate')
        self.assertEqual(p.ds2,'UpToDate')


    def test_parse3(self):
        class ConnectorStub(Stub):
            def getDrbdLines(self):
                return ['version: 8.4.3 (api:1/proto:86-101)\n', 'srcversion: F97798065516C94BE0F27DC \n', '\n', '1: cs:WFConnection ro:Primary/Unknown ds:UpToDate/DUnknown C r-----\n', 'ns:5433228 nr:0 dw:5434240 dr:48876665 al:678 bm:0 lo:0 pe:0 ua:0 ap:0 ep:1 wo:d oos:884\n']
        p=parser_drbd.DrbdParser(1,ConnectorStub())
        p.parse()
        self.assertEqual(p.cs,'WFConnection')
        self.assertEqual(p.dr1,'Primary')
        self.assertEqual(p.dr2,'Unknown')
        self.assertEqual(p.ds1,'UpToDate')
        self.assertEqual(p.ds2,'DUnknown')

class TestHASlaveStrategy(unittest.TestCase):
    def test_both_ok_docker_down(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='Connected'
                self.dr1='Primary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'demote_drbd')
    def test_both_ok_docker_up(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='Connected'
                self.dr1='Primary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_down')
    def test_slave_ok_docker_down(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Primary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_up')
    def test_slave_ok_docker_ok(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Primary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'wait')

    def test_slave_secondary_disconnected_docker_down(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Secondary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'promote_drbd')

    def test_slave_secondary_disconnected_docker_up(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Secondary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_down')
    def test_slave_secondary_connected_secondary_docker_down(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'wait')

    def test_slave_secondary_connected_secondary_docker_up(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_down')
    def test_slave_secondary_connected_primary_docker_up(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_down')
    def test_slave_secondary_connected_primary_docker_down(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Primary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HASlaveStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'wait')

class TestHAMasterStrategy(unittest.TestCase):
    def test_both_ok_docker_down(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='Connected'
                self.dr1='Primary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_up')
    def test_both_ok_docker_up(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='Connected'
                self.dr1='Primary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'wait')
    def test_master_ok_docker_down(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Primary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_up')
    def test_master_ok_docker_ok(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Primary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'wait')

    def test_master_secondary_disconnected_docker_down(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Secondary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'promote_drbd')

    def test_master_secondary_disconnected_docker_up(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='WFConnection'
                self.dr1='Secondary'
                self.dr2='Unknown'
                self.ds1='UpToDate'
                self.ds2='DUnknown'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_down')
    def test_master_secondary_connected_secondary_docker_down(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'promote_drbd')

    def test_master_secondary_connected_secondary_docker_up(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_down')
    def test_master_secondary_connected_primary_docker_up(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Secondary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ok'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'docker_down')
    def test_master_secondary_connected_primary_docker_down(self):
        class ParserStub(Stub):
            implemented_by='parser_drbd.DrbdParser'
            def parse(self):
                self.cs='Connected'
                self.dr1='Secondary'
                self.dr2='Primary'
                self.ds1='UpToDate'
                self.ds2='UpToDate'
        class DockerStatusStub(Stub):
            def get_status(self):
                return 'ko'
        import ha_strategy
        s=ha_strategy.HAMasterStrategy(ParserStub(),DockerStatusStub())
        self.assertEqual(s.next_action(),'wait')

class TestAgent(unittest.TestCase):
    def test1(self):
        import ha_agent
        class StubStrategy(Stub):
            next='a'
            def next_action(self):
                actual=self.next
                if len(self.next)<4:
                    self.next=actual +'a'
                else:
                    return 'unknown_action'   
                return actual
        class StubAgent(ha_agent.Agent):
            actions=[]
            def action_a(self):
                self.actions.append('a')
            def action_aa(self):
                self.actions.append('aa')
            def action_aaa(self):
                self.actions.append('aaa')
            def action_wait(self):
                self.actions.append('w')
        a=StubAgent(StubStrategy())
        a.run()
        self.assertEqual(a.actions,['a','w','aa','w','aaa'])
    def test_kwargs(self):
        import ha_agent
        s='stategy'
        o1='object1'
        o2='object2'
        o3='object3'
        a=ha_agent.Agent(s,o1=o1,o2=o2,o3=o3)
        self.assertEqual(a.strategy,s)
        self.assertEqual(a.o1,o1)
        self.assertEqual(a.o2,o2)
        self.assertEqual(a.o3,o3)


class TestHAAgent(unittest.TestCase):
    class DockerRunnerStub(Stub):
        up=False
        down=False
        def docker_up(self):
            self.up=True
        def docker_down(self):
            self.down=True
    class DrbdManagerStub(Stub):
        demoted=False
        promoted=False
        def demote_drbd(self):
            self.demoted=True
        def promote_drbd(self):
            self.promoted=True
    def test_docker(self):
        import ha_agent
        s='strategy'
        r=self.DockerRunnerStub()
        ha=ha_agent.HAAgent(s,docker_runner=r)
        self.assertEqual(r.up,False)
        ha.action_docker_up()
        self.assertEqual(r.up,True)
        self.assertEqual(r.down,False)
        ha.action_docker_down()
        self.assertEqual(r.down,True)
    def test_drbd(self):
        import ha_agent
        s='strategy'
        r=self.DrbdManagerStub()
        ha=ha_agent.HAAgent(s,drbd_manager=r)
        self.assertEqual(r.promoted,False)
        ha.action_promote_drbd()
        self.assertEqual(r.promoted,True)
        self.assertEqual(r.demoted,False)
        ha.action_demote_drbd()
        self.assertEqual(r.demoted,True)

#implementar casuistica dependencies de serveis            
#quan hi hagi accio desconeguda agent ha de fallar i enviar email

if __name__=='__main__':
    unittest.main()
